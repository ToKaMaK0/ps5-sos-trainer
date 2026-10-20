SoS Trainer 0.1.0
God of War Sons of Sparta, PPSA28997, version 01.008.001

Windows x64 trainer. This is a PC application, not a CheatRunner JSON file.
No saved session addresses or PID are required: the game and module are found
on every command. Machine-code fingerprints must match before any game write.
Unknown or partial hooks are rejected. Existing matching trainer hooks are
recognized and reused, including those installed by the original research tool.

USE
1. Start ps5debug-NG on the PS5 (tested with 1.3.2 on FW 11.60).
2. Launch the supported game and load your character.
3. Run SoS-Trainer.exe on Windows, enter the console's LAN IP.
4. Choose 1 for infinite health, spirit and magic. Damage remains normal.
5. After completely closing and relaunching the game, run option 1 again.
   The trainer does not need to stay open once effects are installed.

The single-file build includes its .NET runtime. No .NET install is required.
TCP 744 is used to reach the debugger. First installation of a hook also needs
the debugger's reverse TCP connection to Windows port 755. Allow this only for
the trainer application and the console's LAN IP. Do not disable the firewall.

MENU
1: infinite health, spirit and magic, damage x1.
2: disable all combat effects.
3: high jump, vertical impulse x2, approximate height x4.
4: disable high jump.
5: combat effects with player damage x6.
6: top up loot_currency and loot_orb_red to 100,000 each; never reduce amounts.
7: show status.
0: quit (installed effects keep running).

CLI
SoS-Trainer.exe --status CONSOLE_IP
SoS-Trainer.exe --combat-on CONSOLE_IP
SoS-Trainer.exe --combat-off CONSOLE_IP
SoS-Trainer.exe --jump-on CONSOLE_IP
SoS-Trainer.exe --jump-off CONSOLE_IP
SoS-Trainer.exe --damage-on CONSOLE_IP
SoS-Trainer.exe --money CONSOLE_IP
SoS-Trainer.exe --self-test
SoS-Trainer.exe --license

PROGRESSION
No gear, skill, collectible or quest unlock APIs are called. The trainer does
not grant quest items, boss resources, temple offerings or permanent statistics.
Normal play remains responsible for all progression.
High jump and currencies are separate manual options, never enabled by option 1.
High jump may bypass intended level gates. Currency awards use the game's wallet
API and have not been audited for every possible achievement or quest condition.
Back up your save before using persistent currency changes.

Turning combat/jump off sets their native controls to zero. The validated hooks
remain in memory and pass through normal behavior until the game process exits.
The trainer does not free code that an in-flight call could still be executing.
It does not edit files, save automatically, reboot the console or terminate games.

VALIDATION
85 native combat scenarios and 40 jump scenarios passed under Unicorn.
35 wallet scenarios passed: pre-validation, amounts, readback, one-shot execution,
failure handling and SysV register/stack preservation.
Self-test covers embedded payload integrity and relocation to another module base.
Live game behavior and a complete game-relaunch test are recorded separately;
emulation alone is not a claim of a live-console test.

BUILD FROM SOURCE
.NET SDK 8 or newer, Windows x64 target.
Obtain libdebug.dll from your existing PS5-MemoryPeeker installation and put it
beside SoSTrainer.csproj, or pass -p:LibDebugPath=ABSOLUTE_PATH_TO_DLL.
The public source archive does not redistribute this third-party DLL.
dotnet publish SoSTrainer.csproj -c Release
Output: bin/Release/net8.0/win-x64/publish/SoS-Trainer.exe

Native generators are optional: install keystone-engine, unicorn and capstone
with Python; run build_combat.py then build_jump.py before publishing.
Run verify_combat.py and verify_jump.py to verify those generated payloads.
verify_money.py consumes money-test.bin, emitted from MoneyImage at module base
0x801A0000 and allocation base 0x300000000 for development verification.

See CREDITS.txt and LICENSE.txt. Distributed without warranty.
