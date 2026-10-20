import sys,struct,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent/'cheat-verify-deps'))
from unicorn import Uc,UC_ARCH_X86,UC_MODE_64,UC_HOOK_CODE
from unicorn.x86_const import *
root=Path(__file__).parent
blob=(root/'money-test.bin').read_bytes()
base,heap,stack,end=0x300000000,0x400000000,0x700000000,0x500000000
imagebase=0x801a0000
functions={k:imagebase+v for k,v in {'pawn':0x5d12d0,'wallet':0x8c0810,'string':0x32fac0,'item':0x8c91b0,'amount':0x8ce2b0,'add':0x8ce430}.items()}
q=lambda n:struct.pack('<Q',n)
def run(initial=(356,512),failure=None):
    u=Uc(UC_ARCH_X86,UC_MODE_64)
    for p,size in [(base,0x4000),(heap,0x10000),(stack,0x10000),(end,0x1000)]:u.mem_map(p,size)
    for p in set(v&~4095 for v in functions.values()):u.mem_map(p,4096)
    for v in functions.values():u.mem_write(v,b'\xc3')
    u.mem_write(base,blob)
    controller,pawn,wallet,item0,item1=heap+0x100,heap+0x200,heap+0x300,heap+0x400,heap+0x500
    for p in [item0,item1]:u.mem_write(p+16,q(heap+0x9000))
    amounts=list(initial);added=[];calls=[]
    def native(u,addr,size,_):
        if addr not in functions.values():return
        name=next(k for k,v in functions.items() if v==addr);calls.append(name)
        assert u.reg_read(UC_X86_REG_RSP)%16==8
        rdi,rsi,rdx,rcx,r8=[u.reg_read(r) for r in [UC_X86_REG_RDI,UC_X86_REG_RSI,UC_X86_REG_RDX,UC_X86_REG_RCX,UC_X86_REG_R8]]
        result=0
        if name=='pawn':assert rdi==controller and rsi==0;result=0 if failure=='pawn' else pawn
        elif name=='wallet':assert rdi==pawn and rsi==0;result=0 if failure=='wallet' else wallet
        elif name=='string':
            raw=bytes(u.mem_read(rdi,64)).split(b'\0')[0]
            i=[b'loot_currency',b'loot_orb_red'].index(raw);result=heap+0x1000+i*0x100
        elif name=='item':
            assert rsi==0;i=(rdi-(heap+0x1000))//0x100
            result=0 if failure=='item'+str(i) else [item0,item1][i]
        elif name=='amount':
            assert rdi==wallet and rdx==0;i=[item0,item1].index(rsi);result=amounts[i]
        elif name=='add':
            assert rdi==wallet and rcx==0x101 and r8==0
            i=[item0,item1].index(rsi);assert rdx==100000-amounts[i] and rdx>0
            added.append(i)
            if failure!='add'+str(i):amounts[i]+=rdx
        u.reg_write(UC_X86_REG_RAX,result&((1<<64)-1))
    u.hook_add(UC_HOOK_CODE,native)
    preserved={r:0x1234+i for i,r in enumerate([UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15])}
    sp=stack+0x8008
    def execute():
        for r,v in preserved.items():u.reg_write(r,v)
        u.mem_write(sp,q(end));u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RDI,controller)
        u.emu_start(base,end,count=10000)
        assert u.reg_read(UC_X86_REG_RSP)==sp+8
        assert all(u.reg_read(r)==v for r,v in preserved.items())
    execute();status=struct.unpack('<I',u.mem_read(base+0x2000,4))[0]
    if failure or any(v<0 or v>1000000 for v in initial):
        assert status==3
        if not (failure or '').startswith('add'):assert added==[]
    else:
        assert status==2 and amounts==[max(100000,v) for v in initial]
        assert struct.unpack('<qq',u.mem_read(base+0x2060,16))==tuple(amounts)
    before=len(calls);execute();assert before==len(calls),'One-shot executed twice'
cases=0
for initial in itertools.product([0,356,99999,100000,1000000],repeat=2):run(initial);cases+=1
for initial in [(-1,0),(0,-1),(1000001,0),(0,1000001)]:run(initial);cases+=1
for failure in ['pawn','wallet','item0','item1','add0','add1']:run(failure=failure);cases+=1
print(f'PASS {cases} wallet scenarios: validation before writes, target amounts, readback, one-shot, main-thread ABI and failures.')
