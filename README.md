# Fev

**F**ranco's **ev**aluator. Jev is TypeSafe's typed-decision judge; Kev is the
open-source replica you can train yourself; Fev is mine — the judge, running
on my machines, no HuggingFace required.

Today Fev ships the Kev-0.5b checkpoint (github.com/jaredpalmer/kev,
Apache-2.0) plus its Qwen2.5-0.5B base (Apache-2.0) as split git parts —
download once where the Hub works, `git clone` anywhere. Verified end to end
on a 16GB MacBook Air: rebuild from parts, re-patch, serve fully offline
(`HF_HUB_OFFLINE=1`, empty cache), ~20ms per judgment warm, ~0.1GB resident.

The roadmap is the reason this repo exists apart from upstream: an
**NFL-tuned judge** trained on claudeprophet-nfl's labelled record — move
triggers (12-3 designation vs 0-2 interpretive), grounding pairs, evidence
materiality — a checkpoint of my own in the same shape upstream releases
theirs.

## Run it on an offline machine

```sh
git clone https://github.com/jaredpalmer/kev.git ~/kev && cd ~/kev && uv sync --extra serve
git clone git@github.com:francohtlin/fev.git && cd fev && ./unpack.sh
cd ~/kev && HF_HUB_OFFLINE=1 uv run --extra serve python -m kev.serve --run "$OLDPWD/bundle/checkpoint" --port 8009
```

(kev's code and deps come from GitHub/PyPI, not the Hub; vendor them the same
way if those are blocked too.)

Point any System One client at it — e.g. claudeprophet-nfl:

```sh
JEV_API_URL=http://127.0.0.1:8009/v1/systemone
```

## What this judge is for, measured

On claudeprophet-nfl's benchmark suites, kev-0.5b: **trigger gate 9/11**
(both misses near-threshold false blocks — conservative in the safe
direction), grounding 3/7 (a 0.5B backbone cannot read long evidence),
forecasting below the coin-flip floor. A judge, never a forecaster.

## Layout

| Path | What |
| --- | --- |
| `parts/` | The bundle as ~95MB split parts + SHA256 manifest |
| `unpack.sh` | Verify, rebuild `bundle/`, re-patch the base path for this machine |
| `patch_base.py` | The re-patcher (the base reference lives inside `head.pt`) |
