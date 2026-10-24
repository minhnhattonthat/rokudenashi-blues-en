# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** release candidate; v0.9 built locally (release/, not published; predates the playtest fixes). Last
  build: 2026-10-24, sha1 f8dcf0cd.
- **Done:** all script + other text translated; astra review + fixes for b1a b1b b2 b3 b4 b5 b7a b7b, b6
  self-reviewed (astra dispatch blocked by classifier outage); title menu, options, shouts checked in game.
  Graphics (docs/re/graphics.md): boot copyright, title logo + subtitle, RAGE badge, VS banners, ending mini logo,
  story sound effects (sfx.py).
  Agent playtests 2026-10-24 (docs/bugs.md): options, attract, 1P Blues (lose + win, 2 fighters), Story Mode
  Scenario 1 to mid Scenario 3. Fixed: wrap limit one cell narrower (text clipped at x=240), command label
  padding, sound effects, 5 wording items.
- **Playtest kit:** docs/playtester-brief.md; `tools/lua/fightcheat.lua` (GOD/ONEHIT, via `play.py --script`);
  states (made on build 2812353d or later): work/states/title.mss, s1_hatanaka.mss (Scenario 1 ring fight),
  s1_after_hatanaka.mss. Story3 session states (work/playtest/story3, build 2812353d) reach Scenario 3 Akane scene.
- **Next:** playtest Scenario 3 (Akane fight) onward to the ending and credits; see the other 8 sound effects and
  WAIT! / DOUBLE KO in play; astra review of b6; rebuild release after the fixes; user playtest.
- **Known/accepted:** long speeches auto-page mid-sentence (bugs.md, won't fix for now); 2P Blues needs pad 2
  (play.py drives pad 1 only).
- **Known Japanese left:** copier warning (string at 0x434BD, no pointer found; copier hardware only).
- **Open bugs:** none.
- **Waiting on the user:** playtest.
