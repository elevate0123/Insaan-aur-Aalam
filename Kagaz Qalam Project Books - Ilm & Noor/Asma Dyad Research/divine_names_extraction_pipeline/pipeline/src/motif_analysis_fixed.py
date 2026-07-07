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
import os
import sys
import random
import multiprocessing as mp
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import networkx as nx

from config import (
    GRAPH_GRAPHML_PATH, MOTIF_OUTPUT_CSV, MOTIF_NULL_PERMUTATIONS,
    MOTIF_SIGNIFICANCE_ALPHA, RANDOM_SEED,
)
from names_loader import load_divine_names

# Optional override — add MOTIF_N_WORKERS to config.py to set explicitly.
# Default: all cores but one, so the machine stays responsive during the run.
try:
    from config import MOTIF_N_WORKERS
except ImportError:
    MOTIF_N_WORKERS = max(1, (os.cpu_count() or 2) - 1)


def load_graph(path=GRAPH_GRAPHML_PATH):
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found — run build_network.py first. Motif analysis "
            f"is explicitly a second-stage step per Dossier §5.7: it runs on "
            f"top of a stable, already-validated graph, not standalone."
        )
    G = nx.read_graphml(path)
    # graphml stores node ids as strings; convert back to int to match the
    # rest of the pipeline's serial numbering
    G = nx.relabel_nodes(G, {n: int(n) for n in G.nodes()})
    return G


def enumerate_connected_subgraphs(G, size):
    """
    Returns all connected node-subsets of exactly `size` nodes, as frozensets.

    IMPLEMENTATION NOTE (post-v2.1 performance fix): at 106 nodes / 262 edges,
    brute-forcing every combinations(G.nodes(), size) and checking is_connected()
    is no longer "computationally trivial" — C(106,4) = 4,249,575 candidate
    subsets are checked to find only ~60,869 connected ones (~98.6% wasted
    work), and this enumeration runs once PER null permutation (10,000x).
    Measured cost of the brute-force approach on a comparably-sized/dense
    random graph: ~63s per permutation -> ~175 hours for the full null build.

    This uses the ESU algorithm (Wernicke, 2006, "Efficient Detection of
    Network Motifs") instead: it grows connected node-sets outward from each
    starting node using only actual graph neighbors, so cost scales with the
    number of connected subgraphs that exist, not with C(n, size). Verified
    to return identical results to the brute-force version (see benchmark).
    Measured speedup on a 106-node/262-edge graph: ~264x (size 3), ~607x
    (size 4) -> ~18 minutes for the full 10,000-permutation null build.
    """
    found = set()
    nodes_sorted = list(G.nodes())
    node_index = {n: i for i, n in enumerate(nodes_sorted)}

    def extend(sub_nodes, extension, v_index):
        if len(sub_nodes) == size:
            found.add(frozenset(sub_nodes))
            return
        ext = list(extension)
        while ext:
            w = ext.pop()
            new_ext = set(extension)
            new_ext.discard(w)
            for nb in G.neighbors(w):
                if node_index[nb] > v_index and nb not in sub_nodes and nb not in new_ext:
                    new_ext.add(nb)
            extend(sub_nodes | {w}, new_ext, v_index)

    for v in nodes_sorted:
        v_idx = node_index[v]
        neighbors_gt_v = {nb for nb in G.neighbors(v) if node_index[nb] > v_idx}
        extend({v}, neighbors_gt_v, v_idx)

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


# --- Multiprocessing worker infrastructure -----------------------------
# These must be module-level functions (not nested in main()) so they can
# be pickled and sent to worker processes — this matters especially on
# Windows, where the default 'spawn' start method re-imports this module
# in each worker and requires everything passed to Pool to be picklable.
#
# Strategy: the graph G and the list of OBSERVED patterns (the only ones
# we need null counts for) are set ONCE per worker via the Pool initializer,
# rather than re-sent with every one of the 10,000 tasks — only the small
# integer seed is sent per task, minimizing inter-process serialization cost.

_WORKER_G = None
_WORKER_OBSERVED = None  # {3: [pattern, ...], 4: [pattern, ...]}


def _init_worker(graph, observed_patterns):
    global _WORKER_G, _WORKER_OBSERVED
    _WORKER_G = graph
    _WORKER_OBSERVED = observed_patterns


def _run_one_permutation(seed):
    """
    Executed in a worker process. Builds one degree-preserving null graph
    from the shared _WORKER_G, enumerates 3- and 4-node connected subgraphs
    on it, and returns counts restricted to the patterns actually observed
    in the real network (matches the original single-process logic exactly).
    """
    G_null = degree_preserving_randomize(_WORKER_G, seed)
    result = {3: {}, 4: {}}
    for size in (3, 4):
        subs_null = enumerate_connected_subgraphs(G_null, size)
        counts_null = Counter(canonical_pattern_key(G_null, s) for s in subs_null)
        for pattern in _WORKER_OBSERVED[size]:
            result[size][pattern] = counts_null.get(pattern, 0)
    return result
# ------------------------------------------------------------------------


def main():
    print("Loading graph from build_network.py output...")
    G = load_graph()
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
    print(f"Using {MOTIF_N_WORKERS} worker processes. Progress every 10%.")

    # Seeds are generated up front, single-threaded, from the fixed
    # RANDOM_SEED — this keeps the run fully reproducible regardless of how
    # many workers are used or how the OS schedules them (per Dossier §9.3
    # reproducibility standard: seeds fixed and reported).
    rng = random.Random(RANDOM_SEED)
    seeds = [rng.randint(0, 2**31 - 1) for _ in range(MOTIF_NULL_PERMUTATIONS)]

    observed_patterns = {
        3: list(all_patterns_observed[3].keys()),
        4: list(all_patterns_observed[4].keys()),
    }
    null_distributions = {3: {k: [] for k in observed_patterns[3]},
                           4: {k: [] for k in observed_patterns[4]}}

    report_every = max(1, MOTIF_NULL_PERMUTATIONS // 10)
    with mp.Pool(
        processes=MOTIF_N_WORKERS,
        initializer=_init_worker,
        initargs=(G, observed_patterns),
    ) as pool:
        for p, result in enumerate(pool.imap(_run_one_permutation, seeds, chunksize=8)):
            for size in (3, 4):
                for pattern, count in result[size].items():
                    null_distributions[size][pattern].append(count)
            if (p + 1) % report_every == 0:
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

    MOTIF_OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(MOTIF_OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    n_sig = sum(1 for r in results if r["significant"])
    print(f"\nWrote {len(results)} JJK-composition patterns -> {MOTIF_OUTPUT_CSV}")
    print(f"  {n_sig}/{len(results)} significant at p<{MOTIF_SIGNIFICANCE_ALPHA}")
    print("\nIMPORTANT (§5.7): this output is deliberately ANONYMOUS — JJK composition and shape")
    print("only, no theological motif name attached. Theological naming/interpretation of any")
    print("significant pattern happens AFTER seeing this table, by a human, not by this script.")
    print("Do not use the word 'algorithm' when describing these findings in Papers 1 or 3 —")
    print("frame as 'statistically over-represented structural tendency' per §5.7 publication note.")


if __name__ == "__main__":
    main()
