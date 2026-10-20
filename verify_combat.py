import sys,json,struct,math
from pathlib import Path
root=Path(__file__).parent
sys.path.insert(0,str(root.parent/'cheat-verify-deps'))
from unicorn import *
from unicorn.x86_const import *
from capstone import *
meta=json.loads((root/'combat-hook.json').read_text())
blob=(root/'combat-hook.bin').read_bytes()
code,heap,stack,ret=0x300000000,0x400000000,0x700000000,0x500000000
getter,isplayer,apply=0x600000000,0x809aef70,0x600001000
ptrslot=0x8643c8f0
q=lambda n:struct.pack('<Q',n)
f=lambda n:struct.pack('<f',n)
def setup(player=True,active=True,own_target=False,source_player=True):
    u=Uc(UC_ARCH_X86,UC_MODE_64)
    for a,s in [(code,0x4000),(heap,0x10000),(stack,0x10000),(ret,0x1000),(getter,0x2000),(isplayer&~4095,0x1000),(ptrslot&~4095,0x1000)]:u.mem_map(a,s)
    u.mem_write(code,blob);u.mem_write(ptrslot,q(getter))
    for address in [getter,isplayer,apply]:u.mem_write(address,b'\xc3')
    u.mem_write(code+meta['Offsets']['control'],struct.pack('<I',int(active)))
    obj,hero,enemy,target,module,config,klass,args,hit,hitconfig=[heap+x for x in [0x100,0x1000,0x1100,0x1200,0x2000,0x3000,0x4000,0x5000,0x6000,0x7000]]
    for x in [obj,hero,enemy,target]:u.mem_write(x+16,q(heap+0x9000))
    u.mem_write(obj+0x38,f(200));u.mem_write(obj+0x40,f(20));u.mem_write(obj+0x44,f(10))
    u.mem_write(obj+0x20,f(.5));u.mem_write(obj+0x24,f(5));u.mem_write(obj+0x28,f(3));u.mem_write(obj+0x2c,f(40))
    u.mem_write(hit+0x10,q(hero if source_player else enemy));u.mem_write(hit+0x20,q(target));u.mem_write(hit+0x28,q(hitconfig));u.mem_write(hit+0x30,q(args))
    u.mem_write(hitconfig+0x10,q(module));u.mem_write(module,q(klass));u.mem_write(module+0x10,q(config));u.mem_write(klass+0x178,q(apply));u.mem_write(klass+0x180,q(0x123456));u.mem_write(config+0x10,f(10))
    applied=[]
    def native(u,a,size,_):
        if a not in [getter,isplayer,apply]:return
        sp=u.reg_read(UC_X86_REG_RSP);assert sp%16==8,('alignment',hex(a),hex(sp))
        rdi,rsi,rdx=[u.reg_read(r) for r in [UC_X86_REG_RDI,UC_X86_REG_RSI,UC_X86_REG_RDX]]
        if a==getter:
            assert rdi in [obj,target]
            result=hero if (player if rdi==obj else own_target) else enemy
        elif a==isplayer:assert rsi==0;result=int(rdi==hero)
        else:
            assert rdi==module and rsi==args and rdx==0x123456
            applied.append(struct.unpack('<f',u.mem_read(config+16,4))[0]);result=0
        target_rip=struct.unpack('<Q',u.mem_read(sp,8))[0]
        for r in [UC_X86_REG_RDI,UC_X86_REG_RSI,UC_X86_REG_RDX,UC_X86_REG_RCX,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11]:u.reg_write(r,0xdeadbeef)
        for r in [UC_X86_REG_XMM0,UC_X86_REG_XMM1,UC_X86_REG_XMM2,UC_X86_REG_XMM3,UC_X86_REG_XMM4,UC_X86_REG_XMM5]:u.reg_write(r,0)
        u.reg_write(UC_X86_REG_RAX,result);u.reg_write(UC_X86_REG_RSP,sp+8);u.reg_write(UC_X86_REG_RIP,target_rip)
    u.hook_add(UC_HOOK_CODE,native)
    def run(label,amount=-7,damage=False):
        save={r:i+0x1234 for i,r in enumerate([UC_X86_REG_RBP,UC_X86_REG_RBX,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15])}
        for r,v in save.items():u.reg_write(r,v)
        sp=stack+0xfff8;u.mem_write(sp,q(ret));u.reg_write(UC_X86_REG_RSP,sp)
        u.reg_write(UC_X86_REG_RDI,hit if damage else obj)
        u.reg_write(UC_X86_REG_RSI,0xabc);u.reg_write(UC_X86_REG_RDX,0xdef)
        u.mem_write(heap+0x8000,f(amount));u.reg_write(UC_X86_REG_RCX,heap+0x8000)
        u.reg_write(UC_X86_REG_XMM0,struct.unpack('<I',f(amount))[0])
        try:u.emu_start(code+meta['Offsets'][label],ret,count=10000)
        except UcError:
            print('EMU ERROR',label,'rip',hex(u.reg_read(UC_X86_REG_RIP)),'rsp',hex(u.reg_read(UC_X86_REG_RSP)))
            raise
        assert u.reg_read(UC_X86_REG_RIP)==ret and u.reg_read(UC_X86_REG_RSP)==sp+8
        for r,v in save.items():assert u.reg_read(r)==v,('preservation',r)
    def readfloat(a):return struct.unpack('<f',u.mem_read(a,4))[0]
    return u,obj,config,applied,run,readfloat

count=0
for mode in ['health','grey','spirit']:
    for player in [True,False]:
        for active in [True,False]:
            for amount in [-7,7]:
                u,obj,config,applied,run,r=setup(player,active)
                run(mode+'_filter',amount)
                if mode=='spirit':assert r(obj+0x20)==(5 if player and active else .5)
                else:
                    assert r(obj+0x40)==(200 if player and active else 20)
                    assert r(obj+0x44)==(0 if player and active else 10)
                expect=0 if player and active and (mode=='spirit' or (amount<0 if mode=='health' else amount>0)) else amount
                assert r(heap+0x8000)==expect,(mode,player,active,amount,r(heap+0x8000))
                count+=1
for player in [True,False]:
    for active in [True,False]:
        for amount in [-100,2,100]:
            u,obj,config,applied,run,r=setup(player,active)
            run('mana_filter',amount)
            value=struct.unpack('<f',struct.pack('<I',u.reg_read(UC_X86_REG_XMM0)&0xffffffff))[0]
            assert value==(40 if player and active else max(0,min(40,3+amount)))
            count+=1
for source_player in [True,False]:
    for own_target in [True,False]:
        for active in [True,False]:
            for value in [0,10,-10,float('inf'),float('nan'),3e38]:
                u,obj,config,applied,run,r=setup(True,active,own_target,source_player)
                u.mem_write(config+16,f(value));original=bytes(u.mem_read(config+16,4))
                run('damage_filter',damage=True)
                assert len(applied)==1 and bytes(u.mem_read(config+16,4))==original
                expected=value*6 if active and source_player and not own_target and math.isfinite(value) and abs(value)<1e38 else value
                assert (math.isnan(expected) and math.isnan(applied[0])) or applied[0]==struct.unpack('<f',f(expected))[0],(source_player,own_target,active,value,applied)
                count+=1
u,obj,config,applied,run,r=setup();u.mem_write(config+0x35,b'\1');run('damage_filter',damage=True);assert applied==[10];count+=1
print('PASS',count,'scenarios: player/enemy, enabled/disabled, HP/grey HP/spirit/mana, damage x6, self damage, finite guards, shared damage restoration, SysV registers and stack.')
