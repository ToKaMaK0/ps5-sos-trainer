// SPDX-License-Identifier: GPL-2.0-only
// SoS Trainer, 2026. See LICENSE.txt and CREDITS.txt.
using System.Reflection;
using System.Text;
using System.Text.Json;
using libdebug;

Console.OutputEncoding=Encoding.UTF8;
try
{
    if(args.Length==1 && args[0]=="--self-test"){Trainer.SelfTest();return;}
    if(args.Length==1 && args[0]=="--license"){Trainer.License();return;}
    bool interactive=args.Length==0;
    Console.WriteLine("God of War Sons of Sparta · PPSA28997 · 01.008.001\nTrainer 0.1.0 · ps5debug-NG, port 744");
    Console.WriteLine("GPL-2.0-only · No warranty · --license for credits and license.");
    string ip;
    if(interactive){Console.Write("IP PS5: ");ip=Console.ReadLine()?.Trim()??"";}
    else {if(args.Length!=2)throw new ArgumentException("Usage: SoS-Trainer.exe --status|--combat-on|--combat-off|--jump-on|--jump-off|--damage-on|--money IP");ip=args[1];}
    if(!System.Net.IPAddress.TryParse(ip,out _))throw new ArgumentException("Неверный IP.");
    do
    {
        string command;
        if(interactive)
        {
            Console.WriteLine("\n1 — Здоровье + дух + магия без расхода (урон ×1)\n2 — Отключить боевые эффекты\n3 — Высокий прыжок (~×4 высота)\n4 — Отключить высокий прыжок\n5 — Урон ×6 + боевые эффекты\n6 — Довести две валюты до 100 000\n7 — Проверить состояние\n0 — Выход\nСюжет, снаряжение и навыки программа не открывает.\nПрыжок может позволить обойти сюжетный проход. Валюты применяйте отдельно.");
            Console.Write("> ");
            command=Console.ReadLine()?.Trim() switch {"1"=>"--combat-on","2"=>"--combat-off","3"=>"--jump-on","4"=>"--jump-off","5"=>"--damage-on","6"=>"--money","7"=>"--status","0" or null=>"exit",_=>"invalid"};
            if(command=="exit")break;
            if(command=="invalid")continue;
        }
        else command=args[0];
        try {using var trainer=new Trainer(ip);trainer.Execute(command);}
        catch(Exception ex){Console.WriteLine("Операция остановлена: "+ex.Message);if(!interactive)throw;}
    }while(interactive);
}
catch(Exception ex){Console.Error.WriteLine(ex.Message);Environment.ExitCode=1;}

