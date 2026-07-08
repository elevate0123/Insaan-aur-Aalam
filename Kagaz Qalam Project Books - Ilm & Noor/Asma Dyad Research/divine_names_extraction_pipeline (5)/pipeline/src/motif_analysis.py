# -*- coding: utf-8 -*-
"""
motif_analysis.py — Network Motif Analysis, Dossier §5.7 (v2.1 addition).

Enumerates 3-node and 4-node connected sub-graphs, tests significance
against a degree-sequence-preserving null model (NOT the same null model as
null_models.py — that one permutes name assignments across VERSES; this one
permutes EDGES within the already-built GRAPH, testing a different
hypothesis: "is this local sub-structure more common than the network's own
degree sequence would predict by chance").

Per §5.7's explicit procedural constraint: this script assumes build_network.py
has ALREADY run and produced a stable graph — motif analysis runs "on top of"
that, not before it. Theological naming of motifs happens AFTER the
computational finding (in a human-written follow-up, not in this script) —
this script outputs anonymous structural findings (which nodes, what JJK
composition) and deliberately does NOT pre-label motif "types", per the
dossier's explicit warning against pre-specifying motifs to avoid
confirmation bias.

USAGE:
    python motif_analysis.py
"""

import csv
import sys
import random
import argparse
from collections import Counter
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import networkx as nx

from config import (
    GRAPH_GRAPHML_PATH, MOTIF_OUTPUT_CSV, MOTIF_NULL_PERMUTATIONS,
    MOTIF_SIGNIFICANCE_ALPHA, RANDOM_SEED,
)
from names_loader import load_divine_names


def load_graph(path):
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found — run build_network.py first with the SAME "
            f"--include-unreviewed setting you want to use here (filenames must "
            f"match between the two scripts). Motif analysis is explicitly a "
            f"second-stage step per Dossier §5.7: it runs on top of a stable, "
            f"already-validated graph, not standalone."
        )
    G = nx.read_graphml(path)
    # graphml stores node ids as strings; convert back to int to match the
    # rest of the pipeline's serial numbering
    G = nx.relabel_nodes(G, {n: int(n) for n in G.nodes()})
    return G


def enumerate_connected_subgraphs(G, size):
    """
    Returns all connected node-subsets of exactly `size` nodes, as frozensets.
    For a ~50-node, ~90-edge graph this is computationally trivial (seconds),
    per §5.7 — no special optimization needed.
    """
    found = set()
    for nodes in combinations(G.nodes(), size):
        sub = G.subgraph(nodes)
        if nx.is_connected(sub):
            found.add(frozenset(nodes))
    return found


def canonical_pattern_key(G, nodeset):
    """
    A crude but sufficient canonical key for "this shape of sub-graph":
    the sorted tuple of JJK-class labels of the nodes involved, PLUS the
    sorted tuple of edge-count between them (to distinguish a triangle from
    a path on 3 nodes, etc.). This is intentionally structural/anonymous —
    no theological name is attached here, per the dossier's anti-bias rule.
    """
    sub = G.subgraph(nodeset)
    jjk_labels = tuple(sorted(sub.nodes[n].get("jjk_v21", "?") for n in nodeset))
    edge_count = sub.number_of_edges()
    max_possible_edges = len(nodeset) * (len(nodeset) - 1) // 2
    shape = "complete" if edge_count == max_possible_edges else f"{edge_count}edges"
    return (jjk_labels, shape)


