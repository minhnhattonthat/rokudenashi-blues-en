-- Preview every fight banner in a VS fight: from frame POKE_AT on, write the three banner tilemaps (as the
-- $AF:F040 records do) into the BG3 map at VRAM $5000: FIGHT! row 9, WAIT! row 13, DOUBLE KO row 17.
--   emu.py build/rb_en.sfc --state-in <VS fight state> --script tools/lua/bannerpoke.lua --var POKE_AT=30 --shots 60
local banners = { { 0x34, 6, 9, 13 }, { 0x46, 6, 13, 13 }, { 0x58, 8, 17, 12 } } -- first tile, width, row, col
L.on_frame(function(f)
  if f < (POKE_AT or 30) then return end
  for _, b in ipairs(banners) do
    local t = b[1]
    for r = 0, 2 do
      for c = 0, b[2] - 1 do
        local word = 0x5000 + (b[3] + r) * 32 + b[4] + c
        emu.write(word * 2, t, emu.memType.snesVideoRam)
        emu.write(word * 2 + 1, 0x38, emu.memType.snesVideoRam)
        t = t + 1
      end
    end
  end
end)
