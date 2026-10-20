import sys,json,struct
from pathlib import Path
root=Path(__file__).parent
sys.path.insert(0,str(root.parent/'cheat-verify-deps'))
from keystone import Ks,KS_ARCH_X86,KS_MODE_64
helper=(root/'combat-hook.asm').read_text().split('on_player:',1)[1].split('health_filter:',1)[0]
asm='''
.quad jump_filter,control
.align 16
jump_filter:
push rbx
sub rsp,16
mov rbx,rdi
movss xmm0,dword ptr [rbx+0x9c]
xor esi,esi
mov rax,0x8089ace0
call rax
movq qword ptr [rsp],xmm0
cmp dword ptr [rip+control],0
je jump_done
movss xmm1,dword ptr [rsp+4]
xorps xmm2,xmm2
ucomiss xmm1,xmm2
jbe jump_done
mov rdi,qword ptr [rbx+0x58]
call on_player
test al,al
jz jump_done
movss xmm1,dword ptr [rsp+4]
movss dword ptr [rip+control+32],xmm1
mulss xmm1,dword ptr [rip+control+4]
movss dword ptr [rsp+4],xmm1
movss dword ptr [rip+control+36],xmm1
inc qword ptr [rip+control+8]
mov rax,qword ptr [rbx+0x58]
mov qword ptr [rip+control+16],rax
mov qword ptr [rip+control+24],rbx
jump_done:
movq xmm0,qword ptr [rsp]
add rsp,16
pop rbx
ret
on_player:
'''+helper+'''
.align 8
control:
.long 1
.float 2.0
.quad 0,0,0
.float 0,0
'''
machine,_=Ks(KS_ARCH_X86,KS_MODE_64).asm(asm,as_bytes=True)
entry,control=struct.unpack('<QQ',machine[:16])
manifest={'Size':len(machine),'Offsets':{'jump_filter':entry,'control':control},'Sites':[{'Name':'jump','Address':'0x8089C9C7','Original':'C5FA10839C0000004C8B73584889DFE805E3FFFF','Length':20}],'DamageMultiplier':0,'ModuleBase':'0x801A0000','HeightMultiplier':4}
(root/'jump-hook.bin').write_bytes(machine)
(root/'jump-hook.asm').write_text(asm,encoding='utf-8')
(root/'jump-hook.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('COMPILED',len(machine),'bytes; entry',entry,'control',control)
