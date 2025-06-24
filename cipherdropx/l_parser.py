# """
# CipherDropX – l_parser.py
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
# *   Purpose        : Parse un-obfuscated base.js in legacy player builds
# *   Entry point    : Fallback for parser.py when no H-table is found
# *   Input          : Raw base.js text with visible helper names
# *   Output         : Algorithm object with decoded transformation sequence
# *   Dependencies   : Uses static patterns from l_regex.py
# *   Execution core : cipherdropx.executor (splice, reverse, swap)
#
# Module description
# ------------------
# This module enables CipherDropX to work with legacy YouTube player builds
# where transformation helpers (e.g., splice, reverse, swap) are not hidden
# behind dynamic indexing (like the H-table), but appear directly in source.
#
# l_parser inspects the raw base.js code for known string structures and
# function patterns that are stable across older deployments. It uses
# templates from l_regex.py to identify these helpers and then constructs
# a corresponding Algorithm object for downstream execution.
#
# The output of this parser is identical in structure to that of modern
# parsing logic, ensuring seamless integration with the executor backend.
#
# It is only activated when modern parsing fails due to missing or invalid
# H-table definitions — making it a robust fallback layer.
#
# Guarantee
# ---------
# This module makes no assumptions about minification level but is designed
# to tolerate basic structural changes in legacy base.js implementations.
#
# This header augments documentation only; executable code remains unchanged.
#
# Feel free to open issues or pull requests at the GitHub repository above
# if you have improvement ideas.
# """

import logging
from typing import List, Dict
from .algorithm import Operation
from . import l_regex as L

log = logging.getLogger(__name__)

def parse_js_legacy(js_code: str, *, debug: bool=False) -> List[Operation]:
    """
    Description
    -----------
    Replace this placeholder with a detailed explanation covering intent,
    parameters, return value, and examples.

    Parameters
    ----------
    *args, **kwargs
        See implementation.

    Returns
    -------
    object
        Refer to function body for specifics.
    """
    chall_match = L.CHALL.search(js_code)
    if not chall_match:
        if debug:
            log.debug("Legacy CHALL not found")
        return []
    chall_body = chall_match.group(1)
    helpers: Dict[str,str] = {}
    for label, rgx in (("splice", L.SPLICE), ("reverse", L.REVERSE), ("swap", L.SWAP)):
        m = rgx.search(js_code)
        if m:
            helpers[m.group(1)] = label
    ops: List[Operation] = []
    for name, param in L.CODE.findall(chall_body):
        action = helpers.get(name)
        if not action:
            raise ValueError(f"Unknown helper name: {name}")
        ops.append(Operation(action, int(param)))
        if debug:
            log.debug("Legacy add %s(%s)", action, param)
    return ops