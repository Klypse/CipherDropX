# """
# CipherDropX – l_regex.py
# ========================
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
# *   Purpose        : Provide static regex patterns for legacy deciphering
# *   Usage context  : Used exclusively by l_parser in legacy mode
# *   Design choice  : All patterns are concise, single-line expressions
# *   Execution core : cipherdropx.executor receives the resolved mappings
#
# Module description
# ------------------
# This module defines compact, one-line regular expression templates
# specifically crafted for legacy YouTube player builds where decipher logic
# is not obfuscated via H-table indirection.
#
# These legacy templates detect transformation helpers (e.g., splice,
# reverse, swap) directly based on their string content and structural
# cues rather than dynamic lookup logic.
#
# Unlike modern parsing, there is no need to anchor patterns to H-table
# indices. These templates are static and hard-coded, but still resilient
# to minor format shifts in older player versions.
#
# This file is only used during the legacy fallback path triggered by
# parser.py when H-table-based decoding is unavailable.
#
# Guarantee
# ---------
# All regex templates are constructed without line breaks or multiline flags,
# ensuring compatibility with minified or compact legacy scripts.
#
# This header augments documentation only; executable code remains unchanged.
#
# Feel free to open issues or pull requests at the GitHub repository above
# if you have improvement ideas.
# """

import re
SPLICE  = re.compile(r'(\w+):function\(\w+,\w+\){\w+\.splice\(0,\w+\)}')
REVERSE = re.compile(r'(\w+):function\(\w+\){\w+\.reverse\(\)}')
SWAP    = re.compile(r'(\w+):function\(\w+,\w+\){var \w+=\w+\[0\];\w+\[0\]=\w+\[\w+%\w+\.length\];\w+\[\w+%\w+\.length\]=\w+}')
CHALL   = re.compile(r'function\(\w+\){\w+=\w+\.split\(""\);((?:\w+\.\w+\(\w+,\d+\);)*)return \w+\.join\(""\)};', re.DOTALL)
CODE    = re.compile(r'\w+\.(\w+)\(\w+,(\d+)\);')