# """
# CipherDropX – __init__.py
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
# *   Entry point    : cipherdropx package root (__init__.py)
# *   Public API     : CipherDropX class (from core.py)
# *   Design goal    : Provide parsing + execution with zero network coupling
# *   Usage style    : Lightweight, forward-compatible interface
# *   Scope          : Omits all I/O — input is raw base.js text
#
# Package description
# -------------------
# This file defines the public interface of the CipherDropX package.
# It provides a network-free, single-class interface for decoding YouTube's
# obfuscated signature logic from player JavaScript files (`base.js`).
#
# The only exported artefact is:
#
#     :class:`cipherdropx.core.CipherDropX`
#
# Keeping the surface minimal makes long-term maintenance and evolution
# significantly easier — clients need not track internal refactors.
#
# Typical usage
# -------------
# >>> from cipherdropx import CipherDropX
# >>> cdx = CipherDropX(base_js_text)
# >>> algorithm = cdx.get_algorithm()
# >>> cdx.update(algorithm)
# >>> cdx.run(raw_sig)
# >>> clean_sig = cdx.signature
#
# Behind the scenes
# -----------------
# *   h_parser      – extracts the H-table string (method lookup array)
# *   regex / l_regex – builds regexes for transformation detection
# *   parser / l_parser – maps helpers to ordered operations
# *   algorithm     – executes those operations via executor
#
# Guarantee
# ---------
# All internal modules are fully decoupled from network access. This design
# ensures that CipherDropX can be used in sandboxed, audited, or pre-fetched
# environments with deterministic behavior.
#
# This header augments documentation only; executable code remains unchanged.
#
# Feel free to open issues or pull requests at the GitHub repository above
# if you have improvement ideas.
# """

from .core import CipherDropX

__all__: list[str] = ["CipherDropX"]