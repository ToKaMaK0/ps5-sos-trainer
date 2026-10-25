# Sons of Sparta: damage x50 and 26 resource switches

Updated 2026-10-25. **PPSA28997 / 01.008.001, exact tested BP 4.xx build, PS5 FW 11.60.**

The player confirmed damage x50 is now sufficient and all enabled effects work. This update also includes Death Powder, Pomegranate Seed and Agony Ash, each with its own switch. No experimental enemy-immunity option is included.

## Files and supported readers

- [PS5Upload JSON](json/PPSA28997_01.008.001.json)
- [CheatRunner review JSON](cheatrunner/PPSA28997_01.008.001.json)

Both files are now byte-identical: **30 entries = 3 combat/movement options + 1 resource preparation option + 26 resource switches**. Common code and the quantity hook belong only to preparation; each resource owns one flag. The current package is live-tested with **stock PS5Upload 7.5.2**, without the old custom helper. The actual CheatRunner C conflict classifier reports zero conflict pairs, but **this 30-entry package has not been run live in CheatRunner**. Readers must honor per-mod `module_name` for `Il2CppUserAssemblies.prx`.

All file metadata defaults to off. Reader presets/autoload selections are stored separately and can reapply after restart; clear old profiles when replacing an older layout. The separate Windows SoS-Trainer.exe retains its previous feature set.

## Effects

- Infinite player health, spirit and magic.
- Player damage **x50**, applied only to player attacks against enemies; not enemy or self damage.
- High jump: upward impulse x2, approximately x4 height.
- Independent quantity minimums:

| Resource / ресурс | Internal ID | Minimum |
|---|---|---|
| Монеты | `loot_currency` | 100000 |
| Красные сферы | `loot_orb_red` | 100000 |
| Ржавый обломок | `loot_common_spear` | 1000 |
| Необработанная руда | `loot_common_shield` | 1000 |
| Блестящий металл | `loot_rare_spear` | 1000 |
| Прочная пластина | `loot_rare_shield` | 1000 |
| Критский точильный камень | `loot_epic_spear_tip` | 1000 |
| Эгейский кристалл | `loot_epic_spear_tip_status` | 1000 |
| Коринфская кожа | `loot_epic_spear_grip` | 1000 |
| Ионийская соль | `loot_epic_spear_tail` | 1000 |
| Сплав из Элизия | `loot_epic_shield` | 1000 |
| Крыло странствий | `loot_common_wing` | 1000 |
| Коготь страха | `loot_common_fang` | 1000 |
| Морская раковина | `loot_common_shell` | 1000 |
| Птичьи перья | `loot_rare_feather` | 1000 |
| Кончик хвоста | `loot_rare_tail` | 1000 |
| Клочок меха | `loot_rare_fur` | 1000 |
| Слеза камня | `loot_epic_gorgon` | 1000 |
| Шерсть льва | `loot_mythic_lost_boy` | 1000 |
| Глаз циклопа | `loot_boss_cyclops` | 1000 |
| Золотой клык | `loot_mythic_boar_jr` | 1000 |
| Белокурые волосы | `loot_epic_siren` | 1000 |
| Змеиная шкура | `loot_mythic_ladon` | 1000 |
| Порошок смерти | `loot_rare_charm` | 1000 |
| Семечко граната | `loot_epic_charm_physical` | 1000 |
| Пепел мучений — Яма мучений | `loot_offering_agony_points` | 100000 |

**Two different Pit currencies:** the shop during a Pit run uses **red orbs** (`loot_orb_red`, option 5). The player saw 100,000 after completing a trial and receiving the first award; opening the shop alone did not immediately refresh it. **Agony Ash / Пепел мучений** (`loot_offering_agony_points`, option 29) is separate: the player confirmed 11,900 → 100,000 after enabling it and reopening its menu. Pomegranate Seed is option 28; Death Powder is option 27.

## Install and activate

1. Match the exact game build. Disable cheats and fully close the game before replacing a different package. Use one cheat engine at a time.
2. Import the PS5Upload JSON with its engine off into `/data/ps5upload/cheats/json/`. For a named-module CheatRunner reader, the review file belongs in `/data/cheatrunner/cheats/json/`; live validation there is still pending.
3. Load the game. Enable **Resource preparation first**, then the individual resources needed. Turn every resource off before turning preparation off. Health, damage and jump work independently of resource preparation.
4. Reopen inventory or the relevant purchase/upgrade menu to trigger the normal quantity check. Follow the observed Pit-specific conditions above. Negative and already-higher quantities pass through; disabling stops top-ups and does not remove already awarded amounts. Save normally in the game to retain inventory changes.

The code calls the verified wallet dictionary core, not equipment, skill, collectible or quest-unlock APIs or pickup notification delegates. Possession can still be checked by game logic; no exhaustive progression audit is claimed. High jump can cross intended level gates.

## Verification and limits

- 26,292 resource emulation scenarios: complete inspected catalog, independent flags, invalid definitions/storage/category, negative/high quantities, two image origins, execute-only text, stack and preserved registers. Resource patch bytes are unchanged by the x50 update.
- 86 combat scenarios for x50 on two relocated origins; 1,200 transitions of the real PS5Upload C planner for the exact current JSON.
- Zero conflict pairs from the actual CheatRunner C classifier for this file.
- Live PS5Upload: prior damage ON/OFF checked before replacement, full file readback and all declared code bytes verified after activation. Other enabled choices were preserved. The player confirmed x50 combat, Pomegranate Seed and Agony Ash.
- Earlier health/jump restoration was checked in a fresh process; the latest 30-entry/x50 revision has not had its own full game-process relaunch test. Host classification is not live CheatRunner validation.

Offsets are relative to the executable PRX mapping. Assembly uses virtual origin 0x10000 before that mapping. Title/version alone is insufficient for a port: original instruction bytes must match.

## Source and attribution

[Resource assembly](source/resources.asm), [resource identity/flag metadata](source/resources-meta.json), [x50 damage assembly](source/damage_filter.asm), [health assembly](source/health_entry.asm), [static module metadata](source/console-meta.json), [verification reports](validation/).

Console implementation: ToKaMaK0 with Codex/AI assistance and live player testing. Initial function research: [OverkillLabs3/SoS-PS5](https://github.com/OverkillLabs3/SoS-PS5). Preserve credits and GPL-2.0-only source licensing. The separately retained old PS5Upload helper patch is GPL-3.0-or-later and is not required by this package. No saves, credentials, account data or game binaries are included.
