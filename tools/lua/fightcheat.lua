-- Fight cheat for playtests. P1 slot $0700, P2 slot $07C0 (+$C0); real HP (255 max) is +$1C, +$15 only the HUD bar.
-- Damage code $AF:F845: a hit that leaves < 3 sets HP 1 and a stun ($08B6 = 600, +$0B |= $80); a hit at HP 1 KOs
-- ($0895 = 3). $0880+ is fight state, not a third fighter: never write it.
--   GOD=1    pin P1 HP at 255 (only while nonzero, so screens without a fighter stay untouched)
--   ONEHIT=1 hold P2 HP at 3: the next hit takes the game's own path to 1, the one after KOs
--   play.py SESSION --rom R --state S --script tools/lua/fightcheat.lua --var GOD=1 --var ONEHIT=1
L.on_frame(function(f)
  local wram = emu.memType.snesWorkRam
  if GOD and emu.read(0x071C, wram) ~= 0 then emu.write(0x071C, 255, wram) end
  if ONEHIT and emu.read(0x07DC, wram) > 3 then emu.write(0x07DC, 3, wram) end
end)
