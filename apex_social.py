#!/usr/bin/env python3
"""apex_social.py - 8 Social Platform Suspicious Cleaners"""
import datetime
from apex_utils import (
    p_social_sus, p_telegram, p_tiktok, p_discord, p_pinterest,
    p_whatsapp, p_facebook, p_instagram, p_twitter, p_crit, p_ok, p_okay, p_err,
)
from apex_config import (
    SOCIAL_PLATFORM_SIGNATURES, SOCIAL_CLEANER_PATHS,
    CLEANER_SYSTEM_PATHS, COOLDOWN_CLEANER_PATHS,
    CLEANER_ALL_COOKIES_PATHS, APIKEY_CLEANER_PATHS,
)


class SocialSuspiciousCleaner:
    PLATFORMS = ['Telegram', 'TikTok', 'Discord', 'Pinterest',
                 'WhatsApp', 'Facebook', 'Instagram', 'Twitter']

    LOGGERS = {
        'Telegram': p_telegram, 'TikTok': p_tiktok,
        'Discord': p_discord, 'Pinterest': p_pinterest,
        'WhatsApp': p_whatsapp, 'Facebook': p_facebook,
        'Instagram': p_instagram, 'Twitter': p_twitter,
    }

    def __init__(self, bot):
        self.bot = bot

    def _result_for(self, platform):
        return {
            'Telegram': self.bot.telegram_suspicious_results,
            'TikTok': self.bot.tiktok_suspicious_results,
            'Discord': self.bot.discord_suspicious_results,
            'Pinterest': self.bot.pinterest_suspicious_results,
            'WhatsApp': self.bot.whatsapp_suspicious_results,
            'Facebook': self.bot.facebook_suspicious_results,
            'Instagram': self.bot.instagram_suspicious_results,
            'Twitter': self.bot.twitter_suspicious_results,
        }[platform]

    def _analyze(self, platform, body_raw, headers, status_code, result, weight=1):
        body = body_raw.lower()
        headers_lower = {k.lower(): v.lower() for k, v in headers.items()}
        headers_combined = "\n".join(f"{k}: {v}" for k, v in headers_lower.items())
        logger = self.LOGGERS[platform]
        score = 0
        for sig in ['x-suspicious-', 'x-suspect-', 'x-anomaly-',
                    'x-compromised-', 'x-breach-', 'x-attack-',
                    'x-intrusion-', 'x-alert-', 'x-warning-']:
            if sig in headers_combined:
                if not any(m['signature'] == sig for m in result['matched_headers']):
                    result['matched_headers'].append({
                        'signature': sig, 'platform': platform, 'source': 'header',
                    })
                    score += 4 * weight
                    logger(f"[{platform}] Suspicious Header: {sig}")
        sigs = SOCIAL_PLATFORM_SIGNATURES.get(platform, {})
        for sig in sigs.get('suspicious_body', []):
            if sig.lower() in body:
                if not any(m['signature'] == sig for m in result['matched_bodies']):
                    result['matched_bodies'].append({
                        'signature': sig, 'platform': platform, 'source': 'body',
                    })
                    score += 3 * weight
                    logger(f"[{platform}] Suspicious Body: {sig}")
        for code in (403, 429, 500, 502, 503, 504):
            if status_code == code:
                if code not in result['matched_status_codes']:
                    result['matched_status_codes'].append(code)
                    score += 2 * weight
                    logger(f"[{platform}] Suspicious Status: {code}")
        return score

    def detect_social_suspicious_server(self, platform):
        result = self._result_for(platform)
        logger = self.LOGGERS[platform]
        print(f"\n=== {platform.upper()} SUSPICIOUS SERVER DETECTION ===")
        url = self.bot.target if self.bot.mode == 'link' else self.bot.base_url
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            score = self._analyze(platform, r.text, r.headers, r.status_code, result, weight=1)
            deep_score = 0
            for path in SOCIAL_CLEANER_PATHS.get(platform.lower(), []):
                try:
                    r2 = self.bot._request('GET', self.bot.base_url + path,
                                           timeout=3, allow_redirects=False)
                    if r2.status_code in (200, 201, 202, 204, 403, 429, 500, 502, 503, 504):
                        deep_score += 2
                        result['matched_types'].append({
                            'type': 'Deep-Path', 'path': path,
                            'status': r2.status_code, 'platform': platform,
                        })
                        logger(f"Deep suspicious path: {path} ({r2.status_code})")
                except Exception:
                    pass
            score += deep_score
            result['copy_score'] = score
            result['is_copy'] = score >= 3
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"{platform.upper()} SUSPICIOUS SERVER DETECTED! Score: {result['copy_score']}")
                self._instant_clean(platform, result)
            else:
                p_ok(f"No {platform} suspicious server (score={result['copy_score']})")
        except Exception as e:
            p_err(f"{platform} suspicious detection failed: {e}")
        return result

    def _instant_clean(self, platform, result):
        before = self.bot.cleaner_stats['total_cleaned']
        self.run_social_suspicious_cleaner(platform)
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['social_suspicious_system_cleaned'] += 1

    def run_social_suspicious_cleaner(self, platform):
        key = platform.lower()
        total = (self.bot.cleaner.clean_group(key, SOCIAL_CLEANER_PATHS.get(key, [])) +
                 self.bot.cleaner.clean_group('system', CLEANER_SYSTEM_PATHS) +
                 self.bot.cleaner.clean_group('cooldown', COOLDOWN_CLEANER_PATHS) +
                 self.bot.cleaner.clean_group('all_cookies', CLEANER_ALL_COOKIES_PATHS) +
                 self.bot.cleaner.clean_group('apikey', APIKEY_CLEANER_PATHS))
        total += self._clean_social_tokens(key)
        total += self._destroy_social_suspicious_paths(platform)
        stat_key = f'{key}_cleaned'
        if stat_key in self.bot.cleaner_stats:
            self.bot.cleaner_stats[stat_key] += total
        self.bot.cleaner_stats['total_cleaned'] += total
        p_ok(f"{platform} Suspicious cleaner: {total} items")
        return total

    def _clean_social_tokens(self, key):
        cleaned = 0
        token_paths = {
            'telegram': ['/telegram/tokens', '/telegram/keys', '/t.me/tokens',
                         '/telegram.dog/tokens', '/telegram/session'],
            'tiktok': ['/tiktok/tokens', '/tiktok/keys', '/vm.tiktok.com/tokens',
                       '/tiktok/session', '/tiktok/sessionid'],
            'discord': ['/discord/tokens', '/discord/keys', '/dgg.gg/tokens',
                        '/discord.gg/tokens', '/discord/session'],
            'pinterest': ['/pinterest/tokens', '/pinterest/keys', '/pin.it/tokens',
                          '/pinterest/session'],
            'whatsapp': ['/whatsapp/tokens', '/whatsapp/keys', '/wa.me/tokens'],
            'facebook': ['/facebook/tokens', '/facebook/keys', '/fb.com/tokens'],
            'instagram': ['/instagram/tokens', '/instagram/keys'],
            'twitter': ['/twitter/tokens', '/twitter/keys', '/x.com/tokens'],
        }
        for path in token_paths.get(key, []):
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
                    p_okay(f"OKAY - {key.upper()} TOKEN DESTROYED: {path}")
            except Exception:
                pass
        return cleaned

    def _destroy_social_suspicious_paths(self, platform):
        destroyed = 0
        key = platform.lower()
        paths = [
            f'/{key}/suspicious', f'/{key}/suspicious-activity',
            f'/{key}/compromised', f'/{key}/breach', f'/{key}/attack',
            f'/{key}/anomaly', f'/{key}/alert', f'/{key}/unusual',
            f'/{key}/security/alert', f'/{key}/security/checkup',
            f'/{key}/account/suspended', f'/{key}/account/banned',
            f'/{key}/session/revoked',
        ]
        for path in paths:
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
                    p_okay(f"OKAY - {platform.upper()} SUSPICIOUS DESTROYED: {path}")
            except Exception:
                pass
        return destroyed

    def universal_social_suspicious_clean(self, platform):
        p_social_sus(f"=== {platform.upper()} SUSPICIOUS CLEAN ===")
        result = self.detect_social_suspicious_server(platform)
        if result['is_copy']:
            p_social_sus(f"✅ {platform} cleaned: {result['destroy_count']} items")
        return result

    def universal_all_social_suspicious_clean(self):
        results = {}
        for platform in self.PLATFORMS:
            try:
                results[platform] = self.universal_social_suspicious_clean(platform)
            except Exception as e:
                p_err(f"{platform} failed: {e}")
        return results
