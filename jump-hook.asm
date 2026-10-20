
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



.align 8
control:
.long 1
.float 2.0
.quad 0,0,0
.float 0,0
