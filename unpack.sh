#!/bin/sh
# Rebuild the Kev bundle on a machine with no HuggingFace access.
# Needs: the kev repo installed (github.com/jaredpalmer/kev, `uv sync --extra serve`).
set -e
cd "$(dirname "$0")"
( cd parts && shasum -a 256 -c SHA256SUMS )
mkdir -p bundle && cat parts/kev-bundle.tgz.* | tar xzf - -C bundle
KEV_REPO="${KEV_REPO:-$HOME/kev}"
( cd "$KEV_REPO" && uv run python "$OLDPWD/patch_base.py" "$OLDPWD/bundle" )
echo "Serve with:"
echo "  cd $KEV_REPO && HF_HUB_OFFLINE=1 uv run --extra serve python -m kev.serve --run $(pwd)/bundle/checkpoint --port 8009"
