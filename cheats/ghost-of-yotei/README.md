# Ghost of Yotei: PPSA26344 / 02.002.000

26 independent switches, all OFF by default. Updated 2026-11-10.
Combat and movement are first, currency and materials follow, and the six ammunition switches are last.

- [Bilingual PS5Upload JSON](../json/PPSA26344_02.002.000.json)
- [Identical CheatRunner review JSON](../cheatrunner/PPSA26344_02.002.000.json)
- [Validation and limits](../validation/ghost-of-yotei-PPSA26344-02.002.000.json)

## Activation

Load gameplay in the exact supported build and import the single bilingual table for this title.
PS5Upload's console folder is `/data/ps5upload/cheats/json/`. Enable the engine and the switches you want.
Clear the reader's old saved selection when replacing the earlier table: indices have changed.
Use one cheat engine at a time. No preparation switch is required.

Infinite Resolve prevents spending the current yellow-circle reserve. If empty, drink sake first.
Normal replenishment works. The player confirmed repeated ability use without spending resolve.

Enhanced High Jump boosts ordinary standing and running jumps. The player confirmed sufficient
height and normal landing. Disabling restores the next jump. This is not an infinite-air-jump
option; the internal vertical-offset scale of 32 is not a measured height multiplier.
High jumps may bypass intended level gates.

Currency and material effects run when the corresponding quantity changes through receiving or
spending it. Opening inventory alone does not refill it. Mon has a minimum of 99,999; materials
have a minimum of 1,000. Existing higher quantities are retained and negative sentinel values
are skipped. Mushrooms and fish are independent. Plants / Ezo spruce share one counter;
silk / bast cloth share one counter. English names are descriptive translations of verified
Russian labels. Disabling does not undo already awarded resources or saved progress.

The final six switches refill ordinary, heavy, flaming, poison, disarming and explosive arrows
to the player's current validated capacity. Ordinary resource purchases and spends were checked;
special-arrow crafting was tested, but firing/consumption was not independently verified.

## Compatibility and verification

Live research: PS5 Pro FW 11.60, PPSA26344, version 02.002.000. Another region, version or
executable layout may differ. Compare every declared OFF byte before applying.
Reordering and translation changed no ON/OFF bytes; all 55 patch ranges are disjoint.

The original Infinite Health and One Hit Kill entries are unchanged Yharnam codes from HEN
Cheats Collection, not independently combat-tested in this package. Custom resources, high
jump and resolve were checked through PS5Upload and player testing. Resource emulation covered
181,542 cases / 540 selected masks; jump covered 396 cases; resolve covered 864 cases.
These are bounded checks. Live CheatRunner/etaHEN execution and a full game-process restart
with this reordered table remain unverified; its identical JSON is supplied for maintainer review.

No equipment, quest or mass skill unlock operation is included. Keep a save backup.
No saves, account data, memory dumps or game binaries are distributed here.

Original combat codes: Yharnam via [HEN Cheats Collection](https://github.com/TeeKay87/HEN-Cheats-Collection).
Independent resource, jump and resolve research and packaging: ToKaMaK0 with Codex assistance.
Thanks to the PS5Upload, ps5debug-NG and cheat-library maintainers.
