# -*- coding: utf-8 -*-
"""
quran_source.py — Parses the Tanzil.net Qur'an XML corpus.

You must download the XML yourself (see README.md Step 2) — this pipeline
does not fetch it automatically. Expected format is Tanzil's standard
<quran><sura index="1" name="..."><aya index="1" text="..."/>...
"""

from dataclasses import dataclass
from typing import List
from lxml import etree

from config import TANZIL_XML_PATH

# Meccan/Medinan classification is NOT in the plain Tanzil text XML — Tanzil
# distributes it separately as sura-info metadata. If you need it (Papers 1
# and 3 both do, per the dossier), download quran-data.xml alongside the
# main text file and merge in load_meccan_medinan() below. Left as a TODO
# stub rather than guessed, per the project's zero-silent-assumption rule.
MECCAN_MEDINAN_XML_PATH = TANZIL_XML_PATH.parent / "quran-data.xml"


@dataclass
class Verse:
    surah_number: int
    surah_name: str
    ayah_number: int
    text: str
    meccan_medinan: str = "UNKNOWN"  # filled in by load_meccan_medinan() if available


def load_verses(path=TANZIL_XML_PATH) -> List[Verse]:
    if not path.exists():
        raise FileNotFoundError(
            f"Tanzil XML not found at {path}.\n"
            f"Download it from https://tanzil.net/download/ (choose 'Simple "
            f"Enhanced' or 'Uthmani', XML format) and place it at this path, "
            f"or update TANZIL_XML_PATH in config.py. See README.md Step 2."
        )

    tree = etree.parse(str(path))
    verses = []
    for sura in tree.findall(".//sura"):
        surah_number = int(sura.get("index"))
        surah_name = sura.get("name", "")
        for aya in sura.findall("aya"):
            verses.append(
                Verse(
                    surah_number=surah_number,
                    surah_name=surah_name,
                    ayah_number=int(aya.get("index")),
                    text=aya.get("text", ""),
                )
            )
    if not verses:
        raise ValueError(
            f"Parsed {path} but found zero verses — check the XML structure "
            f"matches Tanzil's standard <sura><aya text='...'/></sura> format. "
            f"If you downloaded a different XML schema, adjust the XPath "
            f"queries in this function."
        )
    return verses


def load_meccan_medinan(verses: List[Verse], path=MECCAN_MEDINAN_XML_PATH) -> List[Verse]:
    """
    Optional enrichment step. If quran-data.xml is present, tags each verse's
    surah as Meccan or Medinan. If absent, leaves 'UNKNOWN' and prints a
    warning rather than guessing — Papers 1 and 3 need this to be correct,
    not approximated.
    """
    if not path.exists():
        print(
            f"[quran_source] WARNING: {path} not found — meccan_medinan left "
            f"as 'UNKNOWN' for all verses. Download quran-data.xml from "
            f"tanzil.net if you need period classification (required for "
            f"Papers 1 and 3's Meccan/Medinan analysis)."
        )
        return verses

    tree = etree.parse(str(path))
    period_by_surah = {}
    for sura in tree.findall(".//sura"):
        idx = int(sura.get("index"))
        period_by_surah[idx] = sura.get("type", "UNKNOWN").capitalize()

    for v in verses:
        v.meccan_medinan = period_by_surah.get(v.surah_number, "UNKNOWN")
    return verses
