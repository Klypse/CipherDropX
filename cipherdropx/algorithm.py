# """
# CipherDropX – algorithm.py
# ==========================
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
# *   Purpose        : Store and replay ordered signature transformation steps
# *   Core class     : Algorithm — precompiled operation sequence executor
# *   Input          : Signature string (str)
# *   Output         : Deciphered string (str)
# *   Operates on    : List of Operation objects (splice, reverse, swap)
# *   Calls into     : cipherdropx.executor for low-level mutations
#
# Module description
# ------------------
# This module defines the Algorithm class — a structured executor that
# represents a compiled sequence of transformation steps extracted from
# YouTube's player JavaScript.
#
# Internally, Algorithm stores an ordered list of Operation objects,
# each representing a single signature mutation (e.g., splice, reverse, swap).
# These are gathered by parser.py (or l_parser.py), based on either dynamic
# or static decoding strategies.
#
# The `run()` method (and its __call__ alias) applies the entire sequence
# to a given input string, mutating a character buffer in-place.
#
# This design avoids reflection, `eval`, or dynamic dispatch. All decoding
# logic is reduced to pure, deterministic actions.
#
# Guarantee
# ---------
# Algorithm provides a stable, testable execution layer between parsing
# and transformation. Output is consistent across equivalent sequences,
# regardless of source obfuscation.
#
# This header augments documentation only; executable code remains unchanged.
#
# Feel free to open issues or pull requests at the GitHub repository above
# if you have improvement ideas.
# """

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, List
from . import executor


@dataclass(slots=True, frozen=True)
class Operation:
    """
    Lightweight, immutable value object.

    Parameters
    ----------
    action : str
        Name of the primitive (``splice`` / ``reverse`` / ``swap``).
    arg : int
        Integer operand whose semantics depend on *action*.
    """
    action: str
    arg: int


# Map string → concrete function to avoid expensive ``getattr`` at runtime.
DISPATCH_TABLE: Dict[str, Callable[[List[str], int], List[str]]] = {
    "splice": executor.splice,
    "reverse": executor.reverse,
    "swap": executor.swap,
}


class Algorithm:
    """
    Callable wrapper around a sequence of operations.

    >>> algo = Algorithm([Operation("reverse", 0), Operation("swap", 3)])
    >>> algo("abcd")
    'dbca'
    """

    def __init__(self, steps: List[Operation]):
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
        self._steps = steps  # store as provided; they’re immutable dataclasses

    # Core entrypoint ----------------------------------------------------
    def run(self, signature: str) -> str:
        """
        Apply all stored operations to *signature* and return the result.
        """
        buffer: List[str] = list(signature)  # convert once
        for op in self._steps:
            fn = DISPATCH_TABLE.get(op.action)
            if fn is None:
                raise ValueError(f"Unsupported action '{op.action}'.")
            buffer = fn(buffer, op.arg)
        return "".join(buffer)

    __call__ = run  # sugar – allows ``algo(sig)``


    # Dunder helpers -----------------------------------------------------
    def __repr__(self) -> str:  # pragma: no cover
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
        return f"Algorithm(steps={self._steps!r})"