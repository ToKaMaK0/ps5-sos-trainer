# PS5 SoS Trainer

## Ready-to-use console JSON

The [Sons of Sparta JSON](cheats/json/PPSA28997_01.008.001.json) is now available separately from the Windows trainer. It was live-tested through PS5Upload 7.1.9 on FW 11.60; the player confirmed health/spirit/magic, damage x6, high jump and the currency pickup top-up.

See [installation, exact compatibility, validation and console assembly source](cheats/README.md). CheatRunner runtime and a subsequent full relaunch with the final JSON remain unverified. Use a reader that supports `module_name`; the offsets target the Il2Cpp module, not eboot.bin.


Experimental Windows trainer for **God of War Sons of Sparta, PPSA28997 01.008.001**. Tested locally with ps5debug-NG 1.3.2 and PS5 FW 11.60.

| Option | Effect |
| --- | --- |
| 1 | Infinite player health, spirit and magic; normal damage |
| 2 | Disable combat effects |
| 3 / 4 | Enable / disable high jump, approximately ×4 height |
| 5 | Combat effects and player damage ×6 |
| 6 | Top up two currencies to 100,000 |
| 7 | Status |

There are **no equipment, skill, collectible or quest unlock commands**. High jump and currency awards are separate manual options. High jump can bypass intended level gates; wallet changes have not been audited against every quest or achievement condition. Keep your own save backup.

The trainer discovers the process and Il2Cpp module on each command, relocates native references, validates code fingerprints, and reuses matching installed hooks. Unknown or incomplete patches stop the operation. It uses allocated executable memory rather than an assumed code cave. Disabling effects retains their code until game exit so in-flight calls remain valid.

## Build and run

1. Obtain `libdebug.dll` separately from your [PS5-MemoryPeeker](https://github.com/POWER-CHANGES-U/PS5-MemoryPeeker) installation. Put it beside the project, or supply `-p:LibDebugPath=ABSOLUTE_PATH_TO_DLL`. This repository does not redistribute that third-party library.
2. With .NET SDK 8 or newer, run `dotnet publish SoSTrainer.csproj -c Release`.
3. Start ps5debug-NG on the PS5 and load your character in the supported game.
4. Run `bin/Release/net8.0/win-x64/publish/SoS-Trainer.exe`, enter the console's LAN IP, and choose the desired option.

The resulting executable is self-contained for Windows x64. TCP 744 connects to the debugger; installing new hooks also requires its reverse TCP connection to Windows port 755. Scope the firewall allowance to this application and your console IP.

Installed effects continue after the PC application exits. Reapply them after completely closing and relaunching the game. **A full game-relaunch test of this trainer build is still pending**; dynamic discovery and relocation alone are not a live restart test.

## Verification

- 85 combat emulation scenarios.
- 40 jump emulation scenarios.
- 35 wallet emulation scenarios, including validation before writes, readback, failure handling, one-shot execution and SysV register/stack preservation.
- `SoS-Trainer.exe --self-test` checks embedded payloads and relocation without connecting to a console.
- Live player confirmed health and high jump; currency top-up was verified by reading the game's resulting amounts. The current default damage multiplier is 1.

Optional native generators and verification scripts use Python with `keystone-engine`, `unicorn`, and `capstone`. See [full instructions](README.txt).

Game function references were researched from [OverkillLabs3/SoS-PS5](https://github.com/OverkillLabs3/SoS-PS5), then checked against the running PS5 game. See [credits](CREDITS.txt) and [GPL-2.0 license](LICENSE.txt). Third-party dependencies retain their own terms. No saved games, console credentials or account data are included.

The Windows trainer source is separate from the console JSON linked above. Not affiliated with Sony or the game developers. Provided without warranty.
