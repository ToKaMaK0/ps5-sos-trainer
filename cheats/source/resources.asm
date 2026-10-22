.quad entry,flag_0,flag_1,flag_2,flag_3,flag_4,flag_5,flag_6,flag_7,flag_8,flag_9,flag_10,flag_11,flag_12,flag_13,flag_14,flag_15,flag_16,flag_17,flag_18,flag_19,flag_20,flag_21,flag_22
entry:
test rdi,rdi
jz getter_original
test rsi,rsi
jz getter_original
cmp qword ptr [rsi+16],0
je getter_original
cmp dword ptr [rsi+0x48],1
jne getter_original
mov rax,qword ptr [rsi+24]
test rax,rax
jz getter_original
cmp dword ptr [rax+16],4
jne getter_original
mov r10,0x38003800330037
cmp qword ptr [rax+20],r10
jne next_0
cmp dword ptr [rsi+0x4c],2
jne getter_original
flag_0:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,100000
jmp material_match
next_0:
mov r10,0x36003800330037
cmp qword ptr [rax+20],r10
jne next_1
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_1:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,100000
jmp material_match
next_1:
mov r10,0x30003900330037
cmp qword ptr [rax+20],r10
jne next_2
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_2:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_2:
mov r10,0x32003900330037
cmp qword ptr [rax+20],r10
jne next_3
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_3:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_3:
mov r10,0x32003000340037
cmp qword ptr [rax+20],r10
jne next_4
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_4:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_4:
mov r10,0x34003000340037
cmp qword ptr [rax+20],r10
jne next_5
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_5:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_5:
mov r10,0x34003100340037
cmp qword ptr [rax+20],r10
jne next_6
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_6:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_6:
mov r10,0x36003100340037
cmp qword ptr [rax+20],r10
jne next_7
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_7:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_7:
mov r10,0x38003100340037
cmp qword ptr [rax+20],r10
jne next_8
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_8:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_8:
mov r10,0x30003200340037
cmp qword ptr [rax+20],r10
jne next_9
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_9:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_9:
mov r10,0x32003200340037
cmp qword ptr [rax+20],r10
jne next_10
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_10:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_10:
mov r10,0x34003900330037
cmp qword ptr [rax+20],r10
jne next_11
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_11:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_11:
mov r10,0x36003900330037
cmp qword ptr [rax+20],r10
jne next_12
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_12:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_12:
mov r10,0x38003900330037
cmp qword ptr [rax+20],r10
jne next_13
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_13:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_13:
mov r10,0x36003000340037
cmp qword ptr [rax+20],r10
jne next_14
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_14:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_14:
mov r10,0x38003000340037
cmp qword ptr [rax+20],r10
jne next_15
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_15:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_15:
mov r10,0x30003100340037
cmp qword ptr [rax+20],r10
jne next_16
cmp dword ptr [rsi+0x4c],1
jne getter_original
flag_16:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_16:
mov r10,0x30003300340037
cmp qword ptr [rax+20],r10
jne next_17
cmp dword ptr [rsi+0x4c],11
jne getter_original
flag_17:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_17:
mov r10,0x34003400340037
cmp qword ptr [rax+20],r10
jne next_18
cmp dword ptr [rsi+0x4c],11
jne getter_original
flag_18:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_18:
mov r10,0x34003600340037
cmp qword ptr [rax+20],r10
jne next_19
cmp dword ptr [rsi+0x4c],11
jne getter_original
flag_19:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_19:
mov r10,0x36003400340037
cmp qword ptr [rax+20],r10
jne next_20
cmp dword ptr [rsi+0x4c],11
jne getter_original
flag_20:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_20:
mov r10,0x38003200340037
cmp qword ptr [rax+20],r10
jne next_21
cmp dword ptr [rsi+0x4c],11
jne getter_original
flag_21:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_21:
mov r10,0x38003400340037
cmp qword ptr [rax+20],r10
jne next_22
cmp dword ptr [rsi+0x4c],11
jne getter_original
flag_22:
mov r10d,0
test r10d,r10d
jz getter_original
mov r11d,1000
jmp material_match
next_22:
jmp getter_original
material_match:
push rbx
push r12
push r13
push r14
sub rsp,8
mov rbx,rdi
mov r12,rsi
mov r13,rdx
mov r14,r11
call getter_original
test rax,rax
js material_done
cmp rax,r14
jge material_done
mov rdx,r14
sub rdx,rax
mov rdi,rbx
mov rsi,r12
xor ecx,ecx
call 9232624
mov rdi,rbx
mov rsi,r12
mov rdx,r13
call getter_original
material_done:
add rsp,8
pop r14
pop r13
pop r12
pop rbx
ret
getter_original:
.byte 85,72,137,229,65,87,65,86,83,80
jmp 9233082
