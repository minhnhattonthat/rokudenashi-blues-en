-- Write one WRAM byte every frame from POKE_AT to POKE_TO (find/confirm RAM values: HP, flags).
--   emu.py build/rb_en.sfc --state-in S --script tools/lua/poke.lua --var ADDR=0x0889 --var VAL=0 --shots 120
L.on_frame(function(f)
  if f < (POKE_AT or 1) or f > (POKE_TO or math.huge) then return end
  emu.write(ADDR, VAL, emu.memType.snesWorkRam)
end)
