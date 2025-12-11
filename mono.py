#!/usr/bin/env python3
"""
MONO ULTIMATE RECON - V6.0 (MONSTER EDITION)
===========================================
Dibuat oleh Rasya - Untuk Tujuan Edukasi dan Audit Keamanan.
Dilarang keras menggunakan tools ini untuk kejahatan.
"""

import sys
import os
import re
import socket
import time
import json
import random
from datetime import datetime
from urllib.parse import quote, urlparse, urljoin, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.tree import Tree
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt
from rich import box
from rich.layout import Layout

# Optional dependencies handling
try:
    import phonenumbers
    PHONENUMBERS_AVAIL = True
except ImportError:
    PHONENUMBERS_AVAIL = False

console = Console()

class MonoUltimateRecon:
    def __init__(self):
        self.found_data = {}
        self.target_user = ""
        self.target_domain = ""
        
        # Rotasi User-Agent (Anti-Blokir)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        ]
        
        self.session = requests.Session()
        self._rotate_user_agent()
        self.session.headers.update({'Connection': 'keep-alive'})
        
        # Wordlist Subdomain
        self.subdomain_wordlist = [
            'www', 'admin', 'administrator', 'secure', 'portal', 'login', 'siswa', 'guru',
            'dev', 'development', 'test', 'staging', 'mail', 'email', 'webmail', 'ppdb',
            'ftp', 'ssh', 'sftp', 'api', 'backend', 'frontend', 'dashboard', 'ujian',
            'cpanel', 'whm', 'webdisk', 'elearning', 'perpus', 'dapodik', 'raport',
            'server', 'vpn', 'proxy', 'db', 'database', 'sql', 'mysql', 'lab', 'workshop'
        ]
        
        # Sensitive Files
        self.sensitive_files = [
            '.env', '.git/config', 'backup.sql', 'backup.zip', 'public.zip',
            'phpinfo.php', 'config.php', 'database.php', 'wp-config.php',
            '.htaccess', 'admin/', 'administrator/', 'wp-admin/',
            'debug.log', 'error.log', 'dump.sql', 'secret.txt', 'password.txt'
        ]
        
        # WAF Signatures
        self.waf_signatures = {
            'Cloudflare': ['cloudflare', '__cfduid', 'cf-ray'],
            'Cloudfront': ['cloudfront', 'x-amz-cf-id'],
            'Wordfence': ['wordfence', 'wfwaf-authcookie']
        }
        
        # Payloads
        self.sqli_payloads = ["'", "' OR '1'='1", "' OR 1=1--", "' UNION SELECT NULL--"]
        self.xss_payloads = ['<script>alert(1)</script>', '" onmouseover="alert(1)']
        
        # CMS Signatures
        self.cms_signatures = {
            'WordPress': {'meta': ['WordPress'], 'files': ['wp-content/']},
            'Joomla': {'meta': ['Joomla'], 'files': ['administrator/']},
            'Laravel': {'headers': ['laravel_session', 'X-CSRF-TOKEN']},
            'Drupal': {'meta': ['Drupal']}
        }
        
        # Ports
        self.critical_ports = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 443: 'HTTPS', 445: 'SMB', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 8080: 'HTTP-Proxy', 27017: 'MongoDB'
        }
        
        # Username Platforms
        self.platforms = {
            "SOCIAL": [("Instagram", "https://instagram.com/{}"), ("TikTok", "https://tiktok.com/@{}"), ("Twitter", "https://twitter.com/{}"), ("Facebook", "https://facebook.com/{}")],
            "DEV": [("GitHub", "https://github.com/{}"), ("GitLab", "https://gitlab.com/{}")],
            "GAMING": [("Steam", "https://steamcommunity.com/id/{}"), ("Roblox", "https://roblox.com/user.aspx?username={}")]
        }

    def _rotate_user_agent(self):
        self.session.headers.update({'User-Agent': random.choice(self.user_agents)})

    def banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        banner_text = Text(r"""
███╗   ███╗ ██████╗ ███╗   ██╗ ██████╗ 
████╗ ████║██╔═══██╗████╗  ██║██╔═══██╗
██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║
██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║
██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ 
        """, style="bold cyan")
        console.print(Align.center(banner_text))
        console.print(Align.center(Text("🔥 MONSTER EDITION - V6.0", style="bold yellow")))
        console.print(Align.center(Text("🔐 Created by psociety", style="dim white")))
        console.print(Align.center(Text(f"📅 {datetime.now().strftime('%Y-%m-%d')}", style="dim cyan")))
        print()

    # ==================== FITUR 1: WEBSITE VULN SCANNER (MONSTER) ====================
    def website_vuln_scanner(self):
        self.banner()
        console.print(Panel("[bold cyan]🔍 WEBSITE VULNERABILITY SCANNER v6.0[/]\n[dim]WAF + CMS + SQLi + XSS + Files[/]", border_style="cyan"))
        
        target = Prompt.ask("[bold yellow]🌐 Enter target URL[/]")
        if not target.startswith(('http', 'https')): target = f"https://{target}"
        self.target_domain = target
        
        results = {'waf': [], 'cms': [], 'files': [], 'headers': {}, 'sqli': [], 'xss': [], 'links': []}
        
        console.print(f"\n[bold green]▶ Starting MONSTER scan on: {target}[/]\n")
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), console=console) as p:
            # 1. WAF
            t1 = p.add_task("[red]Checking WAF...", total=1)
            results['waf'] = self._detect_waf(target)
            p.update(t1, completed=1)
            
            # 2. CMS
            t2 = p.add_task("[cyan]Detecting CMS...", total=1)
            results['cms'] = self._detect_cms(target)
            p.update(t2, completed=1)
            
            # 3. Files
            t3 = p.add_task("[yellow]Hunting Files...", total=len(self.sensitive_files))
            results['files'] = self._hunt_files(target)
            p.update(t3, completed=len(self.sensitive_files))
            
            # 4. SQLi & XSS
            t4 = p.add_task("[magenta]Injecting Payloads...", total=2)
            results['sqli'] = self._scan_sqli(target)
            p.advance(t4)
            results['xss'] = self._scan_xss(target)
            p.advance(t4)

        self._display_vuln_results(results, target)
        input("\n[dim]Press Enter to continue...[/]")

    def _detect_waf(self, url):
        detected = []
        try:
            r = self.session.get(url, timeout=5)
            headers = str(r.headers).lower()
            text = r.text.lower()
            for waf, sigs in self.waf_signatures.items():
                if any(s in headers or s in text for s in sigs): detected.append(waf)
        except: pass
        return detected if detected else ["None"]

    def _detect_cms(self, url):
        detected = []
        try:
            r = self.session.get(url, timeout=5)
            text = r.text
            for cms, sigs in self.cms_signatures.items():
                if any(m in text for m in sigs.get('meta', [])): detected.append(cms)
                elif any(f in text for f in sigs.get('files', [])): detected.append(cms)
        except: pass
        return detected if detected else ["Unknown"]

    def _hunt_files(self, base):
        found = []
        with ThreadPoolExecutor(max_workers=20) as exe:
            futures = [exe.submit(self._check_url, f"{base}/{f}") for f in self.sensitive_files]
            for f in as_completed(futures):
                if f.result(): found.append(f.result())
        return found

    def _check_url(self, url):
        try:
            r = self.session.head(url, timeout=3)
            if r.status_code == 200: return url
        except: pass
        return None

    def _scan_sqli(self, url):
        vuln = []
        if "?" not in url: return []
        for payload in self.sqli_payloads:
            try:
                target = f"{url}{quote(payload)}"
                r = self.session.get(target, timeout=3)
                if "sql" in r.text.lower() or "syntax" in r.text.lower():
                    vuln.append(payload)
                    break 
            except: pass
        return vuln

    def _scan_xss(self, url):
        vuln = []
        if "?" not in url: return []
        for payload in self.xss_payloads:
            try:
                target = f"{url}{quote(payload)}"
                r = self.session.get(target, timeout=3)
                if payload in r.text:
                    vuln.append(payload)
                    break
            except: pass
        return vuln

    def _display_vuln_results(self, res, target):
        self.banner()
        console.print(Panel(f"[bold cyan]📊 RESULTS: {target}[/]", border_style="cyan"))
        
        if "None" not in res['waf']: console.print(f"[bold red]⚠️  WAF DETECTED: {', '.join(res['waf'])}[/]")
        else: console.print("[green]✅ No WAF Detected[/]")
        
        console.print(f"\n[bold yellow]📦 CMS:[/]{', '.join(res['cms'])}")
        
        console.print("\n[bold red]📂 SENSITIVE FILES:[/]")
        if res['files']: 
            for f in res['files']: console.print(f"  - {f}")
        else: console.print("  [green]None found[/]")

        console.print("\n[bold magenta]💉 VULNERABILITIES:[/]")
        if res['sqli']: console.print(f"  [red]⚠️  POSSIBLE SQLi FOUND with payload: {res['sqli'][0]}[/]")
        else: console.print("  [green]No SQLi Errors[/]")
        
        if res['xss']: console.print(f"  [red]⚠️  POSSIBLE XSS FOUND with payload: {res['xss'][0]}[/]")
        else: console.print("  [green]No Reflected XSS[/]")

    # ==================== FITUR 2: SUBDOMAIN SCANNER ====================
    def subdomain_scanner(self):
        self.banner()
        console.print(Panel("[bold cyan]🌐 SUBDOMAIN SCANNER v6.0[/]", border_style="cyan"))
        domain = Prompt.ask("[bold yellow]Enter domain[/]")
        
        found = []
        with Progress(SpinnerColumn(), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console) as p:
            task = p.add_task("Scanning...", total=len(self.subdomain_wordlist))
            with ThreadPoolExecutor(max_workers=50) as exe:
                futures = [exe.submit(self._check_sub, f"{sub}.{domain}") for sub in self.subdomain_wordlist]
                for f in as_completed(futures):
                    if f.result(): found.append(f.result())
                    p.advance(task)
        
        self.banner()
        console.print(f"[bold green]Found {len(found)} subdomains for {domain}:[/]")
        t = Table(box=box.SIMPLE); t.add_column("Subdomain"); t.add_column("IP")
        for s, ip in sorted(found): t.add_row(s, ip)
        console.print(t)
        input("\nEnter...")

    def _check_sub(self, domain):
        try:
            ip = socket.gethostbyname(domain)
            return (domain, ip)
        except: return None

    # ==================== FITUR 3: PORT SCANNER (FIXED) ====================
    def port_scanner(self):
        self.banner()
        console.print(Panel("[bold cyan]🔌 NINJA PORT SCANNER v6.0[/]", border_style="cyan"))
        target = Prompt.ask("[bold yellow]Enter IP/Domain[/]")
        
        try:
            ip = socket.gethostbyname(target)
        except:
            console.print("[red]Invalid Host[/]"); time.sleep(1); return

        open_ports = []
        console.print(f"\n[green]Scanning {ip}...[/]\n")
        
        with Progress(SpinnerColumn(), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console) as p:
            # INI BAGIAN YANG TADI TERPOTONG, SEKARANG SUDAH LENGKAP
            task = p.add_task("Scanning Ports...", total=len(self.critical_ports))
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = {executor.submit(self._scan_port, ip, port): port for port in self.critical_ports}
                
                for future in as_completed(futures):
                    res = future.result()
                    if res: open_ports.append(res)
                    p.advance(task)

        self.banner()
        console.print(Panel(f"[bold cyan]🔌 OPEN PORTS: {target} ({ip})[/]"))
        if open_ports:
            t = Table(box=box.ROUNDED)
            t.add_column("Port", style="cyan"); t.add_column("Service", style="yellow"); t.add_column("Status", style="red")
            for p in sorted(open_ports):
                t.add_row(str(p), self.critical_ports[p], "OPEN")
            console.print(t)
        else: console.print("[green]✅ No open critical ports found[/]")
        input("\nPress Enter...")

    def _scan_port(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5) # Cepat
            if s.connect_ex((ip, port)) == 0:
                s.close(); return port
            s.close()
        except: pass
        return None

    # ==================== FITUR 4: USERNAME SCANNER ====================
    def username_scanner(self):
        self.banner()
        console.print(Panel("[bold cyan]👤 USERNAME SCANNER[/]", border_style="cyan"))
        user = Prompt.ask("[bold yellow]Enter Username[/]")
        if not user: return

        found = {}
        checks = []
        for cat, sites in self.platforms.items():
            for site, url in sites: checks.append((cat, site, url))

        with Progress(SpinnerColumn(), BarColumn(), console=console) as p:
            task = p.add_task("Scanning...", total=len(checks))
            with ThreadPoolExecutor(max_workers=30) as exe:
                futures = {exe.submit(self._check_user, c, s, u.format(user)): s for c, s, u in checks}
                for f in as_completed(futures):
                    res = f.result()
                    if res:
                        c, s, u = res
                        if c not in found: found[c] = []
                        found[c].append((s, u))
                    p.advance(task)

        self.banner()
        if not found: console.print("[red]No footprints found.[/]")
        else:
            tree = Tree(f"[green]Target: {user}[/]")
            for c, items in found.items():
                b = tree.add(f"[yellow]{c}[/]")
                for s, u in items: b.add(f"[cyan]{s}[/] - {u}")
            console.print(tree)
        input("\nEnter...")

    def _check_user(self, cat, site, url):
        try:
            r = self.session.get(url, timeout=5)
            if r.status_code == 200 and "not found" not in r.text.lower():
                return (cat, site, url)
        except: pass
        return None

    # ==================== MAIN MENU ====================
    def main_menu(self):
        while True:
            self.banner()
            t = Table(box=box.DOUBLE_EDGE, show_header=False)
            t.add_column("Opt", justify="center", style="cyan bold")
            t.add_column("Desc")
            t.add_row("1", "WEBSITE VULN SCANNER (Monster)")
            t.add_row("2", "SUBDOMAIN SCANNER")
            t.add_row("3", "PORT SCANNER")
            t.add_row("4", "USERNAME SCANNER")
            t.add_row("0", "[red]EXIT[/]")
            
            console.print(Panel(t, title="MENU", border_style="cyan"))
            c = Prompt.ask("[bold green]mono~#[/]", choices=["1","2","3","4","0"])
            
            if c == "1": self.website_vuln_scanner()
            elif c == "2": self.subdomain_scanner()
            elif c == "3": self.port_scanner()
            elif c == "4": self.username_scanner()
            elif c == "0": sys.exit()

if __name__ == "__main__":
    try:
        app = MonoUltimateRecon()
        app.main_menu()
    except KeyboardInterrupt:
        sys.exit()
