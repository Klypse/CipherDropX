# """
# CipherDropX – h_parser.py
# =========================
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
# *   Purpose        : Extract H‑table used in obfuscated method access
# *   Entry point    : First step in the modern deciphering path
# *   Output         : List of method names (e.g., "split", "splice", ...)
# *   Usage          : Passed to regex templates for transformation detection
# *   Execution core : Enables parser.py to detect helper mappings by index
#
# Module description
# ------------------
# This module is responsible for extracting the H-table — a lookup array
# encoded as a single giant string in YouTube’s base.js. This string,
# typically split using a custom delimiter (e.g., `{`), contains method names
# like "split", "splice", "reverse", and "join", which are later accessed by
# numeric indices (e.g., H[30]).
#
# Because YouTube obfuscates all method references in recent player builds,
# recovering the H-table is a prerequisite for detecting transformation
# helpers in the decipher routine.
#
# Once extracted, the H-table is passed into regex.py, which generates
# regexes using its method-to-index mappings, enabling precise function
# detection despite heavy obfuscation.
#
# Guarantee
# ---------
# The extraction method is robust to variation in delimiters and naming;
# it is designed to match the structural pattern of obfuscated player builds.
#
# This header augments documentation only; executable code remains unchanged.
#
# Feel free to open issues or pull requests at the GitHub repository above
# if you have improvement ideas.
# """

import re
from typing import Dict, List, Tuple

_PATTERN = re.compile(
    r'var\s+(\w+)\s*=\s*"([^"]{400,}?(?:split|splice|join|reverse|length)[^"]*)"\.split\("([^"]+)"\)',
    re.DOTALL,
)

def extract_method_table(js: str) -> Tuple[str, Dict[int, str], Dict[str, int]]:
    """
    Return ``(varname, forward_table, reverse_table)``.

    Raises
    ------
    ValueError
        If the pattern cannot be located – caller should abort gracefully.
    """
    m = _PATTERN.search(js)
    if not m:
        raise ValueError("Unable to find H‑table in the supplied base.js")

    var, raw, delim = m.groups()
    array: List[str] = raw.split(delim)
    forward = {i: v for i, v in enumerate(array)}
    reverse = {v: i for i, v in forward.items()}
    return var, forward, reverse