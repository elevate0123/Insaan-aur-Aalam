# -*- coding: utf-8 -*-
"""
build_network.py — Graph Construction, Dossier §5.6.

Builds the weighted, UNDIRECTED co-occurrence graph (§4.4 "Note on directed
vs undirected" — this is a deliberate, documented decision, not an
oversight; directionality is retained as an edge attribute but does NOT
drive topology).

Computes:
  - Weighted degree, betweenness, closeness centrality
  - Bootstrap CIs on weighted degree (edge-resampling), classifying each
    node Stable / Moderate / Unstable per §5.6 — ONLY Stable and Moderate
    nodes should be cited as primary centrality findings in any paper
  - Dyadic entropy (Shannon) per node
  - 100-run Louvain consensus partition at gamma=1.0, plus sensitivity runs
    at gamma=0.5 and gamma=2.0 (Appendix A.2.6)
  - Respects F1_Include_in_Network from the master CSV — nodes flagged "No"
    are excluded from the graph AND a warning is printed listing which
    Disputed/Supra-polarity nodes were included because their flag is still
    "Yes" pending consultant review (see config.py comment on this)

Exports GraphML (archival) and GEXF (Gephi import) per §5.6.

USAGE:
    python build_network.py
"""

import csv
import math
import random
import sys
import argparse
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import networkx as nx
try:
    import community as community_louvain  # python-louvain package name is 'community'
except ImportError:
    print("ERROR: python-louvain not installed correctly. pip install python-louvain")
    sys.exit(1)

from config import (
    DYAD_OUTPUT_CSV, DIVINE_NAMES_CSV, CENTRALITY_OUTPUT_CSV, COMMUNITY_OUTPUT_CSV,
    GRAPH_GRAPHML_PATH, GRAPH_GEXF_PATH, BOOTSTRAP_RESAMPLES, LOUVAIN_RUNS,
    LOUVAIN_GAMMA_PRIMARY, LOUVAIN_GAMMA_SENSITIVITY, LOUVAIN_CONSENSUS_THRESHOLD,
    CENTRALITY_STABLE_COV, CENTRALITY_MODERATE_COV, RANDOM_SEED,
)
from names_loader import load_divine_names
from filters import load_dyads as filtered_load_dyads, print_filter_report


def load_dyads(path=DYAD_OUTPUT_CSV, confident_only=True):
    rows, n_excl, n_total = filtered_load_dyads(path, confident_only)
    print_filter_report("build_network", n_excl, n_total, confident_only)
    return rows


def build_graph(dyads, names_by_serial, respect_network_flag=True):
    G = nx.Graph()
    excluded_disputed = []

    for n in names_by_serial.values():
        if respect_network_flag and not n.include_in_network:
            continue
        G.add_node(n.serial, label=n.transliteration, tier=n.tier, jjk_v21=n.jjk_v21)
        if n.jjk_v21 == "Disputed":
            excluded_disputed.append(n.transliteration)

    for row in dyads:
        a, b = int(row["name_1_serial"]), int(row["name_2_serial"])
        if a not in G.nodes or b not in G.nodes:
            continue  # excluded by network flag above
        direction = f"{row['name_1_translit']}->{row['name_2_translit']}"
        if G.has_edge(a, b):
            G[a][b]["weight"] += 1
            # BUGFIX (found via real run): GraphML/GEXF writers both throw
            # (and leave a 0-byte file behind, no useful error surfaced to
            # the user) if an edge attribute is a Python list — "GraphML
            # does not support type <class 'list'> as data values." Keep
            # this as a STRING, capped, not an accumulating list.
            existing = G[a][b].get("direction_examples", "")
            examples = existing.split(";") if existing else []
            if len(examples) < 5:  # cap so the string doesn't grow unbounded on a 600+ weight edge
                examples.append(direction)
            G[a][b]["direction_examples"] = ";".join(examples)
        else:
            G.add_edge(a, b, weight=1, direction_examples=direction)

    if excluded_disputed:
        print(f"NOTE: {len(excluded_disputed)} Disputed/Supra-polarity node(s) are INCLUDED in this "
              f"graph because F1_Include_in_Network is still 'Yes' for them (pending consultant "
              f"review — see workbook): {excluded_disputed}")

    return G


def dyadic_entropy(G, node):
    """Shannon entropy of a node's partner-frequency distribution, in bits."""
    weights = [G[node][nbr]["weight"] for nbr in G.neighbors(node)]
    total = sum(weights)
    if total == 0:
        return 0.0
    entropy = 0.0
    for w in weights:
        p = w / total
        entropy -= p * math.log2(p)
    return entropy


