# Fev

[Kev](https://github.com/jaredpalmer/kev), without the Hub: the
`jaredpalmer/kev-0.5b` checkpoint exactly as shipped on HuggingFace, plus its
`Qwen/Qwen2.5-0.5B` base model, packed as split git parts so it can be
cloned and served on machines with **no HuggingFace access**. Download once
where the Hub works; `git clone` anywhere.

Both works are Apache-2.0 (see `LICENSE` and `NOTICE`); the checkpoint is
unmodified except that `unpack.sh` re-points its base-model reference at the
local copy.

## Use

On any machine (needs the kev repo and its deps, from GitHub/PyPI):

```sh
git clone https://github.com/jaredpalmer/kev.git ~/kev && cd ~/kev && uv sync --extra serve
git clone https://github.com/francohtlin/fev.git && cd fev && ./unpack.sh
cd ~/kev && HF_HUB_OFFLINE=1 uv run --extra serve python -m kev.serve --run "$OLDPWD/bundle/checkpoint" --port 8009
```

Then talk to it like any System One server:

```sh
curl -s http://127.0.0.1:8009/v1/systemone -X POST \
  -H "Content-Type: application/json" -H "Authorization: Bearer x" \
  -d '{"model":"kev","state":{"text":"..."},"questions":{"q":{"type":"noul","instructions":"...","criteria":{"true":"...","false":"..."}}}}'
```

Verified end to end on a 16GB MacBook Air (Apple Silicon, MPS): checksums,
rebuild from parts, re-patch, and serve with `HF_HUB_OFFLINE=1` against an
empty HuggingFace cache. ~20ms per judgment warm, ~0.1GB resident.

## Layout

| Path | What |
| --- | --- |
| `parts/` | The bundle as ~95MB split parts + `SHA256SUMS` |
| `unpack.sh` | Verify checksums, rebuild `bundle/`, re-patch the base path for this machine |
| `patch_base.py` | The re-patcher (the base-model reference lives inside `head.pt`) |

## Why the re-patch

The checkpoint's base-model name is stored inside `head.pt`'s metadata (and
`adapter_config.json`) as `Qwen/Qwen2.5-0.5B`, which the loader resolves via
the Hub. `unpack.sh` rewrites both to the absolute path of the bundled base,
so nothing ever asks huggingface.co for anything.