def degree_preserving_randomize(G, seed):
    """
    Returns a new graph with the same degree sequence as G but randomized
    connections, using NetworkX's double_edge_swap. This IS the null model
    for motif significance — distinct from null_models.py's verse-level
    permutation.
    """
    G2 = G.copy()
    n_edges = G2.number_of_edges()
    # nswap heuristic: enough swaps to thoroughly randomize without
    # infinite-looping on a small/dense graph; max_tries gives up gracefully
    try:
        nx.double_edge_swap(G2, nswap=max(n_edges * 3, 50), max_tries=n_edges * 50, seed=seed)
    except nx.NetworkXError:
        pass  # small/dense graphs sometimes can't fully randomize; partial swap is still valid
    return G2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-unreviewed", action="store_true",
                         help="Load the unfiltered graph (must match how build_network.py was run).")
    args = parser.parse_args()
    suffix = "_UNREVIEWED_INCLUDED" if args.include_unreviewed else ""
    graph_path = GRAPH_GRAPHML_PATH.with_name(GRAPH_GRAPHML_PATH.stem + suffix + GRAPH_GRAPHML_PATH.suffix)
    motif_out = MOTIF_OUTPUT_CSV.with_name(MOTIF_OUTPUT_CSV.stem + suffix + MOTIF_OUTPUT_CSV.suffix)

    print("Loading graph from build_network.py output...")
    G = load_graph(graph_path)
    print(f"  {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.\n")

    all_patterns_observed = {}  # size -> Counter of canonical_pattern_key -> count
    all_subgraphs_by_size = {}

    for size in (3, 4):
        print(f"Enumerating connected {size}-node sub-graphs...")
        subs = enumerate_connected_subgraphs(G, size)
        all_subgraphs_by_size[size] = subs
        pattern_counts = Counter(canonical_pattern_key(G, s) for s in subs)
        all_patterns_observed[size] = pattern_counts
        print(f"  {len(subs)} connected {size}-node sub-graphs, {len(pattern_counts)} distinct JJK-composition patterns.")

    print(f"\nBuilding degree-sequence-preserving null distribution ({MOTIF_NULL_PERMUTATIONS} permutations)...")
    print("This is the slow step. Progress every 10%.")

    null_pattern_counts = {3: Counter(), 4: Counter()}
    # We track, for each permutation, the count of each OBSERVED pattern
    # (we only need null-distribution values for patterns we actually saw,
    # per standard motif-significance practice)
    null_distributions = {3: {k: [] for k in all_patterns_observed[3]},
                           4: {k: [] for k in all_patterns_observed[4]}}

    rng = random.Random(RANDOM_SEED)
    for p in range(MOTIF_NULL_PERMUTATIONS):
        seed = rng.randint(0, 2**31 - 1)
        G_null = degree_preserving_randomize(G, seed)
        for size in (3, 4):
            subs_null = enumerate_connected_subgraphs(G_null, size)
            counts_null = Counter(canonical_pattern_key(G_null, s) for s in subs_null)
            for pattern in null_distributions[size]:
                null_distributions[size][pattern].append(counts_null.get(pattern, 0))
        if (p + 1) % max(1, MOTIF_NULL_PERMUTATIONS // 10) == 0:
            print(f"  ...{p+1}/{MOTIF_NULL_PERMUTATIONS}")

    results = []
    for size in (3, 4):
        for pattern, observed_count in all_patterns_observed[size].items():
            dist = null_distributions[size][pattern]
            mean = sum(dist) / len(dist)
            var = sum((x - mean) ** 2 for x in dist) / len(dist)
            std = var ** 0.5
            z = (observed_count - mean) / std if std > 0 else float("inf")
            p_value = sum(1 for x in dist if x >= observed_count) / len(dist)
            jjk_labels, shape = pattern
            results.append({
                "subgraph_size": size,
                "jjk_composition": " + ".join(jjk_labels),
                "shape": shape,
                "observed_count": observed_count,
                "null_mean": round(mean, 4),
                "null_std": round(std, 4),
                "z_score": round(z, 4) if z != float("inf") else "inf",
                "p_value": round(p_value, 6),
                "significant": p_value < MOTIF_SIGNIFICANCE_ALPHA,
            })

    results.sort(key=lambda r: (r["p_value"], -r["observed_count"]))

    motif_out.parent.mkdir(parents=True, exist_ok=True)
    with open(motif_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    n_sig = sum(1 for r in results if r["significant"])
    print(f"\nWrote {len(results)} JJK-composition patterns -> {motif_out}")
    print(f"  {n_sig}/{len(results)} significant at p<{MOTIF_SIGNIFICANCE_ALPHA}")
    print("\nIMPORTANT (§5.7): this output is deliberately ANONYMOUS — JJK composition and shape")
    print("only, no theological motif name attached. Theological naming/interpretation of any")
    print("significant pattern happens AFTER seeing this table, by a human, not by this script.")
    print("Do not use the word 'algorithm' when describing these findings in Papers 1 or 3 —")
    print("frame as 'statistically over-represented structural tendency' per §5.7 publication note.")


if __name__ == "__main__":
    main()
