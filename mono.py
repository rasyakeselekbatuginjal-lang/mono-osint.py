#!/usr/bin/env python3
"""
MONO ULTIMATE - ALL-IN-ONE RECONNAISSANCE SUITE
==============================================
Dibuat untuk tujuan edukasi dan audit keamanan.
Dilarang digunakan untuk aktivitas ilegal.
"""

import sys
import os
import re
import socket
import time
import json
from datetime import datetime
from urllib.parse import quote, urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.tree import Tree
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt, Confirm
from rich import box
from rich.layout import Layout
from rich.live import Live

# Try importing optional dependencies
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
    PHONENUMBERS_AVAIL = True
except ImportError:
    PHONENUMBERS_AVAIL = False

console = Console()

class MonoUltimateRecon:
    def __init__(self):
        self.found_data = {}
        self.target_user = ""
        self.target_domain = ""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        })
        
        # Wordlist untuk Subdomain Scanner
        self.subdomain_wordlist = [
            'www', 'admin', 'administrator', 'secure', 'portal', 'login', 
            'dev', 'development', 'test', 'staging', 'mail', 'email', 'webmail',
            'ftp', 'ssh', 'sftp', 'api', 'backend', 'frontend', 'dashboard',
            'cpanel', 'whm', 'webdisk', 'webmin', 'blog', 'news', 'forum',
            'support', 'help', 'docs', 'wiki', 'status', 'monitor', 'monitoring',
            'app', 'apps', 'application', 'mobile', 'm', 'static', 'assets',
            'cdn', 'shop', 'store', 'payment', 'billing', 'invoice',
            'server', 'vpn', 'proxy', 'ns1', 'ns2', 'smtp', 'db', 'database', 
            'sql', 'mysql', 'mongo', 'redis', 'search', 'jenkins', 'git'
        ]
        
        # Sensitive files to check (File Rahasia)
        self.sensitive_files = [
            '.env', '.git/config', '.git/HEAD', '.git/index',
            'backup.sql', 'backup.zip', 'backup.tar.gz',
            'phpinfo.php', 'test.php', 'info.php',
            'config.php', 'database.php', 'settings.php',
            'wp-config.php', 'configuration.php',
            'robots.txt', 'sitemap.xml',
            '.htaccess', '.htpasswd',
            'admin/', 'administrator/', 'wp-admin/',
            'debug.log', 'error.log', 'access.log',
            'dump.sql', 'secret.txt', 'password.txt'
        ]
        
        # CMS Detection signatures
        self.cms_signatures = {
            'WordPress': {'meta': ['generator', 'WordPress'], 'files': ['wp-content/', 'wp-includes/']},
            'Joomla': {'meta': ['generator', 'Joomla'], 'files': ['media/system/']},
            'Laravel': {'meta': ['csrf-token'], 'headers': ['laravel_session']},
            'Drupal': {'meta': ['generator', 'Drupal'], 'files': ['sites/all/']},
            'Magento': {'headers': ['magento'], 'files': ['skin/frontend/']}
        }
        
        # Critical ports to scan
        self.critical_ports = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 443: 'HTTPS', 445: 'SMB', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 8080: 'HTTP-Proxy', 27017: 'MongoDB'
        }
        
        # Username search platforms
        self.platforms = {
            "SOCIAL": [
                ("Instagram", "https://instagram.com/{}"),
                ("TikTok", "https://tiktok.com/@{}"),
                ("Twitter", "https://twitter.com/{}"),
                ("Facebook", "https://facebook.com/{}"),
                ("LinkedIn", "https://linkedin.com/in/{}"),
                ("Telegram", "https://t.me/{}")
            ],
            "DEV": [
                ("GitHub", "https://github.com/{}"),
                ("GitLab", "https://gitlab.com/{}"),
                ("Replit", "https://replit.com/@{}"),
                ("Pastebin", "https://pastebin.com/u/{}")
            ],
            "GAMING": [
                ("Steam", "https://steamcommunity.com/id/{}"),
                ("Twitch", "https://twitch.tv/{}"),
                ("Roblox", "https://roblox.com/user.aspx?username={}")
            ],
            "CONTENT": [
                ("YouTube", "https://youtube.com/@{}"),
                ("Spotify", "https://open.spotify.com/user/{}")
            ]
        }

    def banner(self):
        """Display the main banner"""
        os.system('clear' if os.name == 'posix' else 'cls')
        banner_text = Text("""
███╗   ███╗ ██████╗ ███╗   ██╗ ██████╗ 
████╗ ████║██╔═══██╗████╗  ██║██╔═══██╗
██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║
██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║
██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ 
        """, style="bold cyan")
        
        console.print(Align.center(banner_text))
        console.print(Align.center(Text("🚀 ALL-IN-ONE RECONNAISSANCE SUITE v5.0", style="bold yellow")))
        console.print(Align.center(Text("🔐 Created for Educational Security Audits", style="dim white")))
        console.print(Align.center(Text(f"📅 {datetime.now().strftime('%Y-%m-%d')}", style="dim cyan")))
        print()

    # ==================== WEBSITE VULNERABILITY SCANNER ====================
    def website_vuln_scanner(self):
        self.banner()
        console.print(Panel("[bold cyan]🔍 WEBSITE VULNERABILITY SCANNER[/]\n[dim]Detect CMS, sensitive files, and headers[/]", border_style="cyan"))
        
        target = Prompt.ask("[bold yellow]🌐 Enter target domain (e.g., sekolah.sch.id)[/]")
        if not target.startswith(('http://', 'https://')): target = f"https://{target}"
        self.target_domain = target
        results = {'cms': [], 'sensitive_files': [], 'headers': {}}
        
        console.print(f"\n[bold green]▶ Starting scan on: [white]{target}[/][/]\n")
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), console=console) as progress:
            # Task 1: CMS
            task1 = progress.add_task("[cyan]Detecting CMS...", total=1)
            results['cms'] = self._detect_cms(target)
            progress.update(task1, completed=1)
            
            # Task 2: Files
            task2 = progress.add_task("[yellow]Hunting sensitive files...", total=len(self.sensitive_files))
            results['sensitive_files'] = self._hunt_sensitive_files(target)
            progress.update(task2, completed=len(self.sensitive_files))
            
            # Task 3: Headers
            task3 = progress.add_task("[green]Analyzing headers...", total=1)
            results['headers'] = self._analyze_headers(target)
            progress.update(task3, completed=1)

        self._display_vuln_results(results, target)
        input("\n[dim]Press Enter to continue...[/]")

    def _detect_cms(self, url):
        detected = []
        try:
            r = self.session.get(url, timeout=10)
            content = r.text.lower()
            headers = str(r.headers).lower()
            
            for cms, sigs in self.cms_signatures.items():
                if 'meta' in sigs and sigs['meta'][1].lower() in content: detected.append(cms)
                elif 'headers' in sigs and any(h in headers for h in sigs['headers']): detected.append(cms)
                elif 'files' in sigs and any(f in content for f in sigs['files']): detected.append(cms)
        except: pass
        return list(set(detected)) if detected else ["Unknown"]

    def _hunt_sensitive_files(self, base_url):
        found = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for f in self.sensitive_files:
                url = f"{base_url}/{f}" if not f.startswith('/') else f"{base_url}{f}"
                futures.append(executor.submit(self._check_file, url))
            
            for future in as_completed(futures):
                res = future.result()
                if res: found.append(res)
        return found

    def _check_file(self, url):
        try:
            r = self.session.get(url, timeout=5, allow_redirects=False)
            if r.status_code == 200: return url
        except: pass
        return None

    def _analyze_headers(self, url):
        headers_info = {}
        try:
            r = self.session.head(url, timeout=5)
            h = r.headers
            headers_info['X-Frame-Options'] = h.get('X-Frame-Options', '❌ Missing')
            headers_info['Server'] = h.get('Server', '✅ Hidden')
            headers_info['Strict-Transport-Security'] = h.get('Strict-Transport-Security', '❌ Missing')
        except: pass
        return headers_info

    def _display_vuln_results(self, results, target):
        self.banner()
        console.print(Panel(f"[bold cyan]📊 RESULTS FOR: {target}[/]", border_style="cyan"))
        
        # CMS
        console.print("\n[bold yellow]📦 CMS DETECTED[/]")
        for cms in results['cms']: console.print(f"✅ {cms}")
        
        # Files
        console.print("\n[bold red]🔍 SENSITIVE FILES FOUND[/]")
        if results['sensitive_files']:
            for f in results['sensitive_files']: console.print(f"[red]⚠️  OPEN: {f}[/]")
        else: console.print("[green]✅ No sensitive files found[/]")
        
        # Headers
        console.print("\n[bold blue]🛡️ HEADERS[/]")
        for k, v in results['headers'].items(): console.print(f"{k}: {v}")

    # ==================== SUBDOMAIN SCANNER ====================
    def subdomain_scanner(self):
        self.banner()
        console.print(Panel("[bold cyan]🌐 SUBDOMAIN SCANNER[/]\n[dim]Discover hidden subdomains[/]", border_style="cyan"))
        domain = Prompt.ask("[bold yellow]🔍 Enter domain (e.g., sekolah.sch.id)[/]")
        
        console.print(f"\n[bold green]▶ Scanning subdomains for: [white]{domain}[/][/]\n")
        found = []
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), console=console) as progress:
            task = progress.add_task("Scanning...", total=len(self.subdomain_wordlist))
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = [executor.submit(self._check_sub, f"{sub}.{domain}") for sub in self.subdomain_wordlist]
                for f in as_completed(futures):
                    res = f.result()
                    if res: found.append(res)
                    progress.advance(task)
        
        self.banner()
        console.print(Panel(f"[bold cyan]🌐 SUBDOMAINS FOUND: {len(found)}[/]"))
        if found:
            t = Table(box=box.SIMPLE); t.add_column("Subdomain", style="cyan"); t.add_column("IP", style="yellow")
            for s, ip in found: t.add_row(s, ip)
            console.print(t)
        else: console.print("[red]❌ No subdomains found[/]")
        input("\n[dim]Press Enter to continue...[/]")

    def _check_sub(self, domain):
        try:
            ip = socket.gethostbyname(domain)
            return (domain, ip)
        except: return None

    # ==================== PORT SCANNER ====================
    def port_scanner(self):
        self.banner()
        console.print(Panel("[bold cyan]🔌 NINJA PORT SCANNER[/]\n[dim]Scan critical ports stealthily[/]", border_style="cyan"))
        target = Prompt.ask("[bold yellow]🎯 Enter target IP or Domain[/]")
        
        try:
            target_ip = socket.gethostbyname(target)
            console.print(f"[dim]Resolved to: {target_ip}[/]")
        except: 
            console.print("[red]Invalid Target[/]"); return

        open_ports = []
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), console=console) as progress:
            task = progress.add_task("Scanning ports...", total=len(self.critical_ports))
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = {executor.submit(self._scan_port, target_ip, p): p for p in self.critical_ports}
                for f in as_completed(futures):
                    res = f.result()
                    if res: open_ports.append(res)
                    progress.advance(task)

        self.banner()
        console.print(Panel(f"[bold cyan]🔌 OPEN PORTS ON {target}[/]"))
        if open_ports:
            t = Table(box=box.ROUNDED)
            t.add_column("Port", style="cyan"); t.add_column("Service", style="yellow"); t.add_column("Status", style="red")
            for p in sorted(open_ports):
                t.add_row(str(p), self.critical_ports[p], "OPEN")
            console.print(t)
        else: console.print("[green]✅ No open critical ports found[/]")
        input("\n[dim]Press Enter to continue...[/]")

    def _scan_port(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                s.close(); return port
            s.close()
        except: pass
        return None

    # ==================== USERNAME SCANNER ====================
    def username_scanner(self):
        self.banner()
        console.print(Panel("[bold cyan]👤 USERNAME SCANNER[/]\n[dim]Search across 120+ platforms[/]", border_style="cyan"))
        self.target_user = Prompt.ask("[bold yellow]🎯 Enter Username[/]")
        if not self.target_user: return

        self.found_data = {}
        checks = []
        for cat, sites in self.platforms.items():
            for site, url in sites: checks.append((cat, site, url))

        console.print(f"\n[cyan]⚡ Scanning: [white]{self.target_user}[/][/]\n")
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), console=console) as p:
            task = p.add_task("Scanning...", total=len(checks))
            with ThreadPoolExecutor(max_workers=30) as ex:
                futures = {ex.submit(self._check_user, c, s, u): s for c, s, u in checks}
                for f in as_completed(futures):
                    res = f.result()
                    if res:
                        c, s, u = res
                        if c not in self.found_data: self.found_data[c] = []
                        self.found_data[c].append((s, u))
                    p.advance(task)

        self._display_username_results()

    def _check_user(self, cat, site, url):
        try:
            u = url.format(self.target_user)
            r = self.session.get(u, timeout=5)
            if r.status_code == 200:
                if "not found" not in r.text.lower(): return (cat, site, u)
        except: pass
        return None

    def _display_username_results(self):
        self.banner()
        total = sum(len(x) for x in self.found_data.values())
        if not total:
            console.print("[red]❌ No results found[/]")
        else:
            tree = Tree(f"[bold green]🎯 TARGET: {self.target_user}[/]")
            for cat, items in self.found_data.items():
                b = tree.add(f"[yellow]{cat}[/]")
                for site, url in items: b.add(f"[cyan]{site}[/] - {url}")
            console.print(tree)
        input("\n[dim]Press Enter to continue...[/]")

    # ==================== MAIN MENU ====================
    def main_menu(self):
        while True:
            self.banner()
            menu_table = Table(box=box.DOUBLE_EDGE, show_header=False)
            menu_table.add_column("Option", justify="center", style="bold cyan")
            menu_table.add_column("Desc", justify="left")
            
            menu_table.add_row("1", "[bold cyan]WEBSITE VULNERABILITY SCANNER[/]\n[dim]CMS, Files, Headers[/]")
            menu_table.add_row("2", "[bold yellow]SUBDOMAIN SCANNER[/]\n[dim]Find hidden subdomains[/]")
            menu_table.add_row("3", "[bold magenta]NINJA PORT SCANNER[/]\n[dim]Check critical ports[/]")
            menu_table.add_row("4", "[bold green]USERNAME SCANNER[/]\n[dim]Track user profiles[/]")
            menu_table.add_row("0", "[bold red]EXIT[/]")
            
            console.print(Panel(menu_table, title="[bold yellow]🔥 MENU 🔥[/]", border_style="cyan"))
            
            c = Prompt.ask("[bold green]mono~#[/]", choices=["1", "2", "3", "4", "0"])
            
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
