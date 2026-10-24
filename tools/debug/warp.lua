-- Story Mode scenario warp. The Story Mode start ($88:E70E) takes the scenario from $00E2 when it is nonzero, else 1
-- (then $089C -> $0EB7 = current scenario, 1-7). Run from the title menu with the cursor on Story Mode
-- (work/states/title.mss); write only during the first frames, $E2 is direct-page scratch later.
--   emu.py build/rb_en.sfc --out D --state-in work/states/title.mss --route-str "6 a;1200 -" \
--     --script tools/debug/warp.lua --var SCENARIO=4 --state-out work/states/s4_start.mss
-- tools/debug/regen.sh makes s3..s7_start.mss.
L.on_frame(function(f)
  if f <= 10 then emu.write(0xE2, assert(SCENARIO, "set --var SCENARIO=1..7"), emu.memType.snesWorkRam) end
end)
