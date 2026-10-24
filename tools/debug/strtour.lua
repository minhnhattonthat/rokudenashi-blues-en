-- String tour (tools/debug/strtour.py): the first dialogue the reader ($88:A168, offset $1E0A = 0) starts reads
-- CHUNK (24-bit CPU address of a {page}-joined block of strings in the debug ROM). The box width is held at the
-- portrait box (13 / 11 cells; face codes in the block would switch it). Once the reader has been idle on a
-- {page} or {end} for 20 frames the page is waiting for a key: shoot pNNNN.png, press A. Idle 240 frames on any
-- other code = the engine paged by itself (an overflow): shot pNNNN_auto.png. The box closing after {end} stops.
local m = emu.memType.snesMemory
local started, ending, last, word, page, press, shot = false, false, 0, 0, 0, 0, false
local function rd(a) return emu.read(a, m) | emu.read(a + 1, m) << 8 end
L.on_exec(0x88A168, 0x88A168, function()
  local off = rd(0x1E0A)
  if not started then
    if off ~= 0 then return end
    started = true
    emu.write(0x1CFB, CHUNK & 0xFF, m)
    emu.write(0x1CFC, (CHUNK >> 8) & 0xFF, m)
    emu.write(0x1CFD, CHUNK >> 16, m)
  end
  local p = emu.read(0x1CFB, m) | emu.read(0x1CFC, m) << 8 | emu.read(0x1CFD, m) << 16
  word, last, shot = rd(p + 2 * off), L.frame, false
  if word == 0xFFFF then ending = true end
end)
L.on_frame(function(n)
  emu.write(0x0F98, (emu.read(0x0F98, m) & 0xE0) | 13, m)
  emu.write(0x0F99, (emu.read(0x0F99, m) & 0xF0) | 11, m)
  if not started or shot then return end
  local idle = n - last
  if (idle == 20 and (word == 0xFFE0 or word == 0xFFFF)) or idle == 240 then
    L.shot(string.format("p%04d%s.png", page, idle == 240 and "_auto" or ""))
    page, shot, press = page + 1, true, 6
    if ending then L.log("pages " .. page); L.finish(0) end
  end
end)
emu.addEventCallback(L.safe(function()
  if press > 0 then press = press - 1; emu.setInput({ a = true }, 0) end
end), emu.eventType.inputPolled)
