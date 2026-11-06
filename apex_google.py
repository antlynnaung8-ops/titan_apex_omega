#!/usr/bin/env python3
"""apex_google.py - Google Account + Google Suspicious Server cleaner"""
import datetime
from apex_utils import p_google_acc, p_google_sus, p_crit, p_ok, p_err, p_okay
from apex_config import (
    GOOGLE_ACCOUNT_SERVER_SIGNATURES, GOOGLE_SUSPICIOUS_SERVER_SIGNATURES,
    GOOGLE_ACCOUNT_CLEANER_PATHS, GOOGLE_SUSPICIOUS_SERVER_PATHS,
    APIKEY_CLEANER_PATHS, CLEANER_ALL_COOKIES_PATHS, CLEANER_SYSTEM_PATHS,
    COOLDOWN_CLEANER_PATHS,
)


class GoogleSuspiciousCleaner:
    def __init__(self, bot):
        self.bot = bot

    # ---------- Google Account ----------
    def detect_google_account_copy(self):
        result = self.bot.google_account_copy_results
        url = (self.bot.target if self.bot.mode == 'link'
               else self.bot.base_url)
        print("\n=== GOOGLE ACCOUNT DETECTION ===")
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            body = r.text.lower()
            headers_lower = {k.lower(): v.lower() for k, v in r.headers.items()}
            headers_combined = "\n".join(f"{k}: {v}" for k, v in headers_lower.items())
            score = 0
            for acc_name, sigs in GOOGLE_ACCOUNT_SERVER_SIGNATURES.items():
                for h in sigs.get('hosts', []):
                    if h.lower() in self.bot.hostname.lower() or h.lower() in body:
                        if not any(m['host'] == h for m in result['matched_hosts']):
                            result['matched_hosts'].append({'host': h, 'type': acc_name})
                            score += 4
                            p_google_acc(f"Google Host: {acc_name} → {h}")
                for sig in sigs.get('headers', []):
                    if sig in headers_combined:
                        if not any(m['signature'] == sig for m in result['matched_headers']):
                            result['matched_headers'].append({'signature': sig, 'type': acc_name})
                            score += 3
                            p_google_acc(f"Google Header: {acc_name} → {sig}")
                for sig in sigs.get('body', []):
                    if sig.lower() in body:
                        if not any(m['signature'] == sig for m in result['matched_types']):
                            result['matched_types'].append({'signature': sig, 'type': acc_name})
                            score += 2
                            p_google_acc(f"Google Body: {acc_name} → {sig}")
            result['copy_score'] = score
            result['is_copy'] = score >= 5
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"GOOGLE ACCOUNT DETECTED! Score: {result['copy_score']}")
                self._instant_google_account_clean(result)
            else:
                p_ok(f"No Google Account (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Google Account detection failed: {e}")
        return result

    def _instant_google_account_clean(self, result):
        before = self.bot.cleaner_stats['total_cleaned']
        self.run_google_account_cleaner()
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['google_account_system_cleaned'] += 1

    def run_google_account_cleaner(self):
        total = (self.bot.cleaner.clean_group('google_account', GOOGLE_ACCOUNT_CLEANER_PATHS) +
                 self.bot.cleaner.clean_group('apikey', APIKEY_CLEANER_PATHS) +
                 self.bot.cleaner.clean_group('all_cookies', CLEANER_ALL_COOKIES_PATHS))
        total += self._clean_google_specific()
        self.bot.cleaner_stats['total_cleaned'] += total
        self.bot.cleaner_stats['google_account_cleaned'] += total
        p_ok(f"Google Account cleaner: {total} items")
        return total

    def _clean_google_specific(self):
        cleaned = 0
        for path in ['/accounts/signin/', '/accounts/v3/signin/',
                     '/accounts/o/oauth2/', '/accounts/oauth2/',
                     '/accounts/ServiceLogin', '/accounts/AccountChooser',
                     '/accounts/Logout', '/accounts/recovery',
                     '/accounts/reset-password', '/accounts/suspicious',
                     '/myaccount/personal-info', '/myaccount/security',
                     '/myaccount/privacy', '/myaccount/data',
                     '/myaccount/suspicious',
                     '/oauth2/token', '/oauth2/auth', '/oauth2/revoke',
                     '/signin/', '/v3/signin/', '/gsi/client',
                     '/sessions', '/session', '/session/tokens',
                     '/tokens', '/token', '/keys', '/key',
                     '/credentials', '/credential']:
            try:
                url = self.bot.base_url + path
                r = self.bot._request('GET', url, timeout=3, allow_redirects=False)
                if r.status_code in (200, 301, 302, 403):
                    try:
                        self.bot.session.delete(url, timeout=3, verify=False)
                    except Exception:
                        pass
                    cleaned += 1
                    self.bot.cleaner_stats['okay_signals'] += 1
                    p_okay(f"OKAY - GOOGLE CLEANED: {path}")
            except Exception:
                pass
        return cleaned

    def universal_google_account_clean(self):
        p_google_acc("=== GOOGLE ACCOUNT CLEAN ===")
        result = self.detect_google_account_copy()
        self.detect_google_suspicious_server()
        return result

    # ---------- Google Suspicious Server ----------
    def _analyze_suspicious(self, body_raw, headers, status_code, result, weight=1):
        body = body_raw.lower()
        headers_lower = {k.lower(): v.lower() for k, v in headers.items()}
        headers_combined = "\n".join(f"{k}: {v}" for k, v in headers_lower.items())
        score = 0
        for sus_name, sigs in GOOGLE_SUSPICIOUS_SERVER_SIGNATURES.items():
            for sig in sigs.get('headers', []):
                if sig in headers_combined:
                    if not any(m['signature'] == sig for m in result['matched_headers']):
                        result['matched_headers'].append(
                            {'signature': sig, 'type': sus_name, 'source': 'header'})
                        score += 4 * weight
                        p_google_sus(f"Suspicious Header: {sus_name} → {sig}")
            for sig in sigs.get('body', []):
                if sig.lower() in body:
                    if not any(m['signature'] == sig for m in result['matched_bodies']):
                        result['matched_bodies'].append(
                            {'signature': sig, 'type': sus_name, 'source': 'body'})
                        score += 3 * weight
                        p_google_sus(f"Suspicious Body: {sus_name} → {sig}")
            if status_code in sigs.get('status_codes', []):
                if status_code not in result['matched_status_codes']:
                    result['matched_status_codes'].append(status_code)
                    score += 2 * weight
                    p_google_sus(f"Suspicious Status: {status_code} ({sus_name})")
        return score

    def detect_google_suspicious_server(self):
        result = self.bot.google_suspicious_copy_results
        print("\n=== GOOGLE SUSPICIOUS SERVER DETECTION ===")
        url = self.bot.target if self.bot.mode == 'link' else self.bot.base_url
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            score = self._analyze_suspicious(r.text, r.headers, r.status_code, result, weight=1)
            deep_score = 0
            for path in GOOGLE_SUSPICIOUS_SERVER_PATHS:
                try:
                    r2 = self.bot._request('GET', self.bot.base_url + path,
                                           timeout=3, allow_redirects=False)
                    if r2.status_code in (200, 201, 202, 204, 403, 429, 500, 502, 503, 504):
                        deep_score += 2
                        result['matched_types'].append({
                            'type': 'Deep-Path', 'path': path, 'status': r2.status_code,
                        })
                        p_google_sus(f"Deep suspicious path: {path} ({r2.status_code})")
                except Exception:
                    pass
            score += deep_score
            result['copy_score'] = score
            result['is_copy'] = score >= 3
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"GOOGLE SUSPICIOUS SERVER DETECTED! Score: {result['copy_score']}")
                self._instant_google_suspicious_clean(result)
            else:
                p_ok(f"No Google suspicious server (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Google suspicious detection failed: {e}")
        return result

    def _instant_google_suspicious_clean(self, result):
        before = self.bot.cleaner_stats['total_cleaned']
        self.run_google_suspicious_cleaner()
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['google_suspicious_system_cleaned'] += 1

    def run_google_suspicious_cleaner(self):
        total = (self.bot.cleaner.clean_group('google_suspicious', GOOGLE_SUSPICIOUS_SERVER_PATHS) +
                 self.bot.cleaner.clean_group('system', CLEANER_SYSTEM_PATHS) +
                 self.bot.cleaner.clean_group('cooldown', COOLDOWN_CLEANER_PATHS) +
                 self.bot.cleaner.clean_group('google_account', GOOGLE_ACCOUNT_CLEANER_PATHS) +
                 self.bot.cleaner.clean_group('all_cookies', CLEANER_ALL_COOKIES_PATHS) +
                 self.bot.cleaner.clean_group('apikey', APIKEY_CLEANER_PATHS))
        total += self._clean_google_suspicious_tokens()
        total += self._destroy_suspicious_server_paths()
        self.bot.cleaner_stats['total_cleaned'] += total
        self.bot.cleaner_stats['google_suspicious_cleaned'] += total
        p_ok(f"Google Suspicious cleaner: {total} items")
        return total

    def _clean_google_suspicious_tokens(self):
        cleaned = 0
        for path in ['/suspicious/tokens', '/suspicious/keys',
                     '/accounts/suspicious/tokens', '/myaccount/suspicious/tokens',
                     '/security/alert/tokens', '/server/suspicious/tokens',
                     '/system/suspicious/tokens', '/api/suspicious/tokens']:
            try:
                url = self.bot.base_url + path
                r = self.bot._request('GET', url, timeout=3, allow_redirects=False)
                if r.status_code in (200, 201, 202, 204, 301, 302, 403):
                    try:
                        self.bot.session.delete(url, timeout=3, verify=False)
                    except Exception:
                        pass
                    cleaned += 1
                    self.bot.cleaner_stats['tokens_cleaned'] += 1
                    self.bot.cleaner_stats['okay_signals'] += 1
                    p_okay(f"OKAY - SUSPICIOUS TOKEN DESTROYED: {path}")
            except Exception:
                pass
        return cleaned

    def _destroy_suspicious_server_paths(self):
        destroyed = 0
        for path in ['/server/anomaly', '/server/unusual', '/server/alert',
                     '/system/anomaly', '/system/unusual', '/system/alert',
                     '/api/anomaly', '/api/unusual', '/api/alert',
                     '/backend/suspicious', '/backend/compromised',
                     '/upstream/suspicious', '/upstream/error',
                     '/internal/suspicious', '/internal/error']:
            try:
                url = self.bot.base_url + path
                r = self.bot._request('GET', url, timeout=3, allow_redirects=False)
                if r.status_code in (200, 201, 202, 204, 301, 302, 403):
                    try:
                        self.bot.session.delete(url, timeout=3, verify=False)
                    except Exception:
                        pass
                    destroyed += 1
                    self.bot.cleaner_stats['okay_signals'] += 1
                    p_okay(f"OKAY - SUSPICIOUS SERVER PATH DESTROYED: {path}")
            except Exception:
                pass
        return destroyed

    def universal_google_suspicious_clean(self):
        p_google_sus("=== GOOGLE SUSPICIOUS CLEAN ===")
        result = self.detect_google_suspicious_server()
        if result['is_copy']:
            p_google_sus(f"✅ Cleaned: {result['destroy_count']} items")
        return result
