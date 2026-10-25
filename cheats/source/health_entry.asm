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
