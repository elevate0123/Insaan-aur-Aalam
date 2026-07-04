# -*- coding: utf-8 -*-
"""
names_loader.py — Loads and normalizes the master divine-names list for
matching against morphologically-analyzed Qur'anic tokens.
"""

import csv
from dataclasses import dataclass
from typing import Dict, List

from config import DIVINE_NAMES_CSV
from morphology import normalize_for_matching


@dataclass
class DivineName:
    serial: int
    arabic: str
    transliteration: str
    english: str
    root: str
    tier: str
    jjk_legacy: str
    jjk_v21: str
    homonym_flag: bool
    include_in_network: bool
    normalized_arabic: str  # precomputed, used for matching


def load_divine_names(path=DIVINE_NAMES_CSV) -> List[DivineName]:
    names = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            arabic = row["A2_Arabic_Name"].strip()
            names.append(
                DivineName(
                    serial=int(row["A1_Serial_Number"]),
                    arabic=arabic,
                    transliteration=row["A3_Transliteration_ALA_LC"],
                    english=row["A4_English_Meaning"],
                    root=row["A5_Arabic_Root"],
                    tier=row["A7_Tier"],
                    jjk_legacy=row["D1_Jalal_Jamal_Kamal"],
                    jjk_v21=row["H1_JJK_5Class_v2_1"],
                    homonym_flag=(row["C4_Homonym_Flag"].strip().lower() == "yes"),
                    include_in_network=(row["F1_Include_in_Network"].strip().lower() == "yes"),
                    normalized_arabic=normalize_for_matching(arabic),
                )
            )
    return names


def build_lemma_index(names: List[DivineName]) -> Dict[str, List[DivineName]]:
    """
    Maps a normalized lemma string -> list of DivineName entries that share
    it. A list (not a single entry) because e.g. Al-Wāḥid / Al-Aḥad share a
    root and some transliterated forms can collide after normalization —
    the extraction script must NOT silently pick one; ambiguous matches are
    routed to HITL review (see extract_dyads.py MATCH_AMBIGUOUS handling).

    IMPORTANT — a note on Tier 1 vs Tier 3: this loader includes ALL rows in
    divine_names_master.csv, including the Tier 3 documented exclusions
    (Al-Sittīr, Al-Jamīl). This is deliberate: if either happens to occur in
    the Qur'anic text, we want to KNOW, not silently miss it — but matches
    against Tier 3 names are tagged and excluded from the primary dyad
    dataset by default (see extract_dyads.py TIER3_POLICY).
    """
    index: Dict[str, List[DivineName]] = {}
    for n in names:
        index.setdefault(n.normalized_arabic, []).append(n)
    return index
