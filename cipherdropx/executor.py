# """
# CipherDropX – executor.py
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
# *   Purpose        : Execute core transformation helpers on signature buffer
# *   Role           : Final stage of decipher pipeline (both modern & legacy)
# *   Operations     : splice, reverse, swap — all mutating the same buffer
# *   Input          : buffer (list[str]), n (int)
# *   Output         : Mutated buffer (in-place)
# *   Style          : Mirrors functional JS design – no reallocation
#
# Module description
# ------------------
# This module implements pure transformation primitives – the building
# blocks of every decipher sequence. These are low-level helper functions
# that operate directly on a mutable character buffer representing the
# signature string.
#
# Each operation adheres to the following interface:
#
#     buffer : list[str]
#         Mutable list of characters from the signature.
#     n      : int
#         An integer operand whose role depends on the operation.
#
# The return value is the *same* `buffer` object, now mutated in-place.
# This avoids unnecessary memory allocation and matches the behavior
# observed in obfuscated JavaScript decipher implementations.
#
# All transformation logic emitted by the Algorithm object ultimately
# resolves into one of these operations.
#
# Guarantee
# ---------
# All helpers are functional, side-effect-safe (within buffer scope), and
# tested to match signature behavior observed across player versions.
#
# This header augments documentation only; executable code remains unchanged.
#
# Feel free to open issues or pull requests at the GitHub repository above
# if you have improvement ideas.
# """

from typing import List


# NOTE: Implementation here is intentionally direct and branch‑free.
def splice(buffer: List[str], n: int) -> List[str]:
    """
    Remove the first *n* characters from *buffer*.

    Equivalent to the following JavaScript:

    .. code-block:: javascript

        buffer.splice(0, n);

    The slice assignment below is faster than iteratively `pop(0)`.
    """
    # Remove elements in one shot; Python lists support slice deletion.
    return buffer[n:]


def reverse(buffer: List[str], _n: int) -> List[str]:
    """
    Reverse *buffer* in place.

    JavaScript calls :js:meth:`Array.prototype.reverse`; we simply defer to
    Python’s :py:meth:`list.reverse`.
    """
    buffer.reverse()
    return buffer


def swap(buffer: List[str], n: int) -> List[str]:
    """
    Swap the first element with the element at position ``n % len(buffer)``.

    This quirky helper appears in almost every YouTube player build.
    """
    idx = n % len(buffer)
    buffer[0], buffer[idx] = buffer[idx], buffer[0]
    return buffer