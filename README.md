# CipherDropX

**CipherDropX** is a small, dependency‑light Python library that extracts the client‑side transformation routine stored in YouTube’s `base.js` player file and applies it to any signature string.
It does **not** execute JavaScript and does **not** rely on a browser or Node runtime – only regular‑expression parsing and a tiny in‑memory virtual machine.

---

## Installation

```bash
pip install cipherdropx
```

*(Python 3.9 or newer is recommended)*

---

## When is it useful?

\* Whenever you already have a copy of *base.js* (downloaded once, shipped with your own binaries, etc.) and need to transform many signatures without re‑downloading the player file each time.
\* When you want to keep network, JavaScript and heavy AST libraries out of your build.

---

## Basic workflow

1. **Create** a `CipherDropX` instance with the raw *base.js* text.
2. **Extract** the algorithm once via `.get_algorithm()` – you can cache or serialise it.
3. **Feed** the algorithm back with `.update()` *(or skip and keep the internal one)*.
4. **Run** `.run(sig)` to obtain the transformed signature.
5. The result is stored in `.signature`.

---

## Example A – live download with *requests*

```python
import requests
from cipherdropx import CipherDropX

# 1️⃣ Pull the latest player file (≈100 kB)
url = "https://www.youtube.com/s/player/9fe2e06e/player_ias.vflset/ja_JP/base.js"
res = requests.get(url)
res.raise_for_status()  # ensure HTTP 200

# 2️⃣ Build the decipher helper from raw JS
cdx = CipherDropX(res.text)           # ↖️ parses method table & CHALL stub
algo = cdx.get_algorithm()            # ↖️ returns Algorithm object (can be cached)
cdx.update(algo)                      # ↖️ loads the algorithm into the instance

# 3️⃣ Apply it to any signature string
sig = "1A2B3C4D5E6F7G8H9I0JKLMNOPQRSTUVWX"
cdx.run(sig)                          # ↖️ executes splice / swap / reverse steps

print("Original :", sig)
print("Deciphered:", cdx.signature)   # transformed output
```

---

## Example B – using a local *base.js* snapshot

```python
from pathlib import Path
from cipherdropx import CipherDropX

# 1️⃣ Load player file that was stored previously
basejs_text = Path("./assets/base_20250616.js").read_text(encoding="utf‑8")

# 2️⃣ Initialise helper (parsing happens once)
cdx = CipherDropX(basejs_text)

# ▶️ If you saved the algorithm earlier you could do:
#     cached_algo = json.loads(Path("algo.json").read_text())
#     cdx.update(cached_algo)
#   otherwise just generate it again:
algorithm = cdx.get_algorithm()
cdx.update(algorithm)

# 3️⃣ Transform signature
sig = "ABCDEF1234567890"
cdx.run(sig)
print(cdx.signature)
```

---

## Caching tips

* `Algorithm` is just a list of `(action, argument)` tuples – safe to `json.dump` and reuse later.
* You can keep one *base.js* offline and only refresh it if YouTube ships a new player revision.

---

## License

Apache‑2.0 – see the [LICENSE](LICENSE) file for details.

---

### Disclaimer

CipherDropX is provided **solely for educational and integration purposes**.
You are responsible for complying with the terms of service of the platform you interact with.
