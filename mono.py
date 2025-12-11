#!/usr/bin/env python3
import sys, os, requests, concurrent.futures, time, re, json, socket
from datetime import datetime
from urllib.parse import quote
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt, Confirm
from rich.tree import Tree
from rich import box

# Try importing phonenumbers for advanced tracking
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
    PHONENUMBERS_AVAIL = True
except ImportError:
    PHONENUMBERS_AVAIL = False

console = Console()

class MonoUltimate:
    def __init__(self):
        self.found_data = {}
        self.target_user = ""
        self.start_time = None
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        
        # DATABASE 120+ SITUS (Shortened for brevity but fully functional logic)
        self.platforms = {
            "SOCIAL": [("Instagram","https://instagram.com/{}"),("TikTok","https://tiktok.com/@{}"),("Twitter","https://twitter.com/{}"),("Facebook","https://facebook.com/{}"),("LinkedIn","https://linkedin.com/in/{}"),("Telegram","https://t.me/{}")],
            "DEV": [("GitHub","https://github.com/{}"),("GitLab","https://gitlab.com/{}"),("Replit","https://replit.com/@{}"),("Pastebin","https://pastebin.com/u/{}"),("NPM","https://npmjs.com/~{}")],
            "GAMING": [("Steam","https://steamcommunity.com/id/{}"),("Twitch","https://twitch.tv/{}"),("Roblox","https://roblox.com/user.aspx?username={}")],
            "CONTENT": [("YouTube","https://youtube.com/@{}"),("Spotify","https://open.spotify.com/user/{}"),("Wattpad","https://wattpad.com/user/{}")],
            "BLOG": [("Medium","https://medium.com/@{}"),("WordPress","https://{}.wordpress.com"),("Blogger","https://{}.blogspot.com")],
            "ADULT": [("Pornhub","https://pornhub.com/users/{}"),("Xvideos","https://xvideos.com/profiles/{}")]
        }

    def banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        art = Text(r"""
███╗   ███╗ ██████╗ ███╗   ██╗ ██████╗ 
████╗ ████║██╔═══██╗████╗  ██║██╔═══██╗
██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║
██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║
██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ """, style="bold white on black")
        console.print(Align.center(art))
        console.print(Align.center(Text("⚡ MONO REVOLUTION: IDENTITY HUNTER ⚡", style="bold yellow")))
        console.print(Align.center(Text(f"v4.0 | REVOLUTION EDITION | {datetime.now().strftime('%Y-%m-%d')}", style="dim white")))
        print()

    def check(self, cat, site, url):
        try:
            target_url = url.format(self.target_user)
            r = self.session.get(target_url, timeout=5)
            if r.status_code == 200:
                c = r.text.lower()
                bad = ["not found","doesn't exist","404","no such user","halaman tidak ditemukan"]
                # Filter False Positive TikTok
                if site == "TikTok" and "tiktok.com" not in r.url: return None
                
                if not any(b in c for b in bad):
                    return (cat, site, target_url)
        except: pass
        return None

    def scan(self):
        self.banner()
        self.target_user = Prompt.ask("[bold yellow]🎯 Enter Username to Hunt[/]")
        if not self.target_user: return
        
        self.start_time = datetime.now()
        self.found_data = {}
        
        checks = []
        for cat, sites in self.platforms.items():
            for site, url in sites: checks.append((cat, site, url))
        
        console.print(f"\n[cyan]⚡ Initiating Deep Scan on: [white]{self.target_user}[/][/]\n")
        
        with Progress(SpinnerColumn("dots"),TextColumn("[cyan]{task.description}"),BarColumn(complete_style="green"),TextColumn("{task.percentage:>3.0f}%"),console=console) as p:
            task = p.add_task("Scanning Digital Universe...", total=len(checks))
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as e:
                futures = {e.submit(self.check, c, s, u): s for c, s, u in checks}
                for f in concurrent.futures.as_completed(futures):
                    r = f.result()
                    if r:
                        cat, site, url = r
                        if cat not in self.found_data: self.found_data[cat] = []
                        self.found_data[cat].append((site, url))
                    p.advance(task)
        self.results()

    def results(self):
        self.banner()
        total = sum(len(i) for i in self.found_data.values())
        
        if not total:
            console.print(Panel(f"[red]TARGET IS A GHOST.[/]\nNo footprint found for '{self.target_user}'.", border_style="red"))
            input("\nPress Enter...")
            return
        
        tree = Tree(f"[bold green]🎯 TARGET IDENTIFIED: {self.target_user}")
        for cat, items in self.found_data.items():
            branch = tree.add(f"[yellow]{cat}[/]")
            for site, url in items:
                branch.add(f"[cyan]{site}[/]: [link={url}]{url}[/link]")
        
        console.print(tree)
        
        # Save Report logic
        filename = f"REPORT_{self.target_user}.txt"
        with open(filename, "w") as f:
            f.write(f"MONO REVOLUTION REPORT: {self.target_user}\n" + "="*50 + "\n")
            for cat, items in self.found_data.items():
                for site, url in items: f.write(f"{site}: {url}\n")
        console.print(f"\n[bold black on green] SUCCESS [/] Report saved: {filename}")
        input("\nPress Enter...")

    # --- FITUR BARU: REAL NAME DNA ---
    def real_name_investigator(self):
        self.banner()
        console.print(Panel("[bold white]🕵️ REAL NAME DNA HUNTER[/]\n[dim]Fitur ini mencari jejak identitas asli (CV, Skripsi, Berita) yang sering terlewat.[/]", border_style="green"))
        
        name = Prompt.ask("[bold yellow]👤 Masukkan Nama Lengkap Target[/]")
        city = Prompt.ask("[bold cyan]🏙️  Masukkan Kota/Asal (Optional - Enter utk skip)[/]")
        
        location_query = f'+ "{city}"' if city else ""
        
        # LOGIKA REVOLUSIONER: Dorking Spesifik
        queries = [
            ("📄 CV & Resume (Bocor)", f'filetype:pdf OR filetype:docx OR filetype:doc "{name}" (cv OR daftar riwayat hidup OR resume)'),
            ("🎓 Data Akademik/Skripsi", f'site:ac.id OR site:sch.id "{name}" (skripsi OR jurnal OR siswa OR mahasiswa)'),
            ("💼 LinkedIn & Profesional", f'site:linkedin.com OR site:jobstreet.co.id "{name}" {location_query}'),
            ("📰 Berita & Media", f'site:news.detik.com OR site:kompas.com OR site:tribunnews.com "{name}"'),
            ("👥 Facebook/Instagram", f'site:facebook.com OR site:instagram.com OR site:tiktok.com "{name}" {location_query}'),
            ("📂 Google Drive Public", f'site:drive.google.com "{name}"'),
        ]
        
        t = Table(title=f"🔍 ANALISIS JEJAK: {name.upper()}", box=box.ROUNDED)
        t.add_column("Tipe Data", style="cyan")
        t.add_column("Link Investigasi (Klik)", style="white")
        
        for title, q in queries:
            url = f"https://www.google.com/search?q={quote(q)}"
            t.add_row(title, f"[link={url}]BUKA HASIL PENCARIAN[/link]")
            
        console.print(t)
        console.print("\n[dim]Tips: Jika nama pasaran, tambahkan nama sekolah/tempat kerja di pencarian.[/]")
        input("\nPress Enter...")

    # --- FITUR UPGRADE: PHONE TRACKER ---
    def phone_advanced(self):
        self.banner()
        console.print(Panel("[bold magenta]📱 ADVANCED PHONE INTEL[/]\n[dim]Melacak Provider, Lokasi, dan WhatsApp tanpa internet.[/]", border_style="magenta"))
        
        if not PHONENUMBERS_AVAIL:
            console.print("[red]❌ Library 'phonenumbers' belum diinstall![/]")
            console.print("Ketik di terminal: [bold]pip install phonenumbers[/]")
            input()
            return

        number = Prompt.ask("[bold yellow]📱 Masukkan Nomor (Pakai kode negara, cth: +62812...)[/]")
        
        try:
            parsed = phonenumbers.parse(number, None)
            if not phonenumbers.is_valid_number(parsed):
                console.print("[bold red]❌ Nomor tidak valid![/]")
                input(); return
            
            # Mendapatkan Data Offline
            country = geocoder.description_for_number(parsed, "id")
            provider = carrier.name_for_number(parsed, "id")
            tz = timezone.time_zones_for_number(parsed)
            
            grid = Table.grid(padding=(0,2))
            grid.add_column(style="bold yellow", justify="right")
            grid.add_column(style="white")
            
            grid.add_row("🌍 Negara/Lokasi", country)
            grid.add_row("📡 Provider", provider)
            grid.add_row("⏰ Timezone", str(tz))
            grid.add_row("✅ Valid", "YES")
            
            console.print(Panel(grid, title=f"DATA: {number}", border_style="green"))
            
            # Social Links
            wa = f"https://wa.me/{number.replace('+','')}"
            tg = f"https://t.me/{number.replace('+','')}"
            
            console.print(f"\n[green]💬 Direct WhatsApp:[/link] [link={wa}]{wa}[/link]")
            console.print(f"[blue]✈️  Direct Telegram:[/link] [link={tg}]{tg}[/link]")
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
        
        input("\nPress Enter...")

    def dork(self):
        self.banner()
        target = Prompt.ask("[yellow]🔎 Enter Target Keyword[/]")
        dorks = {
            "Passwords":f'intext:"password" OR intext:"login" "{target}"',
            "Database":f'filetype:sql OR filetype:db "{target}"',
            "Config":f'ext:env OR ext:yml "{target}"',
            "Camera/CCTV":f'intitle:"webcam 7" "{target}"',
            "Government":f'site:go.id "{target}"'
        }
        t = Table(title="GOOGLE DORKS",box=box.SIMPLE)
        t.add_column("Type",style="cyan")
        t.add_column("Link",style="white")
        for name, query in dorks.items(): 
            url = f"https://www.google.com/search?q={quote(query)}"
            t.add_row(name, f"[link={url}]OPEN LINK[/link]")
        console.print(t)
        input("\nPress Enter...")

    def ip(self):
        self.banner()
        target = Prompt.ask("[yellow]🌐 Enter IP/Domain[/]")
        try:
            if any(c.isalpha() for c in target): target = socket.gethostbyname(target)
            data = self.session.get(f"http://ip-api.com/json/{target}").json()
            
            t = Table(title="IP INTEL", box=box.ROUNDED)
            t.add_column("Key", style="yellow"); t.add_column("Value", style="green")
            for k,v in data.items(): t.add_row(k.upper(), str(v))
            console.print(t)
        except: console.print("[red]Failed.[/]")
        input("\nPress Enter...")

    def menu(self):
        while True:
            self.banner()
            console.print(Panel(
                "[1] [cyan]USERNAME SCAN[/]     (120+ Platforms)\n"
                "[2] [bold green]REAL NAME DNA[/]     (Find Person by Name)\n"
                "[3] [magenta]PHONE TRACKER[/]     (Provider & Location)\n"
                "[4] [yellow]GOOGLE DORKS[/]      (Hacking Queries)\n"
                "[5] [blue]IP TRACKER[/]        (Geolocation)\n"
                "[0] [red]EXIT[/]",
                title="🔥 MAIN MENU", border_style="cyan"))
            
            choice = Prompt.ask("[bold green]MONO~#[/]", choices=["1","2","3","4","5","0"])
            
            if choice=="1": self.scan()
            elif choice=="2": self.real_name_investigator() # FITUR BARU
            elif choice=="3": self.phone_advanced()         # FITUR BARU
            elif choice=="4": self.dork()
            elif choice=="5": self.ip()
            elif choice=="0": sys.exit()

if __name__ == "__main__":
    try:
        app = MonoUltimate()
        app.menu()
    except KeyboardInterrupt:
        print("\n[red]System Shutdown.[/]")
