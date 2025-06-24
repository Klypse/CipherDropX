"""
CipherDropX — main.py
=============================================================================
Repository : https://github.com/Klypse/CipherDropX
Author     : Klypse
License    : Apache-2.0
Generated  : 2025-06-24

Part of the CipherDropX utility suite.

This header only augments documentation; executable code below is unchanged.
"""
import requests
from cipherdropx import CipherDropX

# base.js URL
#url = "https://www.youtube.com/s/player/9fe2e06e/player_ias.vflset/ja_JP/base.js"
url = "https://www.youtube.com/s/player/f676c671/player_ias.vflset/en_US/base.js"
res = requests.get(url)
res.raise_for_status()

# decipher
cdx = CipherDropX(res.text)
algorithm = cdx.get_algorithm()
print(algorithm)
cdx.update(algorithm)

sig = "1A2B3C4D5E6F7G8H9I0JKLMNOPQRSTUVWX"
cdx.run(sig)

print("Original:", sig)
print("Deciphered:", cdx.signature)