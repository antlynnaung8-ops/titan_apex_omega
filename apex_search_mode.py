#!/usr/bin/env python3
"""apex_search_mode.py - Dedicated --search mode handler (query parser + multi-page crawl)"""
from urllib.parse import urlparse, urlencode, parse_qs, urljoin, quote
from apex_utils import p_search, p_ok, p_err, p_info
import re


class SearchModeHandler:
    """Dedicated handler for --search mode.
    Target: search URL with query placeholder (e.g. ?q=, ?s=, ?search=).
    Behavior: parse query, fill payloads, extract search results, crawl result pages.
    """

    DEFAULT_QUERIES = [
        'admin', 'login', 'api', 'token', 'config',
        'suspicious', 'compromised', 'backup', 'test', 'dev',
    ]
    MAX_RESULTS = 30

    def __init__(self, bot):
        self.bot = bot
        self.search_url = bot.target
        self.placeholder = self._detect_placeholder(self.search_url)

    @staticmethod
    def _detect_placeholder(url):
        parsed = urlparse(url)
        if not parsed.query:
            return None
        params = parse_qs(parsed.query, keep_blank_values=True)
        for k, v in params.items():
            if v == [''] or v == ['{}'] or '{query}' in v[0]:
                return k
        return None

    def _build_query_url(self, query):
        """Fill the query placeholder with an actual search query."""
        parsed = urlparse(self.search_url)
        params = parse_qs(parsed.query, keep_blank_values=True)
        if self.placeholder:
            params[self.placeholder] = [query]
        else:
            params['q'] = [query]
        new_q = urlencode(params, doseq=True)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_q}"

    def run(self, args):
        p_search(f"Search URL : {self.search_url}")
        p_search(f"Placeholder: {self.placeholder or 'q (fallback)'}")
        p_search(f"Base URL   : {self.bot.base_url}")

        self.process_once()

        if not (args.ultimate or args.full or args.autonomous):
            self.bot.universal_copyright_clean()
            self.bot.run_clean_pipeline()
        return True

    def process_once(self):
        """One pass of search-mode work."""
        result = self.bot.search_mode_results
        result['queries_parsed'] = []
        result['results_extracted'] = []
        result['pages_analyzed'] = []

        queries = self._get_queries_from_args() or self.DEFAULT_QUERIES
        for q in queries:
            url = self._build_query_url(q)
            result['queries_parsed'].append({'query': q, 'url': url})
            p_search(f"Query: {q!r} → {url}")
            try:
                r = self.bot._request('GET', url, timeout=5)
            except Exception as e:
                p_err(f"Search fetch failed for {q!r}: {e}")
                continue

            # Extract result links
            links = self._extract_result_links(r.text, self.bot.hostname)
            for link in links[:self.MAX_RESULTS]:
                result['results_extracted'].append({
                    'query': q, 'result_url': link,
                })
                p_search(f"  Result: {link}")

            # Analyze the search page itself
            result['pages_analyzed'].append({
                'query': q, 'status': r.status_code,
                'length': len(r.text), 'links': len(links),
            })

        p_ok(f"Search mode: queries={len(result['queries_parsed'])} "
             f"results={len(result['results_extracted'])}")
        return result

    def _get_queries_from_args(self):
        raw = getattr(self.bot.args, 'search_queries', None)
        if raw:
            return [q.strip() for q in raw.split(',') if q.strip()]
        return None

    @staticmethod
    def _extract_result_links(html, base_host):
        links = set()
        # Extract href-based links from same host
        for m in re.finditer(r'href=["\'](https?://[^"\']+)["\']', html, re.I):
            link = m.group(1)
            if urlparse(link).netloc == base_host:
                links.add(link)
        # Extract relative links
        for m in re.finditer(r'href=["\'](/[^"\']+)["\']', html, re.I):
            links.add(m.group(1))
        return sorted(links)
