#!/usr/bin/env python3
"""apex_url_mode.py - Dedicated --url mode handler"""
from urllib.parse import urlparse
from apex_utils import p_urlm, p_ok, p_info, p_err, p_crawl
import time


class URLModeHandler:
    """Dedicated handler for --url mode.
    Target: direct URL. Behavior: comprehensive site-wide scan.
    """

    def __init__(self, bot):
        self.bot = bot

    def run(self, args):
        p_urlm(f"Target URL : {self.bot.target}")
        p_urlm(f"Base URL   : {self.bot.base_url}")
        p_urlm(f"Host       : {self.bot.hostname}")
        p_urlm(f"IP         : {self.bot.ip}")
        p_urlm(f"Port       : {self.bot.port}")

        # Full site-wide processing
        self.process_once()

        # If --ultimate / --full / --autonomous not set, still run these:
        if not (args.ultimate or args.full or args.autonomous):
            self.bot.universal_copyright_clean()
            self.bot.run_clean_pipeline()
        return True

    def process_once(self):
        """One pass of URL-mode work."""
        result = self.bot.url_mode_results
        result['pages_crawled'] = []
        result['assets_found'] = []
        result['forms_found'] = []

        # Site-wide crawl
        try:
            pages = self.bot.recon.crawler_spider(max_pages=30) or []
            result['pages_crawled'] = [p['url'] for p in pages]
            p_ok(f"URL mode crawled: {len(result['pages_crawled'])} pages")
        except Exception as e:
            p_err(f"URL mode crawl failed: {e}")

        # Asset extraction from homepage
        try:
            r = self.bot._request('GET', self.bot.base_url)
            assets = self._extract_assets(r.text)
            result['assets_found'] = assets
            p_ok(f"URL mode assets: {len(assets)}")
        except Exception as e:
            p_err(f"URL mode asset extract failed: {e}")

        # Form analysis
        try:
            r = self.bot._request('GET', self.bot.base_url)
            forms = self._extract_forms(r.text)
            result['forms_found'] = forms
            p_ok(f"URL mode forms: {len(forms)}")
        except Exception as e:
            p_err(f"URL mode form analysis failed: {e}")

        return result

    @staticmethod
    def _extract_assets(html):
        import re
        from urllib.parse import urlparse
        assets = []
        for m in re.finditer(r'(?:src|href)=["\']([^"\']+\.(?:js|css|png|jpg|jpeg|gif|svg|woff2?|ico))', html, re.I):
            assets.append(m.group(1))
        return list(set(assets))

    @staticmethod
    def _extract_forms(html):
        import re
        forms = []
        for m in re.finditer(r'<form[^>]*action=["\']([^"\']*)["\'][^>]*>', html, re.I):
            forms.append(m.group(1))
        return list(set(forms))
