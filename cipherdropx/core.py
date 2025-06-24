# """
# CipherDropX – core.py
# =====================
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
# *   Purpose        : High-level façade bundling all decipher stages
# *   Entry point    : Exposed CipherDropX class for external use
# *   Workflow       : base.js → parser (modern or legacy) → executor
# *   Internals      : Selects parsing strategy, runs Algorithm, returns result
# *   API surface    : Intentionally slim – stable external interface
#
# Module description
# ------------------
# This module serves as the central façade for the entire CipherDropX
# pipeline. It coordinates all steps of the deciphering process, including:
#
# * H‑table extraction (h_parser)
# * Regex pattern generation (regex / l_regex)
# * Operation parsing (parser / l_parser)
# * Signature execution (executor)
#
# The public interface is intentionally minimal, exposing only the top-level
# `CipherDropX` class. This design ensures forward compatibility even as
# internal parsing logic evolves to match future YouTube player variants.
#
# This entry point automatically chooses between modern and legacy strategies
# depending on the structure of the given base.js source, ensuring seamless
# decoding regardless of rollout changes.
#
# Guarantee
# ---------
# This module abstracts all complexity behind a single API call, enabling
# consumers to use the decipherer without needing to understand internal
# structures or parsing heuristics.
#
# This header augments documentation only; executable code remains unchanged.
#
# Feel free to open issues or pull requests at the GitHub repository above
# if you have improvement ideas.
# """

import logging
from typing import Optional
from .h_parser import extract_method_table
from .parser import parse_js
from .l_parser import parse_js_legacy
from .algorithm import Algorithm

log = logging.getLogger(__name__)

class CipherDropX:
    """
    Thin wrapper used by client code.

    Parameters
    ----------
    js : str
        Raw contents of YouTube’s *base.js*.
    debug : bool, optional
        If *True*, emits verbose `logging.DEBUG` messages.
    """

    def __init__(self, js: str, *, debug: bool=False):
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
        self._debug = debug
        self._sig: Optional[str] = None
        self._algo = self._build(js)

    def _build(self, js: str) -> Algorithm:
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
        try:
             var, fwd, rev = extract_method_table(js)
             ops = parse_js(js, var, fwd, rev, debug=self._debug)
             if not ops:
                  raise ValueError("Empty ops")
        except ValueError:
             if self._debug:
                   log.debug("Falling back to legacy parser")
             ops = parse_js_legacy(js, debug=self._debug)

        if self._debug:
            log.debug("Built algorithm with %d steps", len(ops))
        return Algorithm(ops)

    # ------------------------- Public methods ------------------------- #
    def get_algorithm(self) -> Algorithm:
        """Return the current :class:`Algorithm` object (read‑only)."""
        return self._algo

    def update(self, algo: Algorithm) -> None:
        """Replace the internal algorithm with *algo*."""
        self._algo = algo

    def run(self, signature: str) -> str:
        """Decipher *signature* and return the clean string."""
        self._sig = self._algo.run(signature)
        return self._sig

    # Convenience property
    @property
    def signature(self) -> Optional[str]:
        """Result from the most recent :py:meth:`run` invocation."""
        return self._sig