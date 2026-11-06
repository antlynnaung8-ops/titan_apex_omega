#!/usr/bin/env python3
"""apex_copyright.py - 18 copyright detectors"""
from apex_utils import (
    p_copy, p_crit, p_ok, p_err, p_movie, p_video, p_stream,
    p_image, p_series, p_lang, p_sys, p_gws, p_esf, p_apikey, p_cooldown, p_aegis,
)
from apex_config import (
    COPYRIGHT_KNOWN_SITES, COPYRIGHT_META_SIGNATURES, COPYRIGHT_DEFAULT_TITLES,
    MOVIE_COPYRIGHT_SIGNATURES, MOVIE_TITLE_KEYWORDS,
    VIDEO_FILE_EXTENSIONS, STREAMING_PLAYER_SIGNATURES, STREAMING_PROTOCOLS,
    SERIES_COPYRIGHT_SIGNATURES, SERIES_TITLE_KEYWORDS, SERIES_CLEANER_PATHS,
    IMAGE_COPYRIGHT_SIGNATURES, IMAGE_KEYWORDS,
    PROGRAMMING_LANGUAGE_SIGNATURES, WEB_SERVER_SYSTEM_SIGNATURES,
    GWS_CLEANER_PATHS, ESF_CLEANER_PATHS,
    API_KEY_COPYRIGHT_SIGNATURES, APIKEY_CLEANER_PATHS,
    COOLDOWN_SYSTEM_SIGNATURES, COOLDOWN_CLEANER_PATHS,
    FRAMEWORK_COPY_SIGNATURES,
    CLEANER_HTTP_PATHS, CLEANER_HTTPS_PATHS, CLEANER_ANOTHER_PATHS,
    CLEANER_COOKIES_DATA_PATHS, CLEANER_ALL_COOKIES_PATHS,
    CLEANER_COMPLETE_DATA_PATHS, CLEANER_MOVIE_PATHS, CLEANER_VIDEO_PATHS,
    CLEANER_STREAMING_PATHS, CLEANER_IMAGE_PATHS, CLEANER_LANGUAGE_PATHS,
    CLEANER_SYSTEM_PATHS,
)
import datetime
import re

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


