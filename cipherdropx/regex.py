# """
# CipherDropX – regex.py
# =======================
#
# This module is part of CipherDropX, a Python implementation that
# deciphers the streaming signatures used by YouTube (both modern and
# legacy player builds).
#
# Repository : https://github.com/Klypse/CipherDropX
# Author     : Klypse (https://github.com/Klypse)
# License    : Apache-2.0
# Generated  : 2025-06-24
#
# Guidelines for readers
# ----------------------
# 1.  The code below remains bit-for-bit identical to the authoritative
#     source committed by the maintainer. Only documentation has been added.
# 2.  No Markdown emphasis markers are used in this docstring to keep plain
#     text rendering consistent on GitHub.
# 3.  Detailed design discussions live in the project wiki; this header
#     provides a concise overview so you can jump into the source with
#     confidence.
#
# High-level overview
# -------------------
# *   Purpose        : Dynamically generate regex templates for decipher logic
# *   Inputs         : Method keywords + H-table variable name
# *   Output         : 4 compiled regex objects – SPLICE, REVERSE, SWAP, CHALL
# *   Context        : Used in modern path – H-table → regex → algorithm
# *   Design note    : All regex templates must match minified JS precisely
#
# Module description
# ------------------
# This module is the heart of the parser: it dynamically builds four
# regular-expression templates capable of locating obfuscated helper
# functions inside YouTube's minified base.js.
#
# Motivation
# ----------
# YouTube mutates player code frequently, but the structure of decipher logic
# remains consistent:
#
# * A giant lookup array (traditionally named H) stores method names like
#   "split", "splice", "reverse", "join" — split using an arbitrary delimiter.
# * Helper functions (splice, reverse, swap) live in an object with short,
#   pseudo-random keys.
# * A challenge function (CHALL) chains the helpers to transform the signature.
#
# Since property names change frequently, we avoid hard-coding and instead
# use the stable H-table index (e.g., H[30]) as a consistent anchor.
#
# How it works
# ------------
# 1. _piece(): Converts method keyword + H-table variable into a concrete
#    expression like H[30], injected into regex patterns via $H.
# 2. build_patterns(): Constructs and compiles final regexes. Returns a dict:
#
#        {"SPLICE": Pattern | None, "REVERSE": Pattern | None,
#         "SWAP": Pattern | None,   "CHALL": Pattern | None}
#
#    Entries may be None if a transformation is not present in the current
#    player (rare; failure is graceful).
#
# Guarantee
# ---------
# No whitespace or line breaks are introduced in any regex pattern — minified
# base.js files are extremely compact, and our patterns must match exactly.
#
# Feel free to open issues or pull requests at the GitHub repository above
# if you have improvement ideas.
# """

from __future__ import annotations
import re
from typing import Dict, Optional


# ------------------------------------------------------------------ #
# Helper: insert correct H‑table index into template
def _piece(name: str, var: str, index: Dict[str, int]) -> str:
    """
    Return the literal string `"f'{var}[index]'"` used inside
    the regex template.  We keep this small and fast because it
    will be called for every helper keyword (≤ 5 per build).
    """
    return rf"{var}\[{index[name]}\]"


# ------------------------------------------------------------------ #
# Public factory: generate compiled regex objects
def build_patterns(var: str, index: Dict[str, int]) -> Dict[str, Optional[re.Pattern]]:
    """
    Build and **compile** all regex patterns needed to identify
    helper functions in *base.js*.

    Parameters
    ----------
    var
        Name of the JavaScript variable holding the H‑table.
    index
        Reverse map {method_name → numeric_index}.

    Returns
    -------
    Dict[str, re.Pattern | None]
        Compiled patterns, with ``None`` for helpers absent in
        the current build.
    """
    patt: Dict[str, Optional[re.Pattern]] = {k: None for k in ("CHALL","SPLICE","REVERSE","SWAP")}

    templates = {
        "SPLICE": r"(\w+):function\(\w+,\w+\)\{\w+\[$H\]\(0,\w+\)\}",
        "REVERSE": r"(\w+):function\(\w+\)\{\w+\[$H\]\(\)\}",
        "SWAP": r"(\w+):function\(\w+,\w+\)\{var \w+=\w+\[0\];\w+\[0\]=\w+\[\w+%\w+\[$H\]\];\w+\[\w+%\w+\[$H\]\]=\w+\}",
    }
    for label, template in templates.items():
        key = label.lower() if label != "SWAP" else "length"
        if key not in index:
            continue
        piece = _piece(key, var, index)
        patt[label] = re.compile(template.replace("$H", piece), re.DOTALL)

    if "split" in index and "join" in index:
        split_p = _piece("split", var, index)
        join_p = _piece("join", var, index)
        chall = (
            rf"function\(\w+\)\{{\w+=\w+\[{split_p}\]\({var}\[\d+\]\);"
            rf"((?:\w+\[{var}\[\d+\]\]\(\w+,\d+\);)*)"
            rf"return \w+\[{join_p}\]\({var}\[\d+\]\)\}}"
        )
        patt["CHALL"] = re.compile(chall, re.DOTALL)
    return patt