-- Fight cheat for playtests. Fighter slots are $0700 + $C0*n (P1 $0700, P2 $07C0). Real HP (255 max) is +$1C:
-- the damage code at $AF:F845 subtracts, clamps a low result to 2, then 1, and KOs on a hit that lands at 1.
-- +$15 is only the HUD bar, which follows +$1C a point per frame.
--   GOD=1    pin P1 HP at 255 (only while nonzero, so screens without a fighter stay untouched)
--   ONEHIT=1 opponent slots' HP held at 1: the next hit KOs
--   play.py SESSION --rom R --state S --script tools/lua/fightcheat.lua --var GOD=1 --var ONEHIT=1
L.on_frame(function(f)
  local wram = emu.memType.snesWorkRam
  if GOD and emu.read(0x071C, wram) ~= 0 then emu.write(0x071C, 255, wram) end
  if not ONEHIT then return end
  for n = 1, 3 do
    local a = 0x071C + 0xC0 * n
    if emu.read(a, wram) > 1 then emu.write(a, 1, wram) end
  end
end)
