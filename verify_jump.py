import sys,json,struct,math
from pathlib import Path
root=Path(__file__).parent
sys.path.insert(0,str(root.parent/'cheat-verify-deps'))
from unicorn import *
from unicorn.x86_const import *
meta=json.loads((root/'jump-hook.json').read_text());blob=(root/'jump-hook.bin').read_bytes()
code,heap,stack,end=0x300000000,0x400000000,0x700000000,0x500000000
angle,getter,isplayer,ptrslot=0x8089ace0,0x600000000,0x809aef70,0x8643c8f0
q=lambda x:struct.pack('<Q',x)
f=lambda x:struct.pack('<f',x)
cases=0
for player in [True,False]:
  for active in [True,False]:
    for movement in [heap+0x200,0]:
      for x,y in [(0.3,1),(-.25,.5),(1,-1),(0,0),(0,float('nan'))]:
        u=Uc(UC_ARCH_X86,UC_MODE_64)
        for a,s in [(code,0x4000),(heap,0x10000),(stack,0x10000),(end,0x1000),(angle&~4095,0x1000),(getter,0x1000),(isplayer&~4095,0x1000),(ptrslot&~4095,0x1000)]:u.mem_map(a,s)
        for a in [angle,getter,isplayer]:u.mem_write(a,b'\xc3')
        u.mem_write(code,blob);u.mem_write(ptrslot,q(getter));u.mem_write(code+meta['Offsets']['control'],struct.pack('<I',int(active)))
        obj=heap+0x100;u.mem_write(obj+0x58,q(movement));u.mem_write(obj+0x9c,f(.25))
        u.mem_write(heap+0x210,q(heap+0x9000))
        def callback(u,a,s,_):
            if a not in [angle,getter,isplayer]:return
            sp=u.reg_read(UC_X86_REG_RSP);assert sp%16==8
            rdi=u.reg_read(UC_X86_REG_RDI);result=0
            if a==angle:
                assert rdi==obj and u.reg_read(UC_X86_REG_RSI)==0
                assert u.reg_read(UC_X86_REG_XMM0)&0xffffffff==struct.unpack('<I',f(.25))[0]
                vector=struct.unpack('<Q',struct.pack('<ff',x,y))[0]
            elif a==getter:assert rdi==movement;result=heap+(0x1000 if player else 0x1100);vector=0
            else:assert rdi in [heap+0x1000,heap+0x1100];result=int(rdi==heap+0x1000);vector=0
            ret=struct.unpack('<Q',u.mem_read(sp,8))[0]
            for r in [UC_X86_REG_RDI,UC_X86_REG_RSI,UC_X86_REG_RDX,UC_X86_REG_RCX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11]:u.reg_write(r,0xdeadbeef)
            for r in [UC_X86_REG_XMM0,UC_X86_REG_XMM1,UC_X86_REG_XMM2,UC_X86_REG_XMM3]:u.reg_write(r,0)
            u.reg_write(UC_X86_REG_XMM0,vector);u.reg_write(UC_X86_REG_RAX,result);u.reg_write(UC_X86_REG_RSP,sp+8);u.reg_write(UC_X86_REG_RIP,ret)
        u.hook_add(UC_HOOK_CODE,callback)
        saved={r:0x1234+i for i,r in enumerate([UC_X86_REG_RBP,UC_X86_REG_RBX,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15])}
        for r,v in saved.items():u.reg_write(r,v)
        sp=stack+0xfff8;u.mem_write(sp,q(end));u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RDI,obj)
        u.emu_start(code+meta['Offsets']['jump_filter'],end,count=10000)
        assert u.reg_read(UC_X86_REG_RIP)==end and u.reg_read(UC_X86_REG_RSP)==sp+8
        assert all(u.reg_read(r)==v for r,v in saved.items())
        actual=struct.unpack('<ff',q(u.reg_read(UC_X86_REG_XMM0)&0xffffffffffffffff))
        changed=player and active and movement!=0 and y>0
        expected_y=y*2 if changed else y
        assert actual[0]==struct.unpack('<f',f(x))[0]
        assert math.isnan(actual[1]) if math.isnan(expected_y) else actual[1]==expected_y
        count=struct.unpack('<Q',u.mem_read(code+meta['Offsets']['control']+8,8))[0]
        assert count==int(changed)
        cases+=1
print('PASS',cases,'scenarios: only upward player jumps scaled; horizontal direction, enemies, downward launches, disabled mode, null context, NaN and SysV ABI verified.')
