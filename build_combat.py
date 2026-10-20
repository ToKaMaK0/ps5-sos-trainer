import sys,json,struct
from pathlib import Path
root=Path(__file__).parent
sys.path.insert(0,str(root.parent/'cheat-verify-deps'))
from keystone import Ks,KS_ARCH_X86,KS_MODE_64
sites=json.loads((root/'combat-sites.json').read_text(encoding='utf-8-sig'))
labels=['health_entry','grey_entry','spirit_entry','mana_filter','damage_filter','control','on_player','health_filter','grey_filter','spirit_filter']
parts=['.quad '+','.join(labels),'.align 16']
for row in sites[:3]:
    name=row['Name']
    original=bytes.fromhex(row['Original'])
    continuation=int(row['Address'],16)+len(original)
    parts.append(f'''
{name}_entry:
push rdi
push rsi
push rdx
sub rsp,16
movss dword ptr [rsp],xmm0
mov rcx,rsp
call {name}_filter
movss xmm0,dword ptr [rsp]
add rsp,16
pop rdx
pop rsi
pop rdi
.byte {','.join(str(x) for x in original)}
jmp qword ptr [rip]
.quad {continuation}
''')
parts.append('''
on_player:
test rdi,rdi
jz on_player_false
cmp qword ptr [rdi+16],0
je on_player_false
push rbx
mov rbx,rdi
mov rax,0x8643c8f0
mov rax,qword ptr [rax]
test rax,rax
jz on_player_pop_false
call rax
test rax,rax
jz on_player_pop_false
mov rdi,rax
xor esi,esi
mov rax,0x809aef70
call rax
pop rbx
ret
on_player_pop_false:
pop rbx
on_player_false:
xor eax,eax
ret
''')
for kind in ['health','grey','spirit']:
    count={'health':8,'grey':16,'spirit':24}[kind]
    pointer=56 if kind=='spirit' else 48
    parts.append(f'''
{kind}_filter:
push rbx
push r12
push r13
mov rbx,rdi
mov r12,rcx
cmp dword ptr [rip+control],0
je {kind}_done
call on_player
test al,al
jz {kind}_done
inc qword ptr [rip+control+{count}]
mov qword ptr [rip+control+{pointer}],rbx
''')
    if kind=='spirit':
        parts.append('''
movss xmm0,dword ptr [rbx+0x24]
movss dword ptr [rbx+0x20],xmm0
mov dword ptr [r12],0
''')
    else:
        jump='jbe' if kind=='grey' else 'jae'
        parts.append(f'''
movss xmm0,dword ptr [rbx+0x38]
movss dword ptr [rbx+0x40],xmm0
mov dword ptr [rbx+0x44],0
xorps xmm1,xmm1
movss xmm0,dword ptr [r12]
ucomiss xmm0,xmm1
jp {kind}_done
{jump} {kind}_done
mov dword ptr [r12],0
''')
    parts.append(f'''
{kind}_done:
xor eax,eax
pop r13
pop r12
pop rbx
ret
''')
parts.append('''
mana_filter:
push rbx
sub rsp,16
mov rbx,rdi
movss dword ptr [rsp],xmm0
cmp dword ptr [rip+control],0
je mana_original
call on_player
test al,al
jz mana_original
inc qword ptr [rip+control+32]
mov qword ptr [rip+control+64],rbx
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
cmp dword ptr [rip+control],0
je damage_apply
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
mov rax,0x809aef70
call rax
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
mulss xmm0,dword ptr [rip+control+4]
movd eax,xmm0
and eax,0x7f800000
cmp eax,0x7f800000
je damage_apply
mov dword ptr [rsp],edx
mov byte ptr [rsp+8],1
movss dword ptr [r13+0x10],xmm0
inc qword ptr [rip+control+40]
mov rax,qword ptr [rbx+0x10]
mov qword ptr [rip+control+72],rax
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
.quad 0,0,0,0,0,0,0,0,0
''')
asm='\n'.join(parts)
machine,_=Ks(KS_ARCH_X86,KS_MODE_64).asm(asm,as_bytes=True)
offsets=dict(zip(labels,struct.unpack('<'+str(len(labels))+'Q',machine[:8*len(labels)])))
assert len(machine)<0x4000
(root/'combat-hook.bin').write_bytes(machine)
(root/'combat-hook.asm').write_text(asm,encoding='utf-8')
manifest={'Size':len(machine),'Offsets':offsets,'Sites':sites,'DamageMultiplier':6,'ModuleBase':'0x801A0000'}
(root/'combat-hook.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('COMPILED',len(machine),'bytes;',offsets)
