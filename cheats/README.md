# Sons of Sparta: 23 individual resource switches

Updated 2026-10-22. **PPSA28997, 01.008.001, tested BP 4.xx build / PS5 FW 11.60.**

## Choose the file for your reader

| File | Reader and validation |
|---|---|
| [26-switch PS5Upload JSON](json/PPSA28997_01.008.001.json) | Tested on the player's PS5 with the [modified helper](../integrations/ps5upload/README.md). Requires shared-hook retention and session-only checkbox state. Do not distribute this shared layout as stock-CheatRunner compatible. |
| [27-entry CheatRunner mastercode JSON](cheatrunner/PPSA28997_01.008.001.json) | One Resource mastercode, 23 independent resource flags and the same three combat/movement options. Prepared for CheatRunner 0.18/current named-module mastercode readers. Host checks pass; **live CheatRunner execution remains unverified**. |

Both files default to unchecked metadata. Clear previous reader/autoload choices before replacing a file: only the modified PS5Upload helper implements the tested game-PID reset. JSON metadata alone cannot clear another reader's saved choices. The Windows SoS-Trainer.exe is a separate, unchanged application; its feature list was not expanded by this JSON update.

## Effects

The three existing options remain: player-only infinite health/spirit/magic, player damage x6, and high jump (upward impulse x2, approximately x4 height). Each resource has its own switch:

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

The 12 new resources are Крыло странствий, Коготь страха, Морская раковина, Птичьи перья, Кончик хвоста, Клочок меха, Слеза камня, Шерсть льва, Глаз циклопа, Золотой клык, Белокурые волосы and Змеиная шкура. Their names were matched to the running game's Russian localization and item definitions.

Reopen inventory or a purchase/upgrade menu after enabling a resource. Its normal quantity getter tops up the actual wallet; no new pickup is required. Negative and already-higher balances pass through. Disabling stops top-ups and does not remove awarded quantities. Save normally to retain them.

The code does not call equipment, skill, collectible or quest unlock APIs or pickup notification delegates. Golden Fang's localization key is also used by collectible definitions; storage and category checks distinguish the intended resource. The catalog check proves the target key/storage/category combination is unique in the inspected build. This is not an audit of every quest/achievement condition: the game can itself react to possession of an item. High jump can bypass level gates.

## Install and activate

1. Use the exact supported build. Disable cheats and fully close the game before replacing a different cheat package. Use one cheat engine at a time and clear old autoload profiles.
2. For the tested PS5Upload layout, import `json/PPSA28997_01.008.001.json` with the engine off into `/data/ps5upload/cheats/json/`. Run the modified helper. A helper reporting the same official version number is insufficient proof that the modifications are loaded.
3. For CheatRunner, use `cheatrunner/PPSA28997_01.008.001.json` in `/data/cheatrunner/cheats/json/` with a named-module/mastercode reader. Enable **Resource mastercode first**, then the resource options. Disable every resource before disabling the mastercode. Combat/jump do not require it. Live engine validation of this packaging is still required.
4. Load the game and enable the required options. In the modified PS5Upload helper, a new game process starts with all choices off. Returning to the game's main menu does not restart the process. Disable cheats before restarting the helper: restarting it clears its choices but cannot undo patches already present in a running game.

## Build and verification limits

Offsets are relative to the executable mapping of `Il2CppUserAssemblies.prx`, not `eboot.bin`. Readers ignoring per-mod `module_name` are unsupported. Assembly uses virtual module origin 0x10000 before that mapping. Do not port by title/version alone; original instruction bytes must match.

- 21,924 resource emulator cases cover the complete inspected item catalog, all/single/leave-one-out/alternating flags, invalid storage/category, null definitions, negative/high balances, two relocated origins, execute-only text, stack ABI and callee-saved registers.
- The real shared-range C patch planner passed 624 transitions for the 26-switch layout.
- A complete PS5Upload live pass checked 46 resource transitions, every resource flag and shared-hook retention, then verified original bytes restored and all 26 choices off. The player subsequently confirmed all requested new resources appeared and worked. The expanded package has not been tested after a complete game-process relaunch.
- The 27-entry mastercode layout has 0 conflict pairs in the actual CheatRunner C classifier (the shared layout has 253). It matches the 26-switch resource code for 1,073 sampled/edge selections, and passes 1,080 C-plan transitions without shared-range retention. These are host checks, not a live CheatRunner test or exhaustive enumeration of all 23-bit combinations.

The first expanded live attempt failed shared-hook retention. After all options were disabled, the serving helper was gracefully stopped and the stored modified helper relaunched; the complete pass then succeeded. We did not independently identify the earlier serving binary. An older, separate helper SIGSEGV remains unexplained. This JSON does not claim to fix either unrelated crashes or every third-party report. The helper source patch has not passed the full official engine/client quality gate.

## Source and credits

[Resource assembly](source/resources.asm), [offset/flag/item metadata](source/resources-meta.json), [validation reports](validation/). Combat/jump bytes are unchanged from the prior package; see [their source documentation](https://github.com/ToKaMaK0/ps5-sos-trainer/blob/63af5e37443fa3a23ec6f3bfa6b69ec60ba6d554/cheats/README.md#source-attribution-and-license).

AI-assisted console implementation by ToKaMaK0 with Codex and live player testing. Initial game-function research: [OverkillLabs3/SoS-PS5](https://github.com/OverkillLabs3/SoS-PS5). Preserve attribution. Cheat sources retain GPL-2.0-only; the separately identified PS5Upload helper patch is GPL-3.0-or-later. No saves, credentials, account data or game binaries are included.
