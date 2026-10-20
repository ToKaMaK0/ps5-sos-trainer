# Sons of Sparta console cheats

[Download the ready-to-use JSON](https://raw.githubusercontent.com/ToKaMaK0/ps5-sos-trainer/main/cheats/json/PPSA28997_01.008.001.json)

For **God of War Sons of Sparta, PPSA28997, 01.008.001 (tested BP 4.xx build)**.
Live-tested on PS5 FW 11.60 using **PS5Upload 7.1.9**. The player confirmed all four effects on 2026-10-20.

| Switch | Effect |
|---|---|
| Infinite health, spirit and magic | Player-only HP, grey HP, spirit and magic protection |
| Player damage x6 | Multiplies player attacks against enemies; restores shared damage data after the call |
| High jump x4 height | Doubles upward player jump impulse; approximate height x4 |
| Coins and red orbs: minimum 100000 on pickup | A positive pickup brings that currency to at least 100,000; pick up a coin or red orb after enabling |

## Install and activate

1. Start the PS5Upload helper on the PS5. Load your character in the supported game.
2. Import `json/PPSA28997_01.008.001.json` through PS5Upload, or copy it to `/data/ps5upload/cheats/json/`.
3. Open PS5Upload on the console, choose **Cheats**, and toggle the desired effects with Cross. Return to the game.
4. Start the helper again after rebooting the console. The JSON remains on disk.

A copy may also be placed in `/data/cheatrunner/cheats/json/`. **CheatRunner runtime testing is still pending**; only file placement and its named-module resolver were checked. The final JSON has not yet undergone a subsequent full game-process relaunch test. Use one cheat engine at a time and close/relaunch the game before switching from the Windows trainer.

## Compatibility and scope

This file requires a reader that implements the per-mod `module_name` field and resolves `Il2CppUserAssemblies.prx` to its executable mapping. Do not assume compatibility with readers that ignore this field: the offsets are not relative to eboot.bin. Do not apply it to another game/version/backport without checking the module and original bytes.

No quest, equipment, skill or collectible unlock functions are patched. High jump can bypass level gates. Currency changes may persist in saves and have not been audited against every achievement or quest condition. Keep your own save backup.

The PC executable is not required for these JSON effects. Enabling and exact installed bytes were verified through PS5Upload and independent memory readback. The player confirmed combat, jump and currency behavior. Console-native checks cover 126 combat/jump cases at two module origins plus 2,912 wallet cases, including the full 180-item catalogue, negative/pass-through amounts and SysV argument/register/stack preservation. The native code was tested with **execute-only** code pages; it does not read or write configuration in text pages.

## Source, attribution and license

AI-assisted implementation by ToKaMaK0 with Codex. Initial game-function research: [OverkillLabs3/SoS-PS5](https://github.com/OverkillLabs3/SoS-PS5). See the repository [credits](../CREDITS.txt) and [GPL-2.0-only license](../LICENSE.txt). No affiliation with Sony or the game developers. No saved games, account data or console credentials are included.

The assembly sources below correspond to this JSON. They use offsets from the virtual module origin, **64 KiB before** the executable mapping used by PS5Upload. For the JSON memory offsets, subtract `0x10000` from these assembly offsets. Compile with Keystone x86-64 at the listed origin, zero the leading label table (metadata only), and replace the single LEA displacement `0x11223344` with `0x629c8f0 - (instruction_end_offset)`. The JSON's hook locations contain the corresponding original bytes and replacements. Configuration is encoded in instruction immediates because module text is execute-only.

<details>
<summary>combat: assembly origin 0x47A2000, 536 bytes</summary>

```asm
.quad health_entry,grey_entry,spirit_entry,mana_filter,health_filter,grey_filter,spirit_filter,on_player,control
health_entry:
push rdi
push rsi
push rdx
sub rsp,16
movss dword ptr [rsp],xmm0
mov rcx,rsp
call health_filter
movss xmm0,dword ptr [rsp]
add rsp,16
pop rdx
pop rsi
pop rdi
.byte 85,72,137,229,83,80,49,192,128,127,44,1
jmp 14333276


grey_entry:
push rdi
push rsi
push rdx
sub rsp,16
movss dword ptr [rsp],xmm0
mov rcx,rsp
call grey_filter
movss xmm0,dword ptr [rsp]
add rsp,16
pop rdx
pop rsi
pop rdi
.byte 85,72,137,229,65,87,65,86,83,72,131,236,40
jmp 14334717


spirit_entry:
push rdi
push rsi
push rdx
sub rsp,16
movss dword ptr [rsp],xmm0
mov rcx,rsp
call spirit_filter
movss xmm0,dword ptr [rsp]
add rsp,16
pop rdx
pop rsi
pop rdi
.byte 85,72,137,229,65,87,65,86,65,85,65,84
jmp 14295228


on_player:
test rdi,rdi
jz on_player_false
cmp qword ptr [rdi+16],0
je on_player_false
push rbx
mov rbx,rdi
lea rax,[rip+0x11223344]
mov rax,qword ptr [rax]
test rax,rax
jz on_player_pop_false
call rax
test rax,rax
jz on_player_pop_false
mov rdi,rax
xor esi,esi
call 8449904
pop rbx
ret
on_player_pop_false:
pop rbx
on_player_false:
xor eax,eax
ret


health_filter:
push rbx
push r12
push r13
mov rbx,rdi
mov r12,rcx
call on_player
test al,al
jz health_done


movss xmm0,dword ptr [rbx+0x38]
movss dword ptr [rbx+0x40],xmm0
mov dword ptr [rbx+0x44],0
xorps xmm1,xmm1
movss xmm0,dword ptr [r12]
ucomiss xmm0,xmm1
jp health_done
jae health_done
mov dword ptr [r12],0


health_done:
xor eax,eax
pop r13
pop r12
pop rbx
ret


grey_filter:
push rbx
push r12
push r13
mov rbx,rdi
mov r12,rcx
call on_player
test al,al
jz grey_done


movss xmm0,dword ptr [rbx+0x38]
movss dword ptr [rbx+0x40],xmm0
mov dword ptr [rbx+0x44],0
xorps xmm1,xmm1
movss xmm0,dword ptr [r12]
ucomiss xmm0,xmm1
jp grey_done
jbe grey_done
mov dword ptr [r12],0


grey_done:
xor eax,eax
pop r13
pop r12
pop rbx
ret


spirit_filter:
push rbx
push r12
push r13
mov rbx,rdi
mov r12,rcx
call on_player
test al,al
jz spirit_done


movss xmm0,dword ptr [rbx+0x24]
movss dword ptr [rbx+0x20],xmm0
mov dword ptr [r12],0


spirit_done:
xor eax,eax
pop r13
pop r12
pop rbx
ret


mana_filter:
push rbx
sub rsp,16
mov rbx,rdi
movss dword ptr [rsp],xmm0
call on_player
test al,al
jz mana_original
movss xmm0,dword ptr [rbx+0x2c]
jmp mana_done
mana_original:
movss xmm0,dword ptr [rsp]
addss xmm0,dword ptr [rbx+0x28]
movss xmm1,dword ptr [rbx+0x2c]
xorps xmm2,xmm2
minss xmm1,xmm0
cmpltss xmm0,xmm2
andnps xmm0,xmm1
mana_done:
add rsp,16
pop rbx
ret


.align 8
control:
.long 1
.float 6.0
```

Label offsets: `{"health_entry":72,"grey_entry":121,"spirit_entry":171,"mana_filter":458,"health_filter":274,"grey_filter":343,"spirit_filter":412,"on_player":220,"control":528}`.

</details>

<details>
<summary>damage: assembly origin 0x47A2240, 336 bytes</summary>

```asm
.quad damage_filter,on_player,control
on_player:
test rdi,rdi
jz on_player_false
cmp qword ptr [rdi+16],0
je on_player_false
push rbx
mov rbx,rdi
lea rax,[rip+0x11223344]
mov rax,qword ptr [rax]
test rax,rax
jz on_player_pop_false
call rax
test rax,rax
jz on_player_pop_false
mov rdi,rax
xor esi,esi
call 8449904
pop rbx
ret
on_player_pop_false:
pop rbx
on_player_false:
xor eax,eax
ret


damage_filter:
push rbx
push r12
push r13
push r14
push r15
sub rsp,16
mov rbx,rdi
mov byte ptr [rsp+8],0
mov rax,qword ptr [rbx+0x28]
mov r12,qword ptr [rax+0x10]
test r12,r12
jz damage_done
mov r13,qword ptr [r12+0x10]
test r13,r13
jz damage_apply
cmp byte ptr [r13+0x35],0
jne damage_apply
mov rdi,qword ptr [rbx+0x10]
test rdi,rdi
jz damage_apply
cmp qword ptr [rdi+16],0
je damage_apply
xor esi,esi
call 8449904
test al,al
jz damage_apply
mov rdi,qword ptr [rbx+0x20]
test rdi,rdi
jz damage_apply
cmp qword ptr [rdi+16],0
je damage_apply
call on_player
test al,al
jnz damage_apply
mov edx,dword ptr [r13+0x10]
mov eax,edx
and eax,0x7fffffff
jz damage_apply
and eax,0x7f800000
cmp eax,0x7f800000
je damage_apply
movss xmm0,dword ptr [r13+0x10]
mov eax,0x40c00000
movd xmm1,eax
mulss xmm0,xmm1
movd eax,xmm0
and eax,0x7f800000
cmp eax,0x7f800000
je damage_apply
mov dword ptr [rsp],edx
mov byte ptr [rsp+8],1
movss dword ptr [r13+0x10],xmm0
mov rax,qword ptr [rbx+0x10]
damage_apply:
mov rax,qword ptr [r12]
mov rdi,r12
mov rsi,qword ptr [rbx+0x30]
mov rdx,qword ptr [rax+0x180]
call qword ptr [rax+0x178]
cmp byte ptr [rsp+8],0
je damage_done
mov eax,dword ptr [rsp]
mov dword ptr [r13+0x10],eax
damage_done:
add rsp,16
pop r15
pop r14
pop r13
pop r12
pop rbx
ret

.align 8
control:
.long 1
.float 6.0
```

Label offsets: `{"damage_filter":78,"on_player":24,"control":328}`.

</details>

<details>
<summary>jump: assembly origin 0x47A23C0, 224 bytes</summary>

```asm
.quad jump_filter,on_player,control
.align 16
jump_filter:
push rbx
sub rsp,16
mov rbx,rdi
movss xmm0,dword ptr [rbx+0x9c]
xor esi,esi
call 7318752
movq qword ptr [rsp],xmm0
movss xmm1,dword ptr [rsp+4]
xorps xmm2,xmm2
ucomiss xmm1,xmm2
jbe jump_done
mov rdi,qword ptr [rbx+0x58]
call on_player
test al,al
jz jump_done
movss xmm1,dword ptr [rsp+4]
mov eax,0x40000000
movd xmm2,eax
mulss xmm1,xmm2
movss dword ptr [rsp+4],xmm1
mov rax,qword ptr [rbx+0x58]
jump_done:
movq xmm0,qword ptr [rsp]
add rsp,16
pop rbx
ret
on_player:

test rdi,rdi
jz on_player_false
cmp qword ptr [rdi+16],0
je on_player_false
push rbx
mov rbx,rdi
lea rax,[rip+0x11223344]
mov rax,qword ptr [rax]
test rax,rax
jz on_player_pop_false
call rax
test rax,rax
jz on_player_pop_false
mov rdi,rax
xor esi,esi
call 8449904
pop rbx
ret
on_player_pop_false:
pop rbx
on_player_false:
xor eax,eax
ret



.align 8
control:
.long 1
.float 2.0
.quad 0,0,0
.float 0,0
```

Label offsets: `{"jump_filter":32,"on_player":127,"control":184}`.

</details>

<details>
<summary>money: assembly origin 0x47A24C0, 148 bytes</summary>

```asm

money_entry:
test rsi,rsi
jz money_original
test rdx,rdx
jle money_original
cmp qword ptr [rsi+16],0
je money_original
mov rax,qword ptr [rsi+24]
test rax,rax
jz money_original
cmp dword ptr [rax+16],4
jne money_original
mov r10,0x36003800330037
cmp qword ptr [rax+20],r10
je currency_match
mov r10,0x38003800330037
cmp qword ptr [rax+20],r10
je currency_match
jmp money_original
currency_match:
push rdi
push rsi
push rdx
push rcx
push r8
push r9
sub rsp,8
xor edx,edx
call 9233072
test rax,rax
js money_restore
cmp rax,100000
jge money_restore
mov r10,100000
sub r10,rax
cmp r10,qword ptr [rsp+32]
jle money_restore
mov qword ptr [rsp+32],r10
money_restore:
add rsp,8
pop r9
pop r8
pop rcx
pop rdx
pop rsi
pop rdi
money_original:
.byte 85,72,137,229,65,87,65,86,65,84,83
jmp 9233467
```

Label offsets: `{"money_entry":0}`.

</details>