sealed class Trainer:IDisposable
{
    const ulong OldBase=0x801a0000;
    readonly PS4DBG d;
    readonly int pid;
    readonly ulong imageBase;
    readonly Hook[] hooks;
    bool attached;
    public Trainer(string ip)
    {
        d=new PS4DBG(ip);
        try
        {
            d.Connect();
            var games=d.GetProcessList().processes.Where(p=>p.name=="eboot.bin").Where(p=>d.GetProcessInfo(p.pid).titleid=="PPSA28997").ToArray();
            if(games.Length!=1)throw new Exception("Запустите PPSA28997 и загрузите персонажа. Нужен ровно один процесс игры.");
            pid=games[0].pid;
            var text=d.GetProcessMaps(pid).entries.Where(m=>m.name.Contains("Il2CppUserAssemblies") && (m.prot&4)!=0).OrderBy(m=>m.start).ToArray();
            if(text.Length==0 || text[0].start<0x10000)throw new Exception("Модуль Il2CppUserAssemblies не найден.");
            imageBase=text[0].start-0x10000;
            hooks=[Load("combat"),Load("jump")];
            foreach(var h in hooks)Discover(h);
            CheckFingerprints();
            Console.WriteLine($"Игра найдена: PID {pid}, база 0x{imageBase:X}; отпечатки кода совпали.");
        }
        catch {d.Disconnect();throw;}
    }
    Hook Load(string name)
    {
        var spec=JsonSerializer.Deserialize<Spec>(Resource(name+"-hook.json"))!;
        byte[] code=Resource(name+"-hook.bin");
        if(code.Length!=spec.Size || spec.Size>=0x4000)throw new Exception("Повреждён встроенный payload.");
        Relocate(code,spec,name,imageBase);
        // Native state is transient. Never increase persistent character statistics.
        if(name=="combat")BitConverter.GetBytes(1f).CopyTo(code,(int)spec.Offsets["control"]+4);
        return new Hook(name,spec,code);
    }
    static byte[] Resource(string suffix)
    {
        var asm=Assembly.GetExecutingAssembly();
        using var stream=asm.GetManifestResourceStream(asm.GetManifestResourceNames().Single(n=>n.EndsWith("."+suffix,StringComparison.Ordinal)))!;
        using var data=new MemoryStream();stream.CopyTo(data);return data.ToArray();
    }
    public static void License(){Console.WriteLine(Encoding.UTF8.GetString(Resource("LICENSE.txt")));Console.WriteLine(Encoding.UTF8.GetString(Resource("CREDITS.txt")));}
    static void Relocate(byte[] code,Spec spec,string name,ulong targetBase)
    {
        var targets=new Dictionary<ulong,int>{{0x8643c8f0,1},{0x809aef70,name=="combat"?2:1}};
        if(name=="jump")targets[0x8089ace0]=1;
        else foreach(var s in spec.Sites.Take(3))targets[Parse(s.Address)+(ulong)s.Length]=1;
        foreach(var pair in targets)
        {
            byte[] source=BitConverter.GetBytes(pair.Key);int count=0;
            for(int i=0;i<=code.Length-8;i++)if(code.AsSpan(i,8).SequenceEqual(source))
            {BitConverter.GetBytes(targetBase+(pair.Key-OldBase)).CopyTo(code,i);count++;i+=7;}
            if(count!=pair.Value)throw new Exception($"Недопустимая таблица релокаций {name}: {pair.Key:X}, {count}.");
        }
    }
    ulong SiteAddress(Site s)=>imageBase+(Parse(s.Address)-OldBase);
    static ulong Parse(string s)=>Convert.ToUInt64(s[2..],16);
    byte[] Patch(Hook h,Site s,ulong allocation)
    {
        string label=s.Name is "mana" or "damage" or "jump"?s.Name+"_filter":s.Name+"_entry";
        ulong fn=allocation+h.Spec.Offsets[label];
        byte[] bytes=s.Name=="jump"?[0x4c,0x8b,0x73,0x58,0x48,0x89,0xdf,0x48,0xb8,..BitConverter.GetBytes(fn),0xff,0xd0]:s.Name is "mana" or "damage"?[0x48,0x89,0xdf,0x48,0xb8,..BitConverter.GetBytes(fn),0xff,0xd0]:[0x48,0xb8,..BitConverter.GetBytes(fn),0xff,0xe0];
        return [..bytes,..Enumerable.Repeat((byte)0x90,s.Length-bytes.Length)];
    }
    void Discover(Hook h)
    {
        ulong candidate=0;int installed=0;
        foreach(var s in h.Spec.Sites)
        {
            var b=d.ReadMemory(pid,SiteAddress(s),s.Length);
            if(b.SequenceEqual(Convert.FromHexString(s.Original)))continue;
            int at=s.Name=="jump"?9:s.Name is "mana" or "damage"?5:2;
            string label=s.Name is "mana" or "damage" or "jump"?s.Name+"_filter":s.Name+"_entry";
            ulong target=BitConverter.ToUInt64(b,at);
            if(target<h.Spec.Offsets[label])throw new Exception("Неизвестная модификация: "+s.Name);
            ulong found=target-h.Spec.Offsets[label];
            if(found==0 || found%0x4000!=0 || !b.SequenceEqual(Patch(h,s,found)) || (candidate!=0 && candidate!=found))throw new Exception("Неизвестная модификация: "+s.Name);
            candidate=found;installed++;
        }
        if(installed!=0 && installed!=h.Spec.Sites.Length)throw new Exception("Неполный набор хуков: "+h.Name);
        if(installed==0)return;
        int size=(int)h.Spec.Offsets["control"];
        if(!d.ReadMemory(pid,candidate,size).SequenceEqual(h.Image[..size]))throw new Exception("Проверка существующего payload не прошла: "+h.Name);
        h.Allocation=candidate;
    }
    void CheckFingerprints()
    {
        (ulong Hash,(uint,uint)[] Ranges)[] sets=[
            (0x4b6beba820a6ebce,[(0x80ecd0,0x80f0b0),(0xdab1a0,0xdab6b0),(0xdabaf0,0xdabd90)]),
            (0xb0e9d2c9cfd2a0b1,[(0xda20b0,0xda2520),(0xda2b10,0xda2d10),(0x80ecd0,0x80f0b0)]),
            (0xa63f97d69c46ad8d,[(0xd954f0,0xd95bd0),(0xdf2980,0xdf2bc0),(0x823d20,0x823e30),(0xc26550,0xc26750),(0xc1af20,0xc1afe0),(0x80ecd0,0x80f0b0)]),
            (0x7b452922017e03ec,[(0xd91d00,0xd92910),(0xd83100,0xd837d0),(0xdf3900,0xdf3be0),(0xdf3e60,0xdf4e00),(0xdf98d0,0xdf9af0),(0xd94d70,0xd95120),(0x80ecd0,0x80f0b0)]),
            (0x6b8174068fca8cd1,[(0x6fc450,0x6fcbf0),(0x6face0,0x6fb1b0),(0x6efe80,0x6f0180),(0x6f0810,0x6f08e0),(0x708d70,0x709360),(0x80ecd0,0x80f0b0)]),
            (0xdcbbc10a00bb8f1e,[(0x32fac0,0x32fae0),(0x5d12d0,0x5d1390),(0x5d35c0,0x5d35d0),(0x8c0810,0x8c0950),(0x8c91b0,0x8c92b0),(0x8ce0f0,0x8ce6d0),(0x996d20,0x996e70),(0x9971b0,0x997390),(0xd11230,0xd11300)])];
        foreach(var set in sets)
        {
            ulong hash=0xcbf29ce484222325;
            foreach(var r in set.Ranges)
            {
                ulong start=imageBase+r.Item1;var bytes=d.ReadMemory(pid,start,(int)(r.Item2-r.Item1));
                foreach(var h in hooks.Where(h=>h.Allocation!=0))foreach(var s in h.Spec.Sites)
                {
                    ulong addr=SiteAddress(s);var original=Convert.FromHexString(s.Original);
                    for(int i=0;i<original.Length;i++)if(addr+(ulong)i>=start && addr+(ulong)i<start+(ulong)bytes.Length)bytes[(int)(addr+(ulong)i-start)]=original[i];
                }
                foreach(byte b in bytes)hash=unchecked((hash^b)*0x100000001b3);
            }
            if(hash!=set.Hash)throw new Exception($"Версия кода не поддерживается ({hash:X16}). Запись запрещена.");
        }
    }
    public void Execute(string command)
    {
        switch(command)
        {
            case "--status":Status();break;
            case "--combat-on":Set(hooks[0],true,1);break;
            case "--damage-on":Set(hooks[0],true,6);break;
            case "--combat-off":Set(hooks[0],false,1);break;
            case "--jump-on":Set(hooks[1],true,2);break;
            case "--jump-off":Set(hooks[1],false,2);break;
            case "--money":Money();break;
            default:throw new ArgumentException("Неизвестная команда.");
        }
    }
    void Set(Hook h,bool enabled,float factor)
    {
        if(h.Allocation==0 && !enabled){Console.WriteLine(h.Name+": отключено.");return;}
        if(h.Allocation==0)Install(h);
        ulong state=h.Allocation+h.Spec.Offsets["control"];
        // Disable before changing the multiplier; no half-written active configuration.
        WriteVerified(state,BitConverter.GetBytes(0));
        WriteVerified(state+4,BitConverter.GetBytes(factor));
        if(enabled)WriteVerified(state,BitConverter.GetBytes(1));
        Status();
    }
    void Install(Hook h)
    {
        ulong allocation=d.AllocateMemory(pid,0x4000);
        if(allocation==0 || allocation%0x4000!=0)throw new Exception("Не удалось выделить память.");
        byte[] code=(byte[])h.Image.Clone();BitConverter.GetBytes(0).CopyTo(code,(int)h.Spec.Offsets["control"]);
        WriteVerified(allocation,code);d.ChangeProtection(pid,allocation,0x4000,PS4DBG.VM_PROTECTIONS.VM_PROT_ALL);
        bool writing=false;
        try
        {
            d.AttachDebugger(pid,(tid,status,name,regs,fpregs,dbregs)=>{});attached=true;d.ProcessStop();
            foreach(uint tid in d.GetThreadList())
            {
                var regs=d.GetRegisters(tid);
                if(regs.r_rip==0 || regs.r_rsp==0)throw new Exception("Недостоверные регистры потока.");
                if(h.Spec.Sites.Any(s=>regs.r_rip>=SiteAddress(s) && regs.r_rip<SiteAddress(s)+(ulong)s.Length))throw new Exception("Поток находится в месте установки. Повторите операцию.");
            }
            foreach(var s in h.Spec.Sites)if(!d.ReadMemory(pid,SiteAddress(s),s.Length).SequenceEqual(Convert.FromHexString(s.Original)))throw new Exception("Код изменился перед установкой.");
            writing=true;
            foreach(var s in h.Spec.Sites)WriteVerified(SiteAddress(s),Patch(h,s,allocation));
            h.Allocation=allocation;writing=false;
        }
        catch
        {
            if(writing)foreach(var s in h.Spec.Sites)WriteVerified(SiteAddress(s),Convert.FromHexString(s.Original));
            throw;
        }
        finally {if(attached){d.DetachDebugger();attached=false;}}
    }
    void WriteVerified(ulong address,byte[] value)
    {
        d.WriteMemory(pid,address,value);
        if(!d.ReadMemory(pid,address,value.Length).SequenceEqual(value))throw new IOException($"Не подтверждена запись 0x{address:X}. Не повторяйте без проверки состояния.");
    }
    void Status()
    {
        foreach(var h in hooks)
        {
            if(h.Allocation==0){Console.WriteLine(h.Name+": не установлен");continue;}
            var state=d.ReadMemory(pid,h.Allocation+h.Spec.Offsets["control"],h.Name=="combat"?80:40);
            Console.WriteLine($"{h.Name}: {(BitConverter.ToInt32(state)!=0?"ВКЛ":"ВЫКЛ")}; множитель {BitConverter.ToSingle(state,4)}; срабатывания {BitConverter.ToUInt64(state,8)}");
        }
    }
    void Money()
    {
        // Resolves wallet and definitions anew on the game's main thread. No quest or unlock APIs.
        const int allocationSize=0x4000,stateOffset=0x2000;
        ulong update=imageBase+0x5d35c0;
        byte[] original=d.ReadMemory(pid,update,12);
        if(!original.SequenceEqual(Convert.FromHexString("C36666666666662E0F1F8400")))throw new Exception("Update занят другим payload.");
        ulong allocation=d.AllocateMemory(pid,allocationSize);
        if(allocation==0 || allocation%0x4000!=0)throw new Exception("Не удалось выделить память.");
        ulong state=allocation+stateOffset;
        byte[] image=MoneyImage(allocation,imageBase);
        WriteVerified(allocation,image);d.ChangeProtection(pid,allocation,allocationSize,PS4DBG.VM_PROTECTIONS.VM_PROT_ALL);
        byte[] patch=[0x48,0xb8,..BitConverter.GetBytes(allocation),0xff,0xe0];bool armed=false;
        try
        {
            WriteVerified(update+1,patch[1..]);armed=true;WriteVerified(update,[patch[0]]);
            var timer=System.Diagnostics.Stopwatch.StartNew();int result=0;
            while(timer.Elapsed.TotalSeconds<15){result=BitConverter.ToInt32(d.ReadMemory(pid,state,4));if(result is 2 or 3)break;Thread.Sleep(100);}
            if(result!=2)throw new Exception("Выдача валют не подтверждена. Не повторяйте без проверки; загрузите персонажа.");
            for(int i=0;i<2;i++){long amount=BitConverter.ToInt64(d.ReadMemory(pid,state+0x60+(ulong)i*8,8));if(amount<100000 || amount>1000000)throw new Exception("Итоговая сумма не подтверждена.");}
            Console.WriteLine("Две валюты доведены до 100 000. Счётчик обновится после подбора/траты. Остальные предметы не выдавались.");
        }
        finally
        {
            if(armed)WriteVerified(update,[original[0]]);
            WriteVerified(update+1,original[1..]);
        }
    }
    static byte[] MoneyImage(ulong allocation,ulong imageBase)
    {
        string[] names=["loot_currency","loot_orb_red"];
        const int allocationSize=0x4000,stateOffset=0x2000;
        ulong state=allocation+stateOffset;
        var c=new Code();
        c.B(0x55,0x48,0x89,0xe5,0x53,0x41,0x54,0x41,0x55,0x41,0x56,0x41,0x57,0x48,0x83,0xec,8);
        c.B(0x49,0x89,0xfc,0x49,0xbf);c.Q(state);
        c.B(0x31,0xc0,0xb9,1,0,0,0,0xf0,0x41,0x0f,0xb1,0x0f);c.J(0x85,"exit");
        c.B(0x4c,0x89,0xe7,0x31,0xf6);c.Call(imageBase+0x5d12d0);c.B(0x48,0x85,0xc0);c.J(0x84,"fail");
        c.B(0x48,0x89,0xc7,0x31,0xf6);c.Call(imageBase+0x8c0810);c.B(0x48,0x85,0xc0);c.J(0x84,"fail");
        c.B(0x49,0x89,0xc6,0x49,0x89,0x47,8);
        for(int i=0;i<2;i++)
        {
            c.B(0x48,0xbf);c.Q(state+0x100+(ulong)i*64);c.Call(imageBase+0x32fac0);
            c.B(0x48,0x85,0xc0);c.J(0x84,"fail");c.B(0x48,0x89,0xc7,0x31,0xf6);c.Call(imageBase+0x8c91b0);
            c.B(0x48,0x85,0xc0);c.J(0x84,"fail");c.B(0x48,0x83,0x78,0x10,0);c.J(0x84,"fail");c.B(0x49,0x89,0x47,(byte)(0x20+i*8));
            c.B(0x4c,0x89,0xf7,0x48,0x89,0xc6,0x31,0xd2);c.Call(imageBase+0x8ce2b0);
            c.B(0x48,0x85,0xc0);c.J(0x88,"fail");c.B(0x48,0x3d);c.D(1000000);c.J(0x8f,"fail");
            c.B(0x49,0x89,0x47,(byte)(0x40+i*8));
        }
        for(int i=0;i<2;i++)
        {
            c.B(0x49,0x8b,0x47,(byte)(0x40+i*8),0x48,0x3d);c.D(100000);c.J(0x8d,"next"+i);
            c.B(0xba);c.D(100000);c.B(0x48,0x29,0xc2,0x4c,0x89,0xf7,0x49,0x8b,0x77,(byte)(0x20+i*8),0xb9,1,1,0,0,0x45,0x31,0xc0);c.Call(imageBase+0x8ce430);c.Label("next"+i);
            c.B(0x4c,0x89,0xf7,0x49,0x8b,0x77,(byte)(0x20+i*8),0x31,0xd2);c.Call(imageBase+0x8ce2b0);
            c.B(0x49,0x89,0x47,(byte)(0x60+i*8),0x48,0x3d);c.D(100000);c.J(0x8c,"fail");
        }
        c.B(0x41,0xc7,0x07,2,0,0,0);c.Jmp("exit");
        c.Label("fail");c.B(0x41,0xc7,0x07,3,0,0,0);
        c.Label("exit");c.B(0x48,0x83,0xc4,8,0x41,0x5f,0x41,0x5e,0x41,0x5d,0x41,0x5c,0x5b,0x5d,0xc3);
        byte[] image=new byte[allocationSize];var machine=c.Build();
        if(machine.Length>=stateOffset)throw new Exception("Переполнение payload.");
        machine.CopyTo(image,0);for(int i=0;i<2;i++)Encoding.ASCII.GetBytes(names[i]).CopyTo(image,stateOffset+0x100+i*64);
        return image;
    }
    public static void SelfTest()
    {
        foreach(string name in new[]{"combat","jump"})
        {
            var spec=JsonSerializer.Deserialize<Spec>(Resource(name+"-hook.json"))!;
            var original=Resource(name+"-hook.bin");var same=(byte[])original.Clone();Relocate(same,spec,name,OldBase);
            if(!same.SequenceEqual(original))throw new Exception("Identity relocation failed.");
            var shifted=(byte[])original.Clone();Relocate(shifted,spec,name,OldBase+0x10000000);
            if(shifted.SequenceEqual(original))throw new Exception("Relocation did not change references.");
            foreach(var pair in spec.Offsets)if(pair.Value>=(ulong)original.Length)throw new Exception("Invalid offset.");
        }
        byte[] money=MoneyImage(0x300000000,OldBase);
        if(money.Length!=0x4000 || money[0]!=0x55 || !Encoding.ASCII.GetString(money,0x2100,13).StartsWith("loot_currency"))throw new Exception("Money payload failed.");
        Console.WriteLine("Embedded payloads, identity and shifted relocation, wallet payload: OK");
    }
    public void Dispose(){if(attached)d.DetachDebugger();d.Disconnect();}
    sealed class Hook(string name,Spec spec,byte[] image){public string Name=name;public Spec Spec=spec;public byte[] Image=image;public ulong Allocation;}
    record Spec(int Size,Dictionary<string,ulong> Offsets,Site[] Sites);
    record Site(string Name,string Address,string Original,int Length);
}

sealed class Code
{
    readonly List<byte> bytes=[];
    readonly Dictionary<string,int> labels=[];
    readonly List<(int At,string Label)> fixups=[];
    public void B(params byte[] value)=>bytes.AddRange(value);
    public void D(int value)=>bytes.AddRange(BitConverter.GetBytes(value));
    public void Q(ulong value)=>bytes.AddRange(BitConverter.GetBytes(value));
    public void Call(ulong value){B(0x48,0xb8);Q(value);B(0xff,0xd0);}
    public void Label(string name)=>labels.Add(name,bytes.Count);
    public void J(byte condition,string name){B(0x0f,condition);fixups.Add((bytes.Count,name));D(0);}
    public void Jmp(string name){B(0xe9);fixups.Add((bytes.Count,name));D(0);}
    public byte[] Build(){var result=bytes.ToArray();foreach(var f in fixups)BitConverter.GetBytes(labels[f.Label]-f.At-4).CopyTo(result,f.At);return result;}
}
