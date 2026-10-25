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
mov eax,0x42480000
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
.float 50.0
