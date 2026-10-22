# Sons of Sparta: individual resource switches

Game: **PPSA28997, 01.008.001, tested BP 4.xx build**, PS5 FW 11.60.

## Choose the file for your reader

| File | Reader and status |
|---|---|
| [14-switch PS5Upload JSON](json/PPSA28997_01.008.001.json) | Same file tested on the player's console. Requires the [local helper changes](../integrations/ps5upload/README.md) for independent shared-hook removal and session-only checkbox state. Do not import into stock CheatRunner. |
| [15-switch mastercode JSON](cheatrunner/PPSA28997_01.008.001.json) | Prepared for CheatRunner 0.18/current named-module mastercode readers. Includes one shared resource mastercode plus the same 14 effects. Real CheatRunner conflict analysis and host patch tests pass; **live CheatRunner execution remains unverified**. Can also be used with a named-module PS5Upload reader if the mastercode is explicitly enabled first. |

Both files default to unchecked metadata. Existing reader state/autoload profiles are separate: disable or clear profiles for the previous file before replacing it. Only the modified PS5Upload helper implements the tested game-PID reset. Do not treat JSON metadata as a guarantee that every reader clears saved choices.

## Effects

Three combat/movement options are unchanged: player-only infinite health/spirit/magic; player damage x6; high jump (upward impulse x2, approximately x4 height).

Each resource below has its **own** switch:

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

Reopen inventory or an upgrade menu after enabling a resource. The normal quantity getter tops up the actual wallet; no new pickup is required, including currencies. Negative and already-higher quantities pass through. Disabling stops top-ups and does not remove quantities already awarded. Save normally to retain awarded quantities.

No equipment, skill, collectible, or quest unlock commands are included. The resource code calls the dictionary mutation core, not pickup/story notification delegates. High jump can bypass level gates. This is not an audit of every achievement or progression condition.

## Install

1. Use the exact supported game/build. Completely close the game and disable the other trainer/engine before changing packages. Clear old autoload profiles: mod indices have changed.
2. For the tested 14-switch package, install the modified helper and import `json/PPSA28997_01.008.001.json` into PS5Upload with cheats off. It belongs in `/data/ps5upload/cheats/json/`.
3. For CheatRunner, use only `cheatrunner/PPSA28997_01.008.001.json` in `/data/cheatrunner/cheats/json/`. Do not also leave another cheat file for this same game/version selected. Use a reader supporting per-mod `module_name` and mastercodes.
4. Load the game. In the 15-switch package, enable **Resource mastercode** first, then any resource options. CheatRunner may auto-enable it; if a reader's cooldown rejects the following dependent toggle, wait for that cooldown and toggle the resource again. Explicitly enabling the mastercode first avoids that interaction. Turn individual resources off before turning the mastercode off. Combat/jump do not need the resource mastercode.
5. In the tested PS5Upload package, the new game process begins with all choices off. Returning to the game's main menu is not a process restart. Restarting only the helper clears its choices but does not undo memory patches in an already-running game; disable cheats first.

## Compatibility and validation

Offsets are relative to the executable mapping of `Il2CppUserAssemblies.prx`, **not eboot.bin**. Readers ignoring `module_name` are unsupported. Assembly uses the virtual module origin 0x10000 before that executable mapping. Do not port to another update/backport by title/version alone; original instruction bytes must match.

The 14-switch PS5Upload package passed 8,876 resource emulator cases with execute-only text, null/invalid definitions, balances, all/single/alternating flag masks, and two relocated origins. The real C patch planner passed 336 randomized transitions. Two live 28-transition passes verified every flag, shared hook retention and complete final restoration. The player subsequently reported success after a full game close/relaunch; that confirmation is a player report, not a second machine memory capture.

The mastercode package emits exactly the same live-tested resource code for all 2,047 nonempty resource selections. The actual current CheatRunner C conflict classifier reports **0 conflict pairs**, versus 55 for the shared 14-switch layout. A native C patch planner additionally passed 600 transitions without shared-range retention. These host checks do **not** constitute a live CheatRunner test. HEN reports [177](https://github.com/TeeKay87/HEN-Cheats-Collection/issues/177) and [180](https://github.com/TeeKay87/HEN-Cheats-Collection/issues/180) concern the older file; their comments recommend CheatRunner 0.18. We have not reproduced their users' failures or established that this update fixes them.

One PS5Upload helper SIGSEGV preceded the two successful passes. Its cause remains unknown; this package must not be represented as fixing that separate helper failure. No full official engine/client quality gate was run for the helper source patch.

## Source and attribution

New resource code: [assembly](source/resources.asm), [offset/flag/item metadata](source/resources-meta.json), [validation](validation/). Combat/jump patch bytes are unchanged from the previously published five-switch set; their assembly is in [the prior source documentation](https://github.com/ToKaMaK0/ps5-sos-trainer/blob/63af5e37443fa3a23ec6f3bfa6b69ec60ba6d554/cheats/README.md#source-attribution-and-license).

AI-assisted console implementation by ToKaMaK0 with Codex and live player testing. Initial game-function research: [OverkillLabs3/SoS-PS5](https://github.com/OverkillLabs3/SoS-PS5). Preserve that attribution. Console cheat sources retain the repository's GPL-2.0-only license; the separately identified PS5Upload patch is GPL-3.0-or-later, matching its upstream project. No saves, account data, console credentials or game binaries are included.
