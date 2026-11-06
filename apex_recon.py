#!/usr/bin/env python3
"""apex_recon.py - All recon modules"""
import socket
import ssl
import re
from urllib.parse import urljoin, quote
from concurrent.futures import ThreadPoolExecutor
from collections import deque
from apex_utils import (
    p_sub, p_dns, p_whois, p_ssl, p_header, p_isp, p_dir, p_port,
    p_crawl, p_vuln, p_tech, p_secret, p_warn, p_err, p_titan,
)
from apex_config import (
    COMMON_SUBS, COMMON_DIRS, COMMON_PORTS, TECH_SIGNATURES,
    SECRET_PATTERNS, CORS_TEST_ORIGINS, BACKUP_EXTS, TIMEOUT,
)

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    import whois as whois_lib
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


class ReconModules:
    def __init__(self, bot):
        self.bot = bot

    def run_all_recon(self):
        p_titan("Running ALL recon modules...")
        self.subdomain_enumeration()
        self.dns_enumeration()
        self.whois_lookup()
        self.ssl_analysis()
        self.header_enumeration()
        self.isp_information()
        self.directory_bruteforce()
        self.port_scan()
        self.crawler_spider()
        self.vulnerability_scanning()

    def run_full_recon(self):
        p_titan("★ FULL RECON ★")
        self.run_all_recon()
        self.tech_detect()
        self.secret_scan()
        self.cors_scan()
        self.backup_hunt()
        self.git_hunt()
        self.env_hunt()
        self.open_redirect_scan()
        self.lfi_scan()
        self.ssrf_scan()

    def subdomain_enumeration(self):
        def check(sub):
            try:
                fqdn = f"{sub}.{self.bot.hostname}"
                return (fqdn, socket.gethostbyname(fqdn))
            except Exception:
                return None
        with ThreadPoolExecutor(max_workers=20) as ex:
            for res in ex.map(check, COMMON_SUBS):
                if res:
                    self.bot.subdomain_results.append(res)
                    p_sub(f"{res[0]:<40} → {res[1]}")
        return self.bot.subdomain_results

    def dns_enumeration(self):
        if not DNS_AVAILABLE:
            try:
                ips = socket.getaddrinfo(self.bot.hostname, None, socket.AF_INET)
                self.bot.dns_results['A'] = list({i[4][0] for i in ips})
            except Exception:
                pass
            return self.bot.dns_results
        for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]:
            try:
                answers = dns.resolver.resolve(self.bot.hostname, rtype, lifetime=TIMEOUT)
                self.bot.dns_results[rtype] = [str(r) for r in answers]
                p_dns(f"{rtype}: {', '.join(self.bot.dns_results[rtype])[:100]}")
            except Exception:
                pass
        return self.bot.dns_results

    def whois_lookup(self):
        if not WHOIS_AVAILABLE:
            return {}
        try:
            w = whois_lib.whois(self.bot.hostname)
            self.bot.whois_results = {
                "Registrar": str(w.registrar),
                "Created": str(w.creation_date),
                "Expires": str(w.expiration_date),
            }
            for k, v in self.bot.whois_results.items():
                p_whois(f"{k}: {v[:100]}")
        except Exception:
            pass
        return self.bot.whois_results

    def ssl_analysis(self):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            port = 443 if self.bot.port == 80 else self.bot.port
            with socket.create_connection((self.bot.hostname, port), timeout=TIMEOUT) as sock:
                with ctx.wrap_socket(sock, server_hostname=self.bot.hostname) as ssock:
                    cert = ssock.getpeercert()
                    self.bot.ssl_results = {
                        "protocol": ssock.version(),
                        "cipher": ssock.cipher(),
                        "cert": cert,
                    }
                    p_ssl(f"Protocol: {ssock.version()}")
        except Exception as e:
            p_err(f"SSL failed: {e}")
        return self.bot.ssl_results

    def header_enumeration(self):
        try:
            r = self.bot._request('GET', self.bot.base_url)
            self.bot.header_results = dict(r.headers)
            for k, v in r.headers.items():
                p_header(f"{k}: {v[:100]}")
        except Exception as e:
            p_err(f"Header fetch failed: {e}")
        return self.bot.header_results

    def isp_information(self):
        try:
            import requests
            r = requests.get(f"http://ip-api.com/json/{self.bot.ip}", timeout=TIMEOUT)
            if r.status_code == 200:
                d = r.json()
                if d.get('status') == 'success':
                    self.bot.isp_results = d
                    p_isp(f"ISP: {d.get('isp')} | AS: {d.get('as')}")
        except Exception:
            pass
        return self.bot.isp_results

    def directory_bruteforce(self):
        def probe(path):
            try:
                r = self.bot._request('GET', urljoin(self.bot.base_url + "/", path),
                                      allow_redirects=False)
                if r.status_code in (200, 301, 302, 401, 403):
                    return (urljoin(self.bot.base_url + "/", path), r.status_code)
            except Exception:
                pass
            return None
        with ThreadPoolExecutor(max_workers=15) as ex:
            for res in ex.map(probe, COMMON_DIRS):
                if res:
                    self.bot.directory_results.append({"url": res[0], "status": res[1]})
                    p_dir(f"[{res[1]}] {res[0]}")
        return self.bot.directory_results

    def port_scan(self):
        def scan(p):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1.5)
                    if s.connect_ex((self.bot.ip, p)) == 0:
                        return (p, COMMON_PORTS.get(p, "unknown"))
            except Exception:
                pass
            return None
        with ThreadPoolExecutor(max_workers=30) as ex:
            for res in ex.map(scan, list(COMMON_PORTS.keys())):
                if res:
                    self.bot.port_scan_results.append({"port": res[0], "service": res[1]})
                    p_port(f"[OPEN] {res[0]} {res[1]}")
        return self.bot.port_scan_results

    def crawler_spider(self, max_pages=20):
        if not BS4_AVAILABLE:
            return []
        visited, queue = set(), deque([self.bot.base_url])
        from urllib.parse import urlparse
        domain = urlparse(self.bot.base_url).netloc
        count = 0
        while queue and count < max_pages:
            url = queue.popleft()
            if url in visited:
                continue
            visited.add(url)
            count += 1
            try:
                r = self.bot._request('GET', url)
                soup = BeautifulSoup(r.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    full = urljoin(url, a["href"])
                    if urlparse(full).netloc == domain and full not in visited:
                        queue.append(full)
            except Exception:
                pass
        self.bot.crawler_results = [{"url": u} for u in visited]
        return self.bot.crawler_results

    def vulnerability_scanning(self):
        findings = []
        for path in [".env", ".git/config", "robots.txt", "sitemap.xml",
                     "phpinfo.php", "server-status", "backup.zip", "backup.sql"]:
            try:
                r = self.bot._request('GET', urljoin(self.bot.base_url + "/", path))
                if r.status_code == 200:
                    findings.append(f"Exposed: /{path}")
                    p_vuln(f"Exposed file → /{path}")
                    self.bot._add_finding('high', 'exposure', f"Exposed: /{path}",
                                          "", self.bot.base_url + "/" + path)
            except Exception:
                pass
        self.bot.vuln_scan_results = findings
        return findings

    def tech_detect(self):
        try:
            r = self.bot._request('GET', self.bot.base_url)
            haystack = (r.text[:8000] + str(r.headers)).lower()
            for tech, sigs in TECH_SIGNATURES.items():
                for sig in sigs:
                    if sig.lower() in haystack:
                        self.bot.tech_results[tech] = self.bot.tech_results.get(tech, 0) + 1
                        p_tech(f"Detected: {tech}")
                        break
        except Exception as e:
            p_err(f"Tech detect failed: {e}")
        return self.bot.tech_results

    def secret_scan(self):
        try:
            r = self.bot._request('GET', self.bot.base_url)
            for name, pat in SECRET_PATTERNS.items():
                matches = re.findall(pat, r.text)
                if matches:
                    self.bot.secret_results.append({
                        "type": name, "count": len(matches),
                        "sample": str(matches[0])[:80],
                    })
                    p_secret(f"{name}: {len(matches)} found")
        except Exception as e:
            p_err(f"Secret scan failed: {e}")
        return self.bot.secret_results

    def cors_scan(self):
        for origin in CORS_TEST_ORIGINS:
            try:
                r = self.bot._request('GET', self.bot.base_url,
                                      headers={'Origin': origin}, allow_redirects=False)
                acao = r.headers.get('Access-Control-Allow-Origin', '')
                if acao == origin or acao == '*':
                    self.bot.cors_results.append({"origin": origin, "acao": acao})
                    p_warn(f"CORS: {origin} → ACAO:{acao}")
            except Exception:
                pass
        return self.bot.cors_results

    def backup_hunt(self):
        for base in ['index', 'config', 'backup', 'db', '.env', 'wp-config']:
            for ext in BACKUP_EXTS:
                url = urljoin(self.bot.base_url + "/", base + ext)
                try:
                    r = self.bot._request('GET', url, allow_redirects=False)
                    if r.status_code in (200, 301, 302):
                        self.bot.backup_results.append({"url": url, "status": r.status_code})
                        p_warn(f"Backup: {url} ({r.status_code})")
                except Exception:
                    pass
        return self.bot.backup_results

    def git_hunt(self):
        for path in ['/.git/config', '/.git/HEAD', '/.svn/entries', '/.hg/hgrc']:
            try:
                r = self.bot._request('GET', self.bot.base_url + path, allow_redirects=False)
                if r.status_code in (200, 301, 302):
                    self.bot.git_results.append({"url": self.bot.base_url + path,
                                                 "status": r.status_code})
                    p_warn(f"Git: {path} ({r.status_code})")
            except Exception:
                pass
        return self.bot.git_results

    def env_hunt(self):
        for path in ['/.env', '/.env.local', '/config.json', '/web.config',
                     '/settings.py', '/appsettings.json']:
            try:
                r = self.bot._request('GET', self.bot.base_url + path, allow_redirects=False)
                if r.status_code in (200, 301, 302):
                    self.bot.env_results.append({"url": self.bot.base_url + path,
                                                 "status": r.status_code})
                    p_warn(f"Env: {path} ({r.status_code})")
            except Exception:
                pass
        return self.bot.env_results

    def open_redirect_scan(self):
        for p in ['url', 'redirect', 'next', 'return']:
            for pl in ['https://evil.com', '//evil.com']:
                try:
                    test = f"{self.bot.base_url}?{p}={quote(pl)}"
                    r = self.bot._request('GET', test, allow_redirects=False)
                    loc = r.headers.get('Location', '')
                    if 'evil.com' in loc:
                        self.bot.open_redirect_results.append({"param": p, "payload": pl})
                        p_warn(f"Open Redirect: {p}={pl}")
                        break
                except Exception:
                    pass
        return self.bot.open_redirect_results

    def lfi_scan(self):
        for p in ['file', 'page', 'path', 'include']:
            for pl in ['../../../../etc/passwd', '....//....//....//etc/passwd']:
                try:
                    test = f"{self.bot.base_url}?{p}={quote(pl)}"
                    r = self.bot._request('GET', test, allow_redirects=False)
                    if 'root:x:' in r.text:
                        self.bot.lfi_results.append({"param": p, "payload": pl})
                        p_vuln(f"LFI: {p}")
                        break
                except Exception:
                    pass
        return self.bot.lfi_results

    def ssrf_scan(self):
        for p in ['url', 'uri', 'link', 'target']:
            for pl in ['http://127.0.0.1', 'http://169.254.169.254/latest/meta-data/']:
                try:
                    test = f"{self.bot.base_url}?{p}={quote(pl)}"
                    r = self.bot._request('GET', test, allow_redirects=False)
                    if r.status_code in (200, 201, 202):
                        self.bot.ssrf_results.append({"param": p, "payload": pl})
                        p_vuln(f"SSRF: {p}")
                        break
                except Exception:
                    pass
        return self.bot.ssrf_results