class CopyrightDetectors:
    def __init__(self, bot):
        self.bot = bot

    # ---------- WEB ----------
    def detect_web_copy(self):
        result = self.bot.copy_results
        url = self.bot.target if self.bot.mode == 'link' else (
            self.bot.target + 'test' if self.bot.mode == 'search' else self.bot.base_url)
        print("\n=== WEB COPYRIGHT DETECTION ===")
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            body = r.text.lower()
            score = 0
            for sig, name in COPYRIGHT_KNOWN_SITES.items():
                if sig.lower() in body:
                    result['matched_signatures'].append({'signature': sig, 'match': name})
                    score += 2
                    p_copy(f"Signature: {sig} → {name}")
            for meta in COPYRIGHT_META_SIGNATURES:
                if meta.lower() in body:
                    result['matched_meta'].append(meta)
                    score += 3
                    p_copy(f"Meta: {meta}")
            if BS4_AVAILABLE:
                try:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    if soup.title and soup.title.string:
                        t = soup.title.string.strip().lower()
                        result['title'] = soup.title.string.strip()[:120]
                        if t in COPYRIGHT_DEFAULT_TITLES:
                            score += 5
                            p_copy(f"Default title: {result['title']}")
                except Exception:
                    pass
            result['copy_score'] = score
            result['is_copy'] = score >= 3
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"WEB COPYRIGHT DETECTED! Score: {result['copy_score']}")
                self._instant_web_clean(result)
            else:
                p_ok(f"No web copyright (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Web copyright detection failed: {e}")
        return result

    def _instant_web_clean(self, result):
        before = self.bot.cleaner_stats['total_cleaned']
        total = (self.bot.cleaner.clean_group('http', CLEANER_HTTP_PATHS) +
                 self.bot.cleaner.clean_group('https', CLEANER_HTTPS_PATHS) +
                 self.bot.cleaner.clean_group('another', CLEANER_ANOTHER_PATHS) +
                 self.bot.cleaner.clean_group('cookies_data', CLEANER_COOKIES_DATA_PATHS) +
                 self.bot.cleaner.clean_group('all_cookies', CLEANER_ALL_COOKIES_PATHS) +
                 self.bot.cleaner.clean_group('complete_data', CLEANER_COMPLETE_DATA_PATHS))
        self.bot.cleaner_stats['total_cleaned'] += total
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['copyright_instant_cleaned'] += 1

    # ---------- MOVIE ----------
    def detect_movie_copy(self):
        result = self.bot.movie_copy_results
        url = self.bot.target if self.bot.mode == 'link' else (
            self.bot.target + 'movie' if self.bot.mode == 'search' else self.bot.base_url)
        print("\n=== MOVIE COPYRIGHT DETECTION ===")
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            body = r.text.lower()
            score = 0
            for sig, name in MOVIE_COPYRIGHT_SIGNATURES.items():
                if sig.lower() in body:
                    result['matched_movie'].append({'signature': sig, 'match': name})
                    score += 2
                    p_movie(f"Movie: {sig} → {name}")
            for kw in MOVIE_TITLE_KEYWORDS:
                if kw in body:
                    result['matched_titles'].append(kw)
                    score += 3
                    p_movie(f"Keyword: {kw}")
            for sig, name in STREAMING_PLAYER_SIGNATURES.items():
                if sig in body:
                    result['matched_players'].append({'signature': sig, 'name': name})
                    score += 2
                    p_movie(f"Player: {name}")
            result['copy_score'] = score
            result['is_copy'] = score >= 5
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"MOVIE COPYRIGHT DETECTED! Score: {result['copy_score']}")
                self._instant_movie_clean(result)
            else:
                p_ok(f"No movie copyright (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Movie detection failed: {e}")
        return result

    def _instant_movie_clean(self, result):
        before = self.bot.cleaner_stats['total_cleaned']
        total = (self.bot.cleaner.clean_group('movie', CLEANER_MOVIE_PATHS) +
                 self.bot.cleaner.clean_group('streaming', CLEANER_STREAMING_PATHS))
        self.bot.cleaner_stats['total_cleaned'] += total
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['copyright_instant_cleaned'] += 1

    # ---------- SERIES ----------
    def detect_series_copy(self):
        result = self.bot.series_copy_results
        url = self.bot.target if self.bot.mode == 'link' else (
            self.bot.target + 'series' if self.bot.mode == 'search' else self.bot.base_url)
        print("\n=== SERIES COPYRIGHT DETECTION ===")
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            body = r.text.lower()
            score = 0
            for sig, name in SERIES_COPYRIGHT_SIGNATURES.items():
                if sig.lower() in body:
                    result['matched_series'].append({'signature': sig, 'match': name})
                    score += 3
                    p_series(f"Series: {sig} → {name}")
            for kw in SERIES_TITLE_KEYWORDS:
                if kw in body:
                    result['matched_titles'].append(kw)
                    score += 3
                    p_series(f"Keyword: {kw}")
            result['copy_score'] = score
            result['is_copy'] = score >= 6
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"SERIES COPYRIGHT DETECTED! Score: {result['copy_score']}")
                self._instant_series_clean(result)
            else:
                p_ok(f"No series copyright (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Series detection failed: {e}")
        return result

    def _instant_series_clean(self, result):
        before = self.bot.cleaner_stats['total_cleaned']
        total = (self.bot.cleaner.clean_group('series', SERIES_CLEANER_PATHS) +
                 self.bot.cleaner.clean_group('streaming', CLEANER_STREAMING_PATHS))
        self.bot.cleaner_stats['total_cleaned'] += total
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['copyright_instant_cleaned'] += 1

    # ---------- VIDEO ----------
    def detect_video_copy(self):
        result = self.bot.video_copy_results
        url = self.bot.target if self.bot.mode == 'link' else (
            self.bot.target + 'video' if self.bot.mode == 'search' else self.bot.base_url)
        print("\n=== VIDEO COPYRIGHT DETECTION ===")
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            body = r.text.lower()
            score = 0
            for ext in VIDEO_FILE_EXTENSIONS:
                if ext in body:
                    result['matched_extensions'].append(ext)
                    score += 1
                    p_video(f"Video ext: {ext}")
            for sig, name in STREAMING_PLAYER_SIGNATURES.items():
                if sig in body:
                    result['matched_players'].append({'signature': sig, 'name': name})
                    score += 2
                    p_video(f"Player: {name}")
            result['copy_score'] = score
            result['is_copy'] = score >= 3
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"VIDEO COPYRIGHT DETECTED! Score: {result['copy_score']}")
                self._instant_video_clean(result)
            else:
                p_ok(f"No video copyright (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Video detection failed: {e}")
        return result

    def _instant_video_clean(self, result):
        before = self.bot.cleaner_stats['total_cleaned']
        total = (self.bot.cleaner.clean_group('video', CLEANER_VIDEO_PATHS) +
                 self.bot.cleaner.clean_group('streaming', CLEANER_STREAMING_PATHS))
        self.bot.cleaner_stats['total_cleaned'] += total
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['copyright_instant_cleaned'] += 1

    # ---------- STREAMING ----------
    def detect_streaming_copy(self):
        result = self.bot.stream_copy_results
        url = self.bot.target if self.bot.mode == 'link' else (
            self.bot.target + 'stream' if self.bot.mode == 'search' else self.bot.base_url)
        print("\n=== STREAMING COPYRIGHT DETECTION ===")
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            body = r.text.lower()
            score = 0
            for proto in STREAMING_PROTOCOLS:
                if proto in body:
                    result['matched_protocols'].append(proto)
                    score += 3
                    p_stream(f"Protocol: {proto}")
            for sig, name in STREAMING_PLAYER_SIGNATURES.items():
                if sig in body:
                    result['matched_players'].append({'signature': sig, 'name': name})
                    score += 2
                    p_stream(f"Player: {name}")
            result['copy_score'] = score
            result['is_copy'] = score >= 5
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"STREAMING COPYRIGHT DETECTED! Score: {result['copy_score']}")
                self._instant_streaming_clean(result)
            else:
                p_ok(f"No streaming copyright (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Streaming detection failed: {e}")
        return result

    def _instant_streaming_clean(self, result):
        before = self.bot.cleaner_stats['total_cleaned']
        total = (self.bot.cleaner.clean_group('streaming', CLEANER_STREAMING_PATHS) +
                 self.bot.cleaner.clean_group('movie', CLEANER_MOVIE_PATHS) +
                 self.bot.cleaner.clean_group('video', CLEANER_VIDEO_PATHS))
        self.bot.cleaner_stats['total_cleaned'] += total
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['copyright_instant_cleaned'] += 1

    # ---------- IMAGE ----------
    def detect_image_copy(self):
        result = self.bot.image_copy_results
        url = self.bot.target if self.bot.mode == 'link' else (
            self.bot.target + 'image' if self.bot.mode == 'search' else self.bot.base_url)
        print("\n=== IMAGE COPYRIGHT DETECTION ===")
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            body = r.text.lower()
            score = 0
            for sig, name in IMAGE_COPYRIGHT_SIGNATURES.items():
                if sig.lower() in body:
                    result['matched_image'].append({'signature': sig, 'match': name})
                    score += 2
                    p_image(f"Image: {sig} → {name}")
            for kw in IMAGE_KEYWORDS:
                if kw in body:
                    result['matched_keywords'].append(kw)
                    score += 3
                    p_image(f"Keyword: {kw}")
            result['copy_score'] = score
            result['is_copy'] = score >= 5
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"IMAGE COPYRIGHT DETECTED! Score: {result['copy_score']}")
                self._instant_image_clean(result)
            else:
                p_ok(f"No image copyright (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Image detection failed: {e}")
        return result

    def _instant_image_clean(self, result):
        before = self.bot.cleaner_stats['total_cleaned']
        total = self.bot.cleaner.clean_group('image', CLEANER_IMAGE_PATHS)
        self.bot.cleaner_stats['total_cleaned'] += total
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['copyright_instant_cleaned'] += 1

    # ---------- LANGUAGE ----------
    def detect_language_copy(self):
        result = self.bot.lang_copy_results
        url = self.bot.target if self.bot.mode == 'link' else (
            self.bot.target + 'php' if self.bot.mode == 'search' else self.bot.base_url)
        print("\n=== LANGUAGE COPY DETECTION ===")
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            body = r.text.lower()
            headers_lower = {k.lower(): v.lower() for k, v in r.headers.items()}
            score = 0
            for lang, sigs in PROGRAMMING_LANGUAGE_SIGNATURES.items():
                for sig in sigs['headers']:
                    if any(sig in f"{k}: {v}" for k, v in headers_lower.items()):
                        result['matched_languages'].append({'language': lang, 'signature': sig})
                        score += 3
                        p_lang(f"Language: {lang} → {sig}")
                        break
                for sig in sigs['body']:
                    if sig.lower() in body:
                        result['matched_languages'].append({'language': lang, 'signature': sig})
                        score += 2
                        p_lang(f"Language: {lang} → {sig}")
                        break
            for fw, sigs in FRAMEWORK_COPY_SIGNATURES.items():
                for sig in sigs:
                    if sig.lower() in body:
                        result['matched_frameworks'].append({'framework': fw, 'signature': sig})
                        score += 2
                        p_lang(f"Framework: {fw} → {sig}")
                        break
            result['copy_score'] = score
            result['is_copy'] = score >= 5
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"LANGUAGE COPY DETECTED! Score: {result['copy_score']}")
                self._instant_language_clean(result)
            else:
                p_ok(f"No language copy (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Language copy detection failed: {e}")
        return result

    def _instant_language_clean(self, result):
        before = self.bot.cleaner_stats['total_cleaned']
        total = self.bot.cleaner.clean_group('language', CLEANER_LANGUAGE_PATHS)
        self.bot.cleaner_stats['total_cleaned'] += total
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['web_system_cleaned'] += 1

    # ---------- SYSTEM ----------
    def detect_system_copy(self):
        result = self.bot.system_copy_results
        url = self.bot.target if self.bot.mode == 'link' else (
            self.bot.target + 'server' if self.bot.mode == 'search' else self.bot.base_url)
        print("\n=== SYSTEM COPY DETECTION ===")
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            body = r.text.lower()
            headers_lower = {k.lower(): v.lower() for k, v in r.headers.items()}
            score = 0
            for sys_name, sigs in WEB_SERVER_SYSTEM_SIGNATURES.items():
                for sig in sigs['headers']:
                    if any(sig in f"{k}: {v}" for k, v in headers_lower.items()):
                        result['matched_systems'].append({'system': sys_name, 'signature': sig})
                        score += 3
                        p_sys(f"System: {sys_name} → {sig}")
                        break
                for sig in sigs['body']:
                    if sig.lower() in body:
                        result['matched_systems'].append({'system': sys_name, 'signature': sig})
                        score += 2
                        p_sys(f"System: {sys_name} → {sig}")
                        break
            result['copy_score'] = score
            result['is_copy'] = score >= 5
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"SYSTEM COPY DETECTED! Score: {result['copy_score']}")
                self._instant_system_clean(result)
            else:
                p_ok(f"No system copy (score={result['copy_score']})")
        except Exception as e:
            p_err(f"System copy detection failed: {e}")
        return result

    def _instant_system_clean(self, result):
        before = self.bot.cleaner_stats['total_cleaned']
        total = self.bot.cleaner.clean_group('system', CLEANER_SYSTEM_PATHS)
        self.bot.cleaner_stats['total_cleaned'] += total
        result['destroyed'] = True
        result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
        self.bot.cleaner_stats['web_system_cleaned'] += 1

    # ---------- GWS / ESF ----------
    def detect_gws_copy(self):
        result = self.bot.gws_copy_results
        print("\n=== GWS COPY DETECTION ===")
        try:
            r = self.bot._request('GET', self.bot.base_url, allow_redirects=True)
            body = r.text.lower()
            headers_lower = {k.lower(): v.lower() for k, v in r.headers.items()}
            score = 0
            for sig in ['server: gws', 'server: google web server', 'x-gws-']:
                if any(sig in f"{k}: {v}" for k, v in headers_lower.items()):
                    result['matched_gws'].append({'signature': sig})
                    score += 3
                    p_gws(f"GWS: {sig}")
                    break
            for sig in ['/gws/', '/gws/data/', 'gws-config', 'gws-cache']:
                if sig.lower() in body:
                    result['matched_gws'].append({'signature': sig})
                    score += 2
                    p_gws(f"GWS: {sig}")
            result['copy_score'] = score
            result['is_copy'] = score >= 5
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"GWS COPY DETECTED! Score: {result['copy_score']}")
                before = self.bot.cleaner_stats['total_cleaned']
                total = self.bot.cleaner.clean_group('gws', GWS_CLEANER_PATHS)
                self.bot.cleaner_stats['total_cleaned'] += total
                result['destroyed'] = True
                result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
                self.bot.cleaner_stats['gws_system_cleaned'] += 1
            else:
                p_ok(f"No GWS copy (score={result['copy_score']})")
        except Exception as e:
            p_err(f"GWS detection failed: {e}")
        return result

    def detect_esf_copy(self):
        result = self.bot.esf_copy_results
        print("\n=== ESF COPY DETECTION ===")
        try:
            r = self.bot._request('GET', self.bot.base_url, allow_redirects=True)
            body = r.text.lower()
            headers_lower = {k.lower(): v.lower() for k, v in r.headers.items()}
            score = 0
            for sig in ['server: esf', 'server: enterprise service fabric', 'x-esf-']:
                if any(sig in f"{k}: {v}" for k, v in headers_lower.items()):
                    result['matched_esf'].append({'signature': sig})
                    score += 3
                    p_esf(f"ESF: {sig}")
                    break
            for sig in ['/esf/', '/esf/data/', 'esf-config', 'esf-cache']:
                if sig.lower() in body:
                    result['matched_esf'].append({'signature': sig})
                    score += 2
                    p_esf(f"ESF: {sig}")
            result['copy_score'] = score
            result['is_copy'] = score >= 5
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"ESF COPY DETECTED! Score: {result['copy_score']}")
                before = self.bot.cleaner_stats['total_cleaned']
                total = self.bot.cleaner.clean_group('esf', ESF_CLEANER_PATHS)
                self.bot.cleaner_stats['total_cleaned'] += total
                result['destroyed'] = True
                result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
                self.bot.cleaner_stats['esf_system_cleaned'] += 1
            else:
                p_ok(f"No ESF copy (score={result['copy_score']})")
        except Exception as e:
            p_err(f"ESF detection failed: {e}")
        return result

    # ---------- APIKEY ----------
    def detect_apikey_copy(self):
        result = self.bot.apikey_copy_results
        url = self.bot.target if self.bot.mode == 'link' else (
            self.bot.target + 'api' if self.bot.mode == 'search' else self.bot.base_url)
        print("\n=== APIKEY COPYRIGHT DETECTION ===")
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            score = 0
            for key_type, sigs in API_KEY_COPYRIGHT_SIGNATURES.items():
                if sigs.get('regex'):
                    matches = re.findall(sigs['regex'], r.text, re.IGNORECASE)
                    if matches:
                        result['matched_types'].append({'type': key_type, 'count': len(matches)})
                        score += 5
                        p_apikey(f"API Key: {key_type} → {len(matches)} found")
            result['copy_score'] = score
            result['is_copy'] = score >= 3
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"APIKEY COPYRIGHT DETECTED! Score: {result['copy_score']}")
                before = self.bot.cleaner_stats['total_cleaned']
                total = self.bot.cleaner.clean_group('apikey', APIKEY_CLEANER_PATHS)
                self.bot.cleaner_stats['total_cleaned'] += total
                result['destroyed'] = True
                result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
                self.bot.cleaner_stats['apikey_system_cleaned'] += 1
            else:
                p_ok(f"No apikey copyright (score={result['copy_score']})")
        except Exception as e:
            p_err(f"APIKey detection failed: {e}")
        return result

    # ---------- COOLDOWN ----------
    def detect_cooldown_copy(self):
        result = self.bot.cooldown_copy_results
        url = self.bot.target if self.bot.mode == 'link' else (
            self.bot.target + 'cooldown' if self.bot.mode == 'search' else self.bot.base_url)
        print("\n=== COOLDOWN COPY DETECTION ===")
        try:
            r = self.bot._request('GET', url, allow_redirects=True)
            body = r.text.lower()
            headers_lower = {k.lower(): v.lower() for k, v in r.headers.items()}
            score = 0
            for cd_name, sigs in COOLDOWN_SYSTEM_SIGNATURES.items():
                for sig in sigs['headers']:
                    if sig in headers_lower:
                        result['matched_cooldown'].append({'cooldown': cd_name, 'signature': sig})
                        score += 3
                        p_cooldown(f"Cooldown: {cd_name} → {sig}")
                        break
                for sig in sigs['body']:
                    if sig.lower() in body:
                        result['matched_cooldown'].append({'cooldown': cd_name, 'signature': sig})
                        score += 2
                        break
                if r.status_code in sigs.get('status_codes', []):
                    result['matched_status_codes'].append(r.status_code)
                    score += 2
            result['copy_score'] = score
            result['is_copy'] = score >= 3
            result['detected_at'] = datetime.datetime.now().isoformat()
            if result['is_copy']:
                p_crit(f"COOLDOWN COPY DETECTED! Score: {result['copy_score']}")
                before = self.bot.cleaner_stats['total_cleaned']
                total = self.bot.cleaner.clean_group('cooldown', COOLDOWN_CLEANER_PATHS)
                self.bot.cleaner_stats['total_cleaned'] += total
                result['destroyed'] = True
                result['destroy_count'] = self.bot.cleaner_stats['total_cleaned'] - before
                self.bot.cleaner_stats['cooldown_system_cleaned'] += 1
            else:
                p_ok(f"No cooldown copyright (score={result['copy_score']})")
        except Exception as e:
            p_err(f"Cooldown detection failed: {e}")
        return result
