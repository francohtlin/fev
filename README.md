# kev-offline

Kev-0.5b (github.com/jaredpalmer/kev, Apache-2.0) plus its Qwen2.5-0.5B base
(Apache-2.0), packed as split git parts so a machine with **no HuggingFace
access** can run the judge. Same trick as fsim-news-search: download once
where the Hub works, `git clone` anywhere.

Verified on a 16GB MacBook Air: serves fully offline (`HF_HUB_OFFLINE=1`,
empty HF cache), ~20ms per judgment warm, ~0.1GB resident.

## On the offline machine

```sh
git clone https://github.com/jaredpalmer/kev.git ~/kev && cd ~/kev && uv sync --extra serve
git clone <this repo> && cd kev-offline && ./unpack.sh
cd ~/kev && HF_HUB_OFFLINE=1 uv run --extra serve python -m kev.serve --run <path>/kev-offline/bundle/checkpoint --port 8009
```

(The kev repo and PyPI deps come from GitHub/PyPI, not the Hub. If those are
also blocked, vendor them the same way.)

Point any System One client at it, e.g. claudeprophet-nfl:
`JEV_API_URL=http://127.0.0.1:8009/v1/systemone`.

Measured on claudeprophet-nfl's suites: trigger gate 9/11 (misses are
near-threshold false blocks -- conservative), grounding 3/7 (0.5B cannot
read long evidence), forecasting below the coin-flip floor. Use it as a
judge, never a forecaster.
