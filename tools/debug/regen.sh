#!/bin/sh
# Regenerate the scenario start states (Story Mode, scenario N, first narration page) on ROM ($1, default
# build/rb_en.sfc). Run from the repo root after any build whose text or graphics changed.
ROM=${1:-build/rb_en.sfc}
SKILL=$(python tools/skill.py)
for n in 1 2 3 4 5 6 7; do
  python -X utf8 "$SKILL/scripts/emu.py" "$ROM" --out work/qa/warp_s$n --state-in work/states/title.mss \
    --route-str "6 a;1200 -" --script tools/debug/warp.lua --var SCENARIO=$n \
    --state-out work/states/s${n}_start.mss || exit 1
done
