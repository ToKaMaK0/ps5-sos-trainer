.quad health_entry,grey_entry,spirit_entry,mana_filter,damage_filter,control,on_player,health_filter,grey_filter,spirit_filter
.align 16

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
jmp qword ptr [rip]
.quad 2163520860


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
jmp qword ptr [rip]
.quad 2163522301


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
jmp qword ptr [rip]
.quad 2163482812


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


health_filter:
push rbx
push r12
push r13
mov rbx,rdi
mov r12,rcx
cmp dword ptr [rip+control],0
je health_done
call on_player
test al,al
jz health_done
inc qword ptr [rip+control+8]
mov qword ptr [rip+control+48],rbx


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
cmp dword ptr [rip+control],0
je grey_done
call on_player
test al,al
jz grey_done
inc qword ptr [rip+control+16]
mov qword ptr [rip+control+48],rbx


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
cmp dword ptr [rip+control],0
je spirit_done
call on_player
test al,al
jz spirit_done
inc qword ptr [rip+control+24]
mov qword ptr [rip+control+56],rbx


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
