#!/usr/bin/env python3
"""apex_link_mode.py - Dedicated --link mode handler (recursive link follow + asset extract)"""
from urllib.parse import urlparse, urljoin
from apex_utils import p_link, p_ok, p_err, p_info
import re


class LinkModeHandler:
    """Dedicated handler for --link mode.
    Target: specific link/endpoint (e.g. robots.txt, sitemap.xml, API endpoint).
    Behavior: fetch target, follow links from it recursively (max depth), extract assets.
    """

    MAX_FOLLOW = 50

    def __init__(self, bot):
        self.bot = bot

    def run(self, args):
        p_link(f"Target link : {self.bot.target}")
        p_link(f"Base URL    : {self.bot.base_url}")
        p_link(f"Link path   : {urlparse(self.bot.target).path or '/'}")

        self.process_once()

        if not (args.ultimate or args.full or args.autonomous):
            self.bot.universal_copyright_clean()
            self.bot.run_clean_pipeline()
        return True

    def process_once(self):
        """One pass of link-mode work."""
        result = self.bot.link_mode_results
        result['links_followed'] = []
        result['assets_extracted'] = []
        result['endpoints_found'] = []

        # Fetch the target link
        try:
            r = self.bot._request('GET', self.bot.target)
        except Exception as e:
            p_err(f"Link mode fetch failed: {e}")
            return result

        p_ok(f"Link mode fetched: {self.bot.target} (status={r.status_code})")

        # Parse links from the target (URLs, paths, endpoints)
        body = r.text
        target_host = urlparse(self.bot.target).netloc
        found_links = set()

        # Absolute URLs
        for m in re.finditer(r'https?://[^\s"\'<>]+', body):
            found_links.add(m.group(0))

        # Relative paths
        for m in re.finditer(r'(?:href|action|src)=["\'](/[^"\']+)["\']', body, re.I):
            found_links.add(m.group(1))

        # API endpoints
        for m in re.finditer(r'["\'](/(?:api|v\d|graphql|rest)/[^"\']*)["\']', body, re.I):
            result['endpoints_found'].append(m.group(1))

        # Follow links from same host (max N)
        followed = 0
        for link in found_links:
            if followed >= self.MAX_FOLLOW:
                break
            full = urljoin(self.bot.target, link)
            host = urlparse(full).netloc
            if host != target_host:
                continue
            try:
                r2 = self.bot._request('GET', full, timeout=3)
                if r2.status_code in (200, 301, 302):
                    result['links_followed'].append({
                        'url': full, 'status': r2.status_code,
                    })
                    followed += 1
                    p_link(f"Followed: {full} ({r2.status_code})")
            except Exception:
                pass

        # Extract assets from target
        result['assets_extracted'] = self._extract_assets(body)
        p_ok(f"Link mode: followed={len(result['links_followed'])} "
             f"assets={len(result['assets_extracted'])} "
             f"endpoints={len(result['endpoints_found'])}")
        return result

    @staticmethod
    def _extract_assets(html):
        assets = []
        for m in re.finditer(r'(?:src|href|url)["\'(]?\s*([^"\')\s]+\.(?:js|css|png|jpg|jpeg|gif|svg|woff2?|ico|json|xml|txt))', html, re.I):
            assets.append(m.group(1))
        return list(set(assets))
