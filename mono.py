#!/usr/bin/env python3
import sys, os, requests, concurrent.futures, time, re, json, socket, hashlib
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

console = Console()

class MonoUltimate:
    def __init__(self):
        self.found_data = {}
        self.target_user = ""
        self.start_time = None
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        
        self.platforms = {
            "SOCIAL": [("Instagram","https://instagram.com/{}"),("TikTok","https://tiktok.com/@{}"),("Twitter","https://twitter.com/{}"),("Facebook","https://facebook.com/{}"),("LinkedIn","https://linkedin.com/in/{}"),("Pinterest","https://pinterest.com/{}/"),("Reddit","https://reddit.com/user/{}"),("Telegram","https://t.me/{}"),("Snapchat","https://snapchat.com/add/{}"),("VK","https://vk.com/{}"),("Mastodon","https://mastodon.social/@{}"),("Threads","https://threads.net/@{}")],
            "DEV": [("GitHub","https://github.com/{}"),("GitLab","https://gitlab.com/{}"),("Bitbucket","https://bitbucket.org/{}"),("Replit","https://replit.com/@{}"),("CodePen","https://codepen.io/{}"),("StackOverflow","https://stackoverflow.com/users/{}"),("HackerRank","https://hackerrank.com/{}"),("LeetCode","https://leetcode.com/{}"),("Pastebin","https://pastebin.com/u/{}"),("NPM","https://npmjs.com/~{}"),("PyPI","https://pypi.org/user/{}"),("DockerHub","https://hub.docker.com/u/{}"),("HackerOne","https://hackerone.com/{}")],
            "DESIGN": [("DeviantArt","https://deviantart.com/{}"),("Behance","https://behance.net/{}"),("Dribbble","https://dribbble.com/{}"),("ArtStation","https://artstation.com/{}"),("Flickr","https://flickr.com/people/{}"),("500px","https://500px.com/p/{}"),("Unsplash","https://unsplash.com/@{}"),("Imgur","https://imgur.com/user/{}")],
            "GAMING": [("Steam","https://steamcommunity.com/id/{}"),("Twitch","https://twitch.tv/{}"),("Roblox","https://roblox.com/user.aspx?username={}"),("Minecraft","https://namemc.com/profile/{}"),("Chess.com","https://chess.com/member/{}"),("Lichess","https://lichess.org/@{}"),("Itch.io","https://{}.itch.io"),("Newgrounds","https://{}.newgrounds.com")],
            "CONTENT": [("YouTube","https://youtube.com/@{}"),("Vimeo","https://vimeo.com/{}"),("SoundCloud","https://soundcloud.com/{}"),("Spotify","https://open.spotify.com/user/{}"),("Bandcamp","https://{}.bandcamp.com"),("Patreon","https://patreon.com/{}"),("Ko-fi","https://ko-fi.com/{}"),("Substack","https://{}.substack.com")],
            "BLOG": [("Medium","https://medium.com/@{}"),("WordPress","https://{}.wordpress.com"),("Blogger","https://{}.blogspot.com"),("Tumblr","https://{}.tumblr.com"),("Wattpad","https://wattpad.com/user/{}"),("Goodreads","https://goodreads.com/{}")],
            "BIZ": [("AngelList","https://angel.co/u/{}"),("Crunchbase","https://crunchbase.com/person/{}"),("About.me","https://about.me/{}"),("Keybase","https://keybase.io/{}"),("ProductHunt","https://producthunt.com/@{}")],
            "FORUM": [("Quora","https://quora.com/profile/{}"),("Disqus","https://disqus.com/by/{}"),("MyAnimeList","https://myanimelist.net/profile/{}"),("Letterboxd","https://letterboxd.com/{}"),("Last.fm","https://last.fm/user/{}"),("Genius","https://genius.com/{}")],
            "MARKET": [("Etsy","https://etsy.com/shop/{}"),("eBay","https://ebay.com/usr/{}"),("Fiverr","https://fiverr.com/{}"),("Upwork","https://upwork.com/freelancers/~{}")],
            "CRYPTO": [("OpenSea","https://opensea.io/{}"),("Rarible","https://rarible.com/{}")]
        }

    def banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        art = Text(r"""
███╗   ███╗ ██████╗ ███╗   ██╗ ██████╗     ██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗
████╗ ████║██╔═══██╗████╗  ██║██╔═══██╗    ██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║    ██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗  
██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║    ██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝  
██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝    ╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝      ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝""", style="bold cyan")
        console.print(Align.center(art))
        console.print(Align.center(Text("⚡ THE ULTIMATE OSINT FRAMEWORK ⚡", style="bold yellow")))
        console.print(Align.center(Text(f"v3.0 | {datetime.now().strftime('%Y-%m-%d %H:%M')} | 120+ Platforms", style="dim white")))
        print()

    def check(self, cat, site, url):
        try:
            r = self.session.get(url.format(self.target_user), timeout=7, allow_redirects=True)
            if r.status_code == 200:
                c = r.text.lower()
                bad = ["not found","doesn't exist","404","no such user","suspended"]
                good = ["profile","posts","followers","about","bio"]
                if not any(b in c for b in bad) and (any(g in c for g in good) or len(c)>3000):
                    return (cat, site, url.format(self.target_user), r.status_code, len(c))
        except: pass
        return None

    def scan(self):
        self.banner()
        self.target_user = Prompt.ask("[bold yellow]🎯 Enter Username[/]")
        if not self.target_user: return
        
        self.start_time = datetime.now()
        self.found_data = {}
        
        checks = []
        for cat, sites in self.platforms.items():
            for site, url in sites: checks.append((cat, site, url))
        
        console.print(f"\n[cyan]⚡ Scanning {len(checks)} platforms for: [white]{self.target_user}[/][/]\n")
        
        with Progress(SpinnerColumn("dots12"),TextColumn("[cyan]{task.description}"),BarColumn(complete_style="green"),TextColumn("{task.percentage:>3.0f}%"),TimeElapsedColumn(),console=console) as p:
            task = p.add_task("🔍 Scanning...", total=len(checks))
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as e:
                futures = {e.submit(self.check, c, s, u): s for c, s, u in checks}
                for f in concurrent.futures.as_completed(futures):
                    r = f.result()
                    if r:
                        cat, site, url, status, size = r
                        if cat not in self.found_data: self.found_data[cat] = []
                        self.found_data[cat].append((site, url, status, size))
                    p.advance(task)
        
        self.results()

    def results(self):
        self.banner()
        dur = (datetime.now() - self.start_time).total_seconds()
        total = sum(len(i) for i in self.found_data.values())
        
        if not total:
            console.print(Panel(f"[red]👻 No results for '{self.target_user}'[/]\n[dim]Scanned in {dur:.2f}s[/]",border_style="red"))
            input("\nPress Enter...")
            return
        
        risk = min(100, (total/120)*100)
        emoji = "🔴" if risk>60 else "🟡" if risk>30 else "🟢"
        
        s = Table.grid(padding=(0,2))
        s.add_column(style="cyan bold", justify="right")
        s.add_column(style="white")
        s.add_row("🎯 Target", self.target_user)
        s.add_row("✅ Found", f"[green]{total}[/]")
        s.add_row("📁 Categories", f"[yellow]{len(self.found_data)}[/]")
        s.add_row("⏱️  Time", f"{dur:.2f}s")
        s.add_row(f"{emoji} Exposure", f"{risk:.0f}%")
        console.print(Panel(s, title="📊 RESULTS", border_style="cyan"))
        print()
        
        t = Table(title="📈 BREAKDOWN",box=box.DOUBLE_EDGE)
        t.add_column("Category",style="yellow",width=15)
        t.add_column("Found",style="green",justify="center",width=8)
        t.add_column("%",style="cyan",justify="center",width=8)
        for cat, items in sorted(self.found_data.items(), key=lambda x: len(x[1]), reverse=True):
            t.add_row(cat, str(len(items)), f"{(len(items)/total)*100:.0f}%")
        console.print(t)
        print()
        
        tree = Tree(f"[green]🔍 DETAILS: {self.target_user}")
        for cat, items in sorted(self.found_data.items()):
            b = tree.add(f"[yellow]{cat}[/] [dim]({len(items)})[/]")
            for site, url, _, size in sorted(items):
                b.add(f"✅ [cyan]{site}[/] • {url} [dim]({size/1024:.0f}KB)[/]")
        console.print(tree)
        print()
        
        if risk>60: console.print("[red]🔴 HIGH RISK: Review privacy settings![/]")
        elif risk>30: console.print("[yellow]🟡 MODERATE: Enable 2FA everywhere[/]")
        else: console.print("[green]🟢 LOW RISK: Good privacy posture[/]")
        
        if Confirm.ask("\n[cyan]💾 Save reports?[/]", default=True):
            self.export(total, dur, risk)
        
        input("\nPress Enter...")

    def export(self, total, dur, risk):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"MONO_{self.target_user}_{ts}"
        
        with open(f"{base}.txt", "w") as f:
            f.write("="*80+"\n")
            f.write("MONO ULTIMATE - OSINT REPORT\n")
            f.write("="*80+"\n\n")
            f.write(f"Target: {self.target_user}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Found: {total}\nTime: {dur:.2f}s\nRisk: {risk:.0f}%\n")
            f.write("="*80+"\n\n")
            for cat, items in self.found_data.items():
                f.write(f"\n[{cat}] - {len(items)}\n"+"-"*80+"\n")
                for site, url, _, _ in items: f.write(f"  ✓ {site:20} {url}\n")
        
        with open(f"{base}.json", "w") as f:
            json.dump({"target":self.target_user,"found":total,"risk":risk,"results":{c:[{"site":s,"url":u} for s,u,_,_ in i] for c,i in self.found_data.items()}}, f, indent=2)
        
        with open(f"{base}.html", "w") as f:
            f.write(f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>MONO Report</title><style>body{{font-family:monospace;background:#0a0a0a;color:#0f0;padding:20px}}.h{{background:#1a1a1a;padding:20px;border:2px solid #0f0}}.c{{background:#151515;padding:15px;margin:10px 0;border-left:4px solid #0ff}}a{{color:#0ff}}</style></head><body><div class="h"><h1>MONO REPORT</h1><p>Target: {self.target_user}<br>Found: {total}<br>Risk: {risk:.0f}%</p></div>')
            for cat, items in self.found_data.items():
                f.write(f'<div class="c"><h2>{cat} ({len(items)})</h2>')
                for site, url, _, _ in items: f.write(f'<p>✓ <b>{site}</b>: <a href="{url}">{url}</a></p>')
                f.write('</div>')
            f.write('</body></html>')
        
        with open(f"{base}.csv", "w") as f:
            f.write("Category,Site,URL\n")
            for cat, items in self.found_data.items():
                for site, url, _, _ in items: f.write(f'"{cat}","{site}","{url}"\n')
        
        console.print(f"[green]✅ Saved:[/] {base}.txt, .json, .html, .csv")

    def email(self):
        self.banner()
        email = Prompt.ask("[yellow]📧 Enter Email[/]")
        if "@" not in email: return
        
        user, domain = email.split("@")
        t = Table(title="📧 EMAIL INTEL",box=box.ROUNDED)
        t.add_column("Property",style="yellow")
        t.add_column("Value",style="white")
        t.add_row("Username", user)
        t.add_row("Domain", domain)
        t.add_row("Type", "Personal" if domain in ["gmail.com","yahoo.com","outlook.com"] else "Corporate")
        t.add_row("Breach Check", "haveibeenpwned.com")
        t.add_row("Google", f"google.com/search?q={quote(email)}")
        console.print(t)
        
        if Confirm.ask(f"\n[cyan]Scan username '{user}'?[/]"):
            self.target_user = user
            self.scan()
            return
        input("\nPress Enter...")

    def phone(self):
        self.banner()
        phone = Prompt.ask("[yellow]📱 Enter Phone[/]")
        clean = re.sub(r'[^\d+]', '', phone)
        
        t = Table(title="📱 PHONE INTEL",box=box.ROUNDED)
        t.add_column("Service",style="cyan",width=20)
        t.add_column("Link",style="white",width=60)
        searches = {"TrueCaller":f"truecaller.com/search/id/{clean}","WhatsApp":f"wa.me/{clean}","Telegram":f"t.me/{clean}","Google":f"google.com/search?q={quote(phone)}"}
        for s, u in searches.items(): t.add_row(s, u)
        console.print(t)
        input("\nPress Enter...")

    def dork(self):
        self.banner()
        target = Prompt.ask("[yellow]🔎 Enter Target[/]")
        
        dorks = {
            "Secrets":f'site:pastebin.com OR site:docs.google.com "{target}"',
            "Passwords":f'intext:"password" OR intext:"login" "{target}"',
            "Database":f'filetype:sql OR filetype:db "{target}"',
            "Config":f'ext:env OR ext:yml "{target}"',
            "Logs":f'filetype:log "{target}"',
            "Backup":f'ext:bak OR ext:backup "{target}"',
            "Email":f'intext:"@{target}"',
            "Social":f'site:facebook.com OR site:twitter.com "{target}"',
            "Docs":f'filetype:pdf OR filetype:docx "{target}"',
            "Subdomain":f'site:*.{target}',
            "Admin":f'intitle:"admin" site:{target}',
            "GitHub":f'site:github.com "{target}" password OR apikey'
        }
        
        t = Table(title="🔍 GOOGLE DORKS",box=box.HEAVY_EDGE,show_lines=True)
        t.add_column("Type",style="yellow",width=15)
        t.add_column("Query",style="cyan",width=70)
        for name, query in dorks.items(): t.add_row(name, query)
        console.print(t)
        
        if Confirm.ask("\n[cyan]Save to file?[/]"):
            fn = f"DORKS_{target.replace('.','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(fn, "w") as f:
                f.write(f"GOOGLE DORKS: {target}\n"+"="*70+"\n\n")
                for name, query in dorks.items():
                    f.write(f"{name}:\n{query}\nhttps://google.com/search?q={quote(query)}\n\n")
            console.print(f"[green]✅ Saved: {fn}[/]")
        input("\nPress Enter...")

    def ip(self):
        self.banner()
        target = Prompt.ask("[yellow]🌐 Enter IP/Domain[/]")
        
        try:
            with console.status("🔍 Tracking...", spinner="dots"):
                if any(c.isalpha() for c in target):
                    ip = socket.gethostbyname(target)
                    console.print(f"[green]✓[/] {target} → {ip}\n")
                else: ip = target
                
                data = self.session.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
            
            t = Table(title="🌍 IP INTEL",box=box.ROUNDED)
            t.add_column("Property",style="yellow",width=20)
            t.add_column("Value",style="green",width=50)
            t.add_row("IP", ip)
            t.add_row("ISP", data.get('isp','N/A'))
            t.add_row("Org", data.get('org','N/A'))
            t.add_row("Country", f"{data.get('country','N/A')} ({data.get('countryCode','N/A')})")
            t.add_row("Region", data.get('regionName','N/A'))
            t.add_row("City", data.get('city','N/A'))
            t.add_row("Timezone", data.get('timezone','N/A'))
            t.add_row("Coords", f"{data.get('lat','N/A')}, {data.get('lon','N/A')}")
            t.add_row("Map", f"google.com/maps?q={data.get('lat')},{data.get('lon')}")
            console.print(t)
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/]")
        input("\nPress Enter...")

    def menu(self):
        while True:
            self.banner()
            console.print(Panel(
                "[1] [cyan]USERNAME SCAN[/]     - 120+ platforms\n"
                "[2] [yellow]EMAIL INTEL[/]       - Email analysis\n"
                "[3] [magenta]PHONE LOOKUP[/]      - Phone OSINT\n"
                "[4] [green]GOOGLE DORKS[/]      - Advanced search\n"
                "[5] [blue]IP TRACKER[/]        - Geolocation\n"
                "[0] [red]EXIT[/]",
                title="🎯 MONO ULTIMATE",border_style="cyan"))
            
            choice = Prompt.ask("[green]mono>#[/]", choices=["1","2","3","4","5","0"])
            
            if choice=="1": self.scan()
            elif choice=="2": self.email()
            elif choice=="3": self.phone()
            elif choice=="4": self.dork()
            elif choice=="5": self.ip()
            elif choice=="0": 
                console.print("\n[red]🔥 MONO ULTIMATE - Shutting Down[/]\n")
                sys.exit()

if __name__ == "__main__":
    try:
        app = MonoUltimate()
        app.menu()
    except KeyboardInterrupt:
        console.print("\n[red]⚠️  Interrupted[/]")
        sys.exit(0)