def bootstrap_degree_ci(G, node, n_resamples, seed):
    """
    Resamples EDGES (not nodes) with replacement to build a bootstrap
    distribution of this node's weighted degree, per §5.6. Returns
    (mean, std, cov, lower_ci, upper_ci, stability_label).
    """
    edges = list(G.edges(data=True))
    rng = random.Random(seed + node)  # per-node seed offset for independence, still reproducible
    degrees = []
    for _ in range(n_resamples):
        sample = [edges[rng.randrange(len(edges))] for _ in range(len(edges))]
        deg = sum(d["weight"] for u, v, d in sample if u == node or v == node)
        degrees.append(deg)
    degrees.sort()
    mean = sum(degrees) / len(degrees)
    var = sum((x - mean) ** 2 for x in degrees) / len(degrees)
    std = var ** 0.5
    cov = std / mean if mean > 0 else float("inf")
    lo = degrees[int(0.025 * len(degrees))]
    hi = degrees[int(0.975 * len(degrees))]

    if cov < CENTRALITY_STABLE_COV:
        label = "Stable"
    elif cov < CENTRALITY_MODERATE_COV:
        label = "Moderate"
    else:
        label = "Unstable"
    return mean, std, cov, lo, hi, label


def run_louvain_consensus(G, gamma, n_runs, seed):
    """
    Runs Louvain n_runs times with different random seeds, returns:
      - consensus partition: node -> most-frequent community label
      - stability: node -> fraction of runs where it landed in its consensus community
    """
    node_community_votes = defaultdict(Counter)
    rng = random.Random(seed)

    for run in range(n_runs):
        run_seed = rng.randint(0, 2**31 - 1)
        partition = community_louvain.best_partition(G, weight="weight", resolution=gamma, random_state=run_seed)
        for node, comm in partition.items():
            node_community_votes[node][comm] += 1

    consensus = {}
    stability = {}
    for node, votes in node_community_votes.items():
        best_comm, best_count = votes.most_common(1)[0]
        consensus[node] = best_comm
        stability[node] = best_count / n_runs

    return consensus, stability


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-unreviewed", action="store_true",
                         help="Include homonym-flagged/unreviewed names. Default (off) excludes them — "
                              "see filters.py; this is what fixes Al-'Alī showing up as a top hub.")
    args = parser.parse_args()
    confident_only = not args.include_unreviewed

    print("Loading names and dyads...")
    names = load_divine_names()
    names_by_serial = {n.serial: n for n in names}
    dyads = load_dyads(confident_only=confident_only)

    print("Building undirected weighted graph (§4.4 — directionality retained as edge metadata only)...")
    G = build_graph(dyads, names_by_serial)
    print(f"  {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.\n")

    suffix = "" if confident_only else "_UNREVIEWED_INCLUDED"
    centrality_out = CENTRALITY_OUTPUT_CSV.with_name(CENTRALITY_OUTPUT_CSV.stem + suffix + CENTRALITY_OUTPUT_CSV.suffix)
    community_out = COMMUNITY_OUTPUT_CSV.with_name(COMMUNITY_OUTPUT_CSV.stem + suffix + COMMUNITY_OUTPUT_CSV.suffix)
    graphml_out = GRAPH_GRAPHML_PATH.with_name(GRAPH_GRAPHML_PATH.stem + suffix + GRAPH_GRAPHML_PATH.suffix)
    gexf_out = GRAPH_GEXF_PATH.with_name(GRAPH_GEXF_PATH.stem + suffix + GRAPH_GEXF_PATH.suffix)

    print(f"Computing centrality metrics + bootstrap CIs ({BOOTSTRAP_RESAMPLES} resamples/node — slow step)...")
    betweenness = nx.betweenness_centrality(G, weight="weight")
    closeness = nx.closeness_centrality(G, distance="weight")

    centrality_rows = []
    for i, node in enumerate(G.nodes()):
        mean, std, cov, lo, hi, label = bootstrap_degree_ci(G, node, BOOTSTRAP_RESAMPLES, RANDOM_SEED)
        entropy = dyadic_entropy(G, node)
        n = names_by_serial[node]
        centrality_rows.append({
            "serial": node, "transliteration": n.transliteration, "jjk_v21": n.jjk_v21,
            "weighted_degree": G.degree(node, weight="weight"),
            "degree_bootstrap_mean": round(mean, 3), "degree_bootstrap_cov": round(cov, 4),
            "degree_ci_lower": lo, "degree_ci_upper": hi,
            "stability_label": label,
            "betweenness_centrality": round(betweenness[node], 6),
            "closeness_centrality": round(closeness[node], 6),
            "dyadic_entropy_bits": round(entropy, 4),
            "unique_partners": G.degree(node),
        })
        if (i + 1) % 10 == 0:
            print(f"  ...{i+1}/{G.number_of_nodes()} nodes done")

    centrality_out.parent.mkdir(parents=True, exist_ok=True)
    with open(centrality_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(centrality_rows[0].keys()))
        writer.writeheader()
        writer.writerows(centrality_rows)

    n_stable = sum(1 for r in centrality_rows if r["stability_label"] == "Stable")
    n_moderate = sum(1 for r in centrality_rows if r["stability_label"] == "Moderate")
    n_unstable = sum(1 for r in centrality_rows if r["stability_label"] == "Unstable")
    print(f"\nWrote centrality table -> {centrality_out}")
    print(f"  Stable: {n_stable}  Moderate: {n_moderate}  Unstable: {n_unstable}")
    print(f"  REMINDER (§5.6): only Stable+Moderate nodes ({n_stable + n_moderate}/{len(centrality_rows)}) "
          f"should be cited as primary centrality findings in any paper.\n")

    print(f"Running {LOUVAIN_RUNS}-run Louvain consensus at gamma={LOUVAIN_GAMMA_PRIMARY} (primary)...")
    consensus, stability = run_louvain_consensus(G, LOUVAIN_GAMMA_PRIMARY, LOUVAIN_RUNS, RANDOM_SEED)

    community_rows = []
    for node in G.nodes():
        n = names_by_serial[node]
        is_stable_member = stability[node] >= LOUVAIN_CONSENSUS_THRESHOLD
        community_rows.append({
            "serial": node, "transliteration": n.transliteration, "jjk_v21": n.jjk_v21,
            "consensus_community_gamma1.0": consensus[node],
            "stability_fraction": round(stability[node], 3),
            "node_type": "Stable community member" if is_stable_member else "Boundary node",
        })

    print(f"Sensitivity runs at gamma={LOUVAIN_GAMMA_SENSITIVITY}...")
    for gamma in LOUVAIN_GAMMA_SENSITIVITY:
        cons_g, stab_g = run_louvain_consensus(G, gamma, LOUVAIN_RUNS, RANDOM_SEED)
        for row in community_rows:
            row[f"consensus_community_gamma{gamma}"] = cons_g[row["serial"]]

    with open(community_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(community_rows[0].keys()))
        writer.writeheader()
        writer.writerows(community_rows)

    n_boundary = sum(1 for r in community_rows if r["node_type"] == "Boundary node")
    n_communities = len(set(consensus.values()))
    print(f"\nWrote community table -> {community_out}")
    print(f"  {n_communities} consensus communities at gamma=1.0")
    print(f"  {n_boundary}/{len(community_rows)} nodes are boundary nodes (<{int(LOUVAIN_CONSENSUS_THRESHOLD*100)}% "
          f"stability) — report these as provisional, per §5.6")

    print(f"\nExporting graph formats...")
    try:
        nx.write_graphml(G, graphml_out)
        print(f"  {graphml_out}")
    except Exception as e:
        print(f"  ERROR writing GraphML: {type(e).__name__}: {e}")
        print(f"  This is exactly the failure mode found in the first real run (list-type")
        print(f"  edge attribute) — if you see this again, check every edge/node attribute")
        print(f"  added anywhere in this script is a plain str/int/float/bool, never a list/dict.")
        if graphml_out.exists() and graphml_out.stat().st_size == 0:
            graphml_out.unlink()
            print(f"  Removed the resulting 0-byte file rather than leaving a silent empty artifact.")

    try:
        nx.write_gexf(G, gexf_out)
        print(f"  {gexf_out}  (import into Gephi, apply ForceAtlas2 per Dossier §6.5)")
    except Exception as e:
        print(f"  ERROR writing GEXF: {type(e).__name__}: {e}")
        if gexf_out.exists() and gexf_out.stat().st_size == 0:
            gexf_out.unlink()
            print(f"  Removed the resulting 0-byte file rather than leaving a silent empty artifact.")


if __name__ == "__main__":
    main()
