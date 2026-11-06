#!/usr/bin/env python3
"""
TITAN_APEX_OMEGA.PY v17000 - TITAN APEX EDITION
================================================
WEB SERVER ONLY | FULLY AUTONOMOUS | UNSTOPPABLE AI ROBOT

NEW in v17000:
- RENAMED: TITAN_APEX_OMEGA (was TITANGOD_X_OMEGA)
- 3 DEDICATED MODE HANDLERS: --url / --link / --search (fully separate code paths)
- 18 COPYRIGHT TYPES → 18 INSTANT CLEANERS
- 14 AI ROBOTS (was 10)
- 32-STEP CLEANER PIPELINE (was 24)
- 8 SOCIAL PLATFORMS (was 4)
- FREE VPN + PRIVATE VPN + PROTOCOL VPN cleaners
- ADVANCED IP-BYPASS: 12 headers + proxy chain rotation
- DEEP SEARCH: query parser + multi-page crawl + result extraction
- RECURSIVE LINK: link-follow + asset extractor + form analyzer
- GOOGLE SUSPICIOUS SERVER INSTANT CLEANER
- --features flag (full feature matrix)

WARNING: WEB SERVER ONLY - NOT FOR LOCAL COMPUTER!
File: titan_apex_omega.py
Version: 17000.0
"""

import os
import sys
import re
import ssl
import csv
import json
import time
import signal
import socket
import random
import hashlib
import base64
import argparse
import datetime
import ipaddress
import threading
import subprocess
import requests
import urllib3
from urllib.parse import urlparse, urljoin, quote, parse_qs, urlencode, unquote
from collections import deque, OrderedDict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------- Optional deps ----------
try:
    import dns.resolver
    import dns.query
    import dns.zone
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

# ============================================
# META
# ============================================
VERSION = "17000.0"
BUILD_NUMBER = "17000.001"
SCRIPT_NAME = "titan_apex_omega.py"
RELEASE_NAME = ("TITAN APEX OMEGA | WEB SERVER ONLY | 18 COPYRIGHT CLEANERS | "
                "14 AI ROBOTS | 8 SOCIAL CLEANERS | 3 VPN CLEANERS | "
                "GOOGLE SUSPICIOUS | ADVANCED IP-BYPASS")

DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443
TIMEOUT = 5
REQ_HEADERS = {"User-Agent": "Mozilla/5.0 (Titan-Apex-Omega/17000)"}


class C:
    RESET = '\033[0m'
    RED = '\033[91m'; GREEN = '\033[92m'; YELLOW = '\033[93m'; BLUE = '\033[94m'
    MAGENTA = '\033[95m'; CYAN = '\033[96m'; WHITE = '\033[97m'; BOLD = '\033[1m'
    OKGREEN = '\033[92m\033[1m'; OKCYAN = '\033[96m\033[1m'
    COPY = '\033[38;5;201m\033[1m'; CLEAN = '\033[38;5;118m\033[1m'
    AEGIS = '\033[38;5;51m\033[1m'; ROBOT = '\033[38;5;46m\033[1m'
    MOVIE = '\033[38;5;213m\033[1m'; VIDEO = '\033[38;5;214m\033[1m'
    STREAM = '\033[38;5;196m\033[1m'; IMAGE = '\033[38;5;220m\033[1m'
    SERIES = '\033[38;5;129m\033[1m'; CRIGHT = '\033[38;5;199m\033[1m'
    LANG = '\033[38;5;46m\033[1m'; SYS = '\033[38;5;202m\033[1m'
    GWS = '\033[38;5;87m\033[1m'; ESF = '\033[38;5;165m\033[1m'
    APIKEY = '\033[38;5;196m\033[1m'; COOLDOWN = '\033[38;5;208m\033[1m'
    APOLLO = '\033[38;5;220m\033[1m'
    GOOGLE_ACC = '\033[38;5;196m\033[1m'
    GOOGLE_SUS = '\033[38;5;208m\033[1m'
    SOCIAL_SUS = '\033[38;5;213m\033[1m'
    VPN_SUS = '\033[38;5;51m\033[1m'
    TELEGRAM = '\033[38;5;33m\033[1m'
    TIKTOK = '\033[38;5;196m\033[1m'
    DISCORD = '\033[38;5;99m\033[1m'
    PINTEREST = '\033[38;5;196m\033[1m'
    WHATSAPP = '\033[38;5;46m\033[1m'
    FACEBOOK = '\033[38;5;27m\033[1m'
    INSTAGRAM = '\033[38;5;201m\033[1m'
    TWITTER = '\033[38;5;51m\033[1m'
    VPN = '\033[38;5;46m\033[1m'
    ULTIMATE = '\033[38;5;201m\033[1m'
    WALL = '\033[38;5;196m\033[1m'
    FACTORY = '\033[38;5;208m\033[1m'; TOKEN = '\033[38;5;213m\033[1m'
    K8S = '\033[38;5;201m\033[1m'; BORG = '\033[38;5;46m\033[1m'
    DEEPMIND = '\033[38;5;51m\033[1m'; RANKBRAIN = '\033[38;5;226m\033[1m'
    CAPTCHA = '\033[38;5;208m\033[1m'; SMS = '\033[38;5;213m\033[1m'
    IPBYPASS = '\033[38;5;46m\033[1m'; AI = '\033[38;5;51m\033[1m'
    HTTP = '\033[38;5;46m\033[1m'; HTTPS = '\033[38;5;51m\033[1m'
    OKAY = '\033[38;5;46m\033[1m'; INFO = '\033[38;5;51m\033[1m'
    SUBDOMAIN = '\033[38;5;213m\033[1m'; DNS = '\033[38;5;51m\033[1m'
    WHOIS = '\033[38;5;226m\033[1m'; SSL = '\033[38;5;208m\033[1m'
    HEADER = '\033[38;5;118m\033[1m'; ISP = '\033[38;5;201m\033[1m'
    DIR = '\033[38;5;45m\033[1m'; PORT = '\033[38;5;141m\033[1m'
    CRAWL = '\033[38;5;229m\033[1m'; VULN = '\033[38;5;196m\033[1m'
    SAFETY = '\033[38;5;196m\033[1m'; WARN = '\033[38;5;226m\033[1m'
    HEAL = '\033[38;5;46m\033[1m'; SCALE = '\033[38;5;51m\033[1m'
    DEFEND = '\033[38;5;196m\033[1m'; RECOVER = '\033[38;5;213m\033[1m'
    AUTO = '\033[38;5;226m\033[1m'; NEURAL = '\033[38;5;201m\033[1m'
    TECH = '\033[38;5;87m\033[1m'; SECRET = '\033[38;5;196m\033[1m'
    API = '\033[38;5;208m\033[1m'; QUANTUMC = '\033[38;5;51m\033[1m'
    CVE = '\033[38;5;196m\033[1m'; COMPLIANCE = '\033[38;5;82m\033[1m'
    SMART = '\033[38;5;213m\033[1m'; PIPE = '\033[38;5;45m\033[1m'
    WEBSRV = '\033[38;5;226m\033[1m'; STEALTH = '\033[38;5;244m\033[1m'
    OMEGA = '\033[38;5;46m\033[1m'
    TITAN = '\033[38;5;226m\033[1m'
    APEX = '\033[38;5;201m\033[1m'
    SEARCH = '\033[38;5;51m\033[1m'
    LINK = '\033[38;5;213m\033[1m'
    URLM = '\033[38;5;46m\033[1m'


def p_ok(m):    print(f"{C.OKGREEN}[+] OK: {m}{C.RESET}", flush=True)
def p_info(m):  print(f"{C.CYAN}[*] {m}{C.RESET}", flush=True)
def p_warn(m):  print(f"{C.YELLOW}[!] {m}{C.RESET}", flush=True)
def p_err(m):   print(f"{C.RED}[-] {m}{C.RESET}", flush=True)
def p_crit(m):  print(f"{C.RED}\033[1m[CRITICAL] {m}{C.RESET}", flush=True)
def p_robot(m): print(f"{C.ROBOT}[ROBOT] {m}{C.RESET}", flush=True)
def p_clean(m): print(f"{C.CLEAN}[CLEANER] {m}{C.RESET}", flush=True)
def p_copy(m):  print(f"{C.COPY}[COPYRIGHT-DETECT] {m}{C.RESET}", flush=True)
def p_aegis(m): print(f"{C.AEGIS}[AEGIS] {m}{C.RESET}", flush=True)
def p_movie(m): print(f"{C.MOVIE}[MOVIE-COPYRIGHT] {m}{C.RESET}", flush=True)
def p_video(m): print(f"{C.VIDEO}[VIDEO-COPYRIGHT] {m}{C.RESET}", flush=True)
def p_stream(m):print(f"{C.STREAM}[STREAM-COPYRIGHT] {m}{C.RESET}", flush=True)
def p_image(m): print(f"{C.IMAGE}[IMAGE-COPYRIGHT] {m}{C.RESET}", flush=True)
def p_series(m):print(f"{C.SERIES}[SERIES-COPYRIGHT] {m}{C.RESET}", flush=True)
def p_cright(m):print(f"{C.CRIGHT}[COPYRIGHT-CLEAN] {m}{C.RESET}", flush=True)
def p_lang(m):  print(f"{C.LANG}[LANG-COPY] {m}{C.RESET}", flush=True)
def p_sys(m):   print(f"{C.SYS}[SERVER-COPY] {m}{C.RESET}", flush=True)
def p_gws(m):   print(f"{C.GWS}[GWS-COPY] {m}{C.RESET}", flush=True)
def p_esf(m):   print(f"{C.ESF}[ESF-COPY] {m}{C.RESET}", flush=True)
def p_apikey(m):print(f"{C.APIKEY}[APIKEY-COPY] {m}{C.RESET}", flush=True)
def p_cooldown(m):print(f"{C.COOLDOWN}[COOLDOWN-COPY] {m}{C.RESET}", flush=True)
def p_apollo(m):print(f"{C.APOLLO}[APOLLO] {m}{C.RESET}", flush=True)
def p_google_acc(m):print(f"{C.GOOGLE_ACC}[GOOGLE-ACCOUNT] {m}{C.RESET}", flush=True)
def p_google_sus(m):print(f"{C.GOOGLE_SUS}[GOOGLE-SUSPICIOUS] {m}{C.RESET}", flush=True)
def p_social_sus(m):print(f"{C.SOCIAL_SUS}[SOCIAL-SUSPICIOUS] {m}{C.RESET}", flush=True)
def p_vpn_sus(m):print(f"{C.VPN_SUS}[VPN-SUSPICIOUS] {m}{C.RESET}", flush=True)
def p_telegram(m):print(f"{C.TELEGRAM}[TELEGRAM] {m}{C.RESET}", flush=True)
def p_tiktok(m):print(f"{C.TIKTOK}[TIKTOK] {m}{C.RESET}", flush=True)
def p_discord(m):print(f"{C.DISCORD}[DISCORD] {m}{C.RESET}", flush=True)
def p_pinterest(m):print(f"{C.PINTEREST}[PINTEREST] {m}{C.RESET}", flush=True)
def p_whatsapp(m):print(f"{C.WHATSAPP}[WHATSAPP] {m}{C.RESET}", flush=True)
def p_facebook(m):print(f"{C.FACEBOOK}[FACEBOOK] {m}{C.RESET}", flush=True)
def p_instagram(m):print(f"{C.INSTAGRAM}[INSTAGRAM] {m}{C.RESET}", flush=True)
def p_twitter(m):print(f"{C.TWITTER}[TWITTER] {m}{C.RESET}", flush=True)
def p_vpn(m):   print(f"{C.VPN}[VPN] {m}{C.RESET}", flush=True)
def p_ult(m):   print(f"{C.ULTIMATE}[ULTIMATE] {m}{C.RESET}", flush=True)
def p_wall(m):  print(f"{C.WALL}[WALL-BREAK] {m}{C.RESET}", flush=True)
def p_okay(m):  print(f"{C.OKAY}[OKAY] {m}{C.RESET}", flush=True)
def p_token(m): print(f"{C.TOKEN}[TOKEN] {m}{C.RESET}", flush=True)
def p_fact(m):  print(f"{C.FACTORY}[FACTORY] {m}{C.RESET}", flush=True)
def p_k8s(m):   print(f"{C.K8S}[K8S] {m}{C.RESET}", flush=True)
def p_borg(m):  print(f"{C.BORG}[BORG] {m}{C.RESET}", flush=True)
def p_dm(m):    print(f"{C.DEEPMIND}[DEEPMIND] {m}{C.RESET}", flush=True)
def p_rb(m):    print(f"{C.RANKBRAIN}[RANKBRAIN] {m}{C.RESET}", flush=True)
def p_captcha(m):print(f"{C.CAPTCHA}[CAPTCHA] {m}{C.RESET}", flush=True)
def p_sms(m):   print(f"{C.SMS}[SMS] {m}{C.RESET}", flush=True)
def p_ipb(m):   print(f"{C.IPBYPASS}[IP-BYPASS] {m}{C.RESET}", flush=True)
def p_ai(m):    print(f"{C.AI}[AI] {m}{C.RESET}", flush=True)
def p_http(m):  print(f"{C.HTTP}[HTTP] {m}{C.RESET}", flush=True)
def p_https(m): print(f"{C.HTTPS}[HTTPS] {m}{C.RESET}", flush=True)
def p_sub(m):   print(f"{C.SUBDOMAIN}[SUBDOMAIN] {m}{C.RESET}", flush=True)
def p_dns(m):   print(f"{C.DNS}[DNS] {m}{C.RESET}", flush=True)
def p_whois(m): print(f"{C.WHOIS}[WHOIS] {m}{C.RESET}", flush=True)
def p_ssl(m):   print(f"{C.SSL}[SSL] {m}{C.RESET}", flush=True)
def p_header(m):print(f"{C.HEADER}[HEADER] {m}{C.RESET}", flush=True)
def p_isp(m):   print(f"{C.ISP}[ISP] {m}{C.RESET}", flush=True)
def p_dir(m):   print(f"{C.DIR}[DIR] {m}{C.RESET}", flush=True)
def p_port(m):  print(f"{C.PORT}[PORT] {m}{C.RESET}", flush=True)
def p_crawl(m): print(f"{C.CRAWL}[CRAWL] {m}{C.RESET}", flush=True)
def p_vuln(m):  print(f"{C.VULN}[VULN] {m}{C.RESET}", flush=True)
def p_safety(m):print(f"{C.SAFETY}[SAFETY] {m}{C.RESET}", flush=True)
def p_heal(m):  print(f"{C.HEAL}[AUTO-HEAL] {m}{C.RESET}", flush=True)
def p_scale(m): print(f"{C.SCALE}[AUTO-SCALE] {m}{C.RESET}", flush=True)
def p_defend(m):print(f"{C.DEFEND}[AUTO-DEFENSE] {m}{C.RESET}", flush=True)
def p_recover(m):print(f"{C.RECOVER}[AUTO-RECOVERY] {m}{C.RESET}", flush=True)
def p_auto(m):  print(f"{C.AUTO}[AUTO] {m}{C.RESET}", flush=True)
def p_neural(m):print(f"{C.NEURAL}[NEURAL-NET] {m}{C.RESET}", flush=True)
def p_tech(m):  print(f"{C.TECH}[TECH] {m}{C.RESET}", flush=True)
def p_secret(m):print(f"{C.SECRET}[SECRET] {m}{C.RESET}", flush=True)
def p_api(m):   print(f"{C.API}[API] {m}{C.RESET}", flush=True)
def p_quantum(m):print(f"{C.QUANTUMC}[QUANTUM] {m}{C.RESET}", flush=True)
def p_cve(m):   print(f"{C.CVE}[CVE] {m}{C.RESET}", flush=True)
def p_comp(m):  print(f"{C.COMPLIANCE}[COMPLIANCE] {m}{C.RESET}", flush=True)
def p_smart(m): print(f"{C.SMART}[SMART-AI] {m}{C.RESET}", flush=True)
def p_pipe(m):  print(f"{C.PIPE}[PIPELINE] {m}{C.RESET}", flush=True)
def p_websrv(m):print(f"{C.WEBSRV}[WEB-SERVER] {m}{C.RESET}", flush=True)
def p_stealth(m):print(f"{C.STEALTH}[STEALTH] {m}{C.RESET}", flush=True)
def p_omega(m): print(f"{C.OMEGA}[OMEGA] {m}{C.RESET}", flush=True)
def p_titan(m): print(f"{C.TITAN}[TITAN] {m}{C.RESET}", flush=True)
def p_apex(m):  print(f"{C.APEX}[APEX] {m}{C.RESET}", flush=True)
def p_search(m):print(f"{C.SEARCH}[SEARCH-MODE] {m}{C.RESET}", flush=True)
def p_link(m):  print(f"{C.LINK}[LINK-MODE] {m}{C.RESET}", flush=True)
def p_urlm(m):  print(f"{C.URLM}[URL-MODE] {m}{C.RESET}", flush=True)


_SINGULARITY_MODE = False
_AI_ROBOT_LOCK = False


def _unstoppable_handler(signum, frame):
    if _SINGULARITY_MODE or _AI_ROBOT_LOCK:
        p_robot(f"Signal {signum} absorbed")
        return
    raise KeyboardInterrupt()


def install_singularity_lock():
    global _SINGULARITY_MODE, _AI_ROBOT_LOCK
    _SINGULARITY_MODE = True
    _AI_ROBOT_LOCK = True
    for sn in ['SIGINT', 'SIGTERM', 'SIGHUP', 'SIGQUIT', 'SIGTSTP', 'SIGUSR1', 'SIGUSR2']:
        if hasattr(signal, sn):
            try:
                signal.signal(getattr(signal, sn), _unstoppable_handler)
            except Exception:
                pass
    p_robot("★ TITAN APEX SINGULARITY LOCK ACTIVE - CANNOT BE STOPPED ★")


def release_singularity():
    global _SINGULARITY_MODE, _AI_ROBOT_LOCK
    _SINGULARITY_MODE = False
    _AI_ROBOT_LOCK = False


def safety_check_web_server_only(host):
    LOCAL_HOSTNAMES = {'localhost', 'localhost.localdomain', 'mycomputer',
                       'my-pc', 'desktop', 'laptop'}
    LOCAL_IP_RANGES = [
        ipaddress.ip_network('10.0.0.0/8'),
        ipaddress.ip_network('172.16.0.0/12'),
        ipaddress.ip_network('192.168.0.0/16'),
        ipaddress.ip_network('127.0.0.0/8'),
        ipaddress.ip_network('169.254.0.0/16'),
    ]
    h = str(host).lower().strip('[]')
    if h in LOCAL_HOSTNAMES:
        p_err(f"LOCAL HOSTNAME blocked: {h}")
        return False
    try:
        ip = ipaddress.ip_address(h)
        for net in LOCAL_IP_RANGES:
            if ip in net:
                p_err(f"PRIVATE IP blocked: {ip}")
                return False
    except ValueError:
        pass
    p_ok(f"WEB SERVER target validated: {h}")
    return True


# ============================================
# IMPORTS FROM SPLIT MODULES
# ============================================
from apex_config import (
    VERSION as CFG_VERSION, BUILD_NUMBER as CFG_BUILD,
    DEFAULT_HTTP_PORT, DEFAULT_HTTPS_PORT, TIMEOUT, REQ_HEADERS,
    USER_AGENTS, CONFIG,
    COMMON_SUBS, COMMON_DIRS, COMMON_PORTS,
    TECH_SIGNATURES, SECRET_PATTERNS,
    CORS_TEST_ORIGINS, HTTP_METHODS, BACKUP_EXTS,
    COPYRIGHT_KNOWN_SITES, COPYRIGHT_META_SIGNATURES, COPYRIGHT_DEFAULT_TITLES,
    MOVIE_COPYRIGHT_SIGNATURES, MOVIE_TITLE_KEYWORDS,
    VIDEO_FILE_EXTENSIONS, STREAMING_PLAYER_SIGNATURES, STREAMING_PROTOCOLS,
    SERIES_COPYRIGHT_SIGNATURES, SERIES_TITLE_KEYWORDS, SERIES_CLEANER_PATHS,
    IMAGE_COPYRIGHT_SIGNATURES, IMAGE_KEYWORDS,
    PROGRAMMING_LANGUAGE_SIGNATURES,
    WEB_SERVER_SYSTEM_SIGNATURES,
    GWS_CLEANER_PATHS, ESF_CLEANER_PATHS,
    GOOGLE_ACCOUNT_SERVER_SIGNATURES, GOOGLE_SUSPICIOUS_SERVER_SIGNATURES,
    SOCIAL_PLATFORM_SIGNATURES, SOCIAL_CLEANER_PATHS,
    VPN_SUSPICIOUS_SIGNATURES, VPN_KNOWN_DOMAINS, VPN_CLEANER_PATHS,
    GOOGLE_ACCOUNT_CLEANER_PATHS, GOOGLE_SUSPICIOUS_SERVER_PATHS,
    API_KEY_COPYRIGHT_SIGNATURES, APIKEY_CLEANER_PATHS,
    COOLDOWN_SYSTEM_SIGNATURES, COOLDOWN_CLEANER_PATHS,
    FRAMEWORK_COPY_SIGNATURES,
    CLEANER_HTTP_PATHS, CLEANER_HTTPS_PATHS, CLEANER_ANOTHER_PATHS,
    CLEANER_COOKIES_DATA_PATHS, CLEANER_ALL_COOKIES_PATHS,
    CLEANER_COMPLETE_DATA_PATHS, CLEANER_MOVIE_PATHS, CLEANER_VIDEO_PATHS,
    CLEANER_STREAMING_PATHS, CLEANER_IMAGE_PATHS, CLEANER_LANGUAGE_PATHS,
    CLEANER_SYSTEM_PATHS, CLEANER_ALL_GROUPS,
    HONEYPOT_WALL_PATTERNS, FIREWALL_WALL_PATTERNS,
    API_TOKEN_TARGETS, FACTORY_PATTERNS, ACCOUNT_ACTION_PATTERNS,
)

from apex_ip_bypass import AdvancedIPBypass
from apex_ai_robots import AIRobotManager
from apex_cleaner import CleanerCore
from apex_copyright import CopyrightDetectors
from apex_social import SocialSuspiciousCleaner
from apex_vpn import VPNSuspiciousCleaner
from apex_google import GoogleSuspiciousCleaner
from apex_recon import ReconModules
from apex_url_mode import URLModeHandler
from apex_link_mode import LinkModeHandler
from apex_search_mode import SearchModeHandler


# ============================================
# MAIN CLASS
# ============================================
class TitanApexOmega:
    def __init__(self, input_info, args=None):
        self.args = args
        self.input_info = input_info
        self.mode = input_info['mode']
        self.target = input_info['target_url']

        self.session = requests.Session()
        self.session.headers.update(REQ_HEADERS)
        self.session.headers.update({'User-Agent': random.choice(USER_AGENTS)})

        self.rate_limiter = RateLimiter(getattr(args, 'rate_limit', 0) if args else 0)
        self.retries = getattr(args, 'retry', 0) if args else 0
        self.stealth = getattr(args, 'stealth', False) if args else False

        if args and getattr(args, 'proxy', None):
            self.session.proxies = {'http': args.proxy, 'https': args.proxy}

        self._last_request = 0
        self.request_count = 0
        self.start_time = time.time()

        self.findings = []
        self.subdomain_results = []
        self.dns_results = {}
        self.whois_results = {}
        self.ssl_results = {}
        self.header_results = {}
        self.isp_results = {}
        self.directory_results = []
        self.port_scan_results = []
        self.crawler_results = []
        self.vuln_scan_results = []
        self.tech_results = {}
        self.secret_results = []
        self.cors_results = []
        self.backup_results = []
        self.git_results = []
        self.env_results = []
        self.open_redirect_results = []
        self.lfi_results = []
        self.ssrf_results = []

        # 18 Copyright results
        self.copy_results = self._empty_result('matched_signatures', 'matched_meta')
        self.movie_copy_results = self._empty_result('matched_movie', 'matched_titles', 'matched_players')
        self.video_copy_results = self._empty_result('matched_video', 'matched_players', 'matched_extensions')
        self.stream_copy_results = self._empty_result('matched_stream', 'matched_protocols', 'matched_players')
        self.image_copy_results = self._empty_result('matched_image', 'matched_keywords')
        self.series_copy_results = self._empty_result('matched_series', 'matched_titles')
        self.lang_copy_results = self._empty_result('matched_languages', 'matched_frameworks')
        self.system_copy_results = self._empty_result('matched_systems', 'matched_versions')
        self.gws_copy_results = self._empty_result('matched_gws')
        self.esf_copy_results = self._empty_result('matched_esf')
        self.apikey_copy_results = self._empty_result('matched_apikeys', 'matched_types', 'matched_patterns')
        self.cooldown_copy_results = self._empty_result('matched_cooldown', 'matched_types', 'matched_status_codes')
        self.google_account_copy_results = self._empty_result(
            'matched_hosts', 'matched_types', 'matched_headers', 'matched_paths')
        self.google_suspicious_copy_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.telegram_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.tiktok_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.discord_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.pinterest_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.whatsapp_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.facebook_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.instagram_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.twitter_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.vpn_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.freevpn_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.privatevpn_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')
        self.protocolvpn_suspicious_results = self._empty_result(
            'matched_types', 'matched_headers', 'matched_bodies', 'matched_status_codes')

        # Mode-specific results
        self.url_mode_results = self._empty_result('pages_crawled', 'assets_found', 'forms_found')
        self.link_mode_results = self._empty_result('links_followed', 'assets_extracted', 'endpoints_found')
        self.search_mode_results = self._empty_result('queries_parsed', 'results_extracted', 'pages_analyzed')

        self.cleaner_stats = {
            'total_cleaned': 0, 'cookies_cleaned': 0, 'sessions_cleaned': 0,
            'tokens_cleaned': 0, 'devices_cleaned': 0, 'api_tokens_cleaned': 0,
            'api_keys_cleaned': 0, 'sms_codes_cleaned': 0,
            'http_cleaned': 0, 'https_cleaned': 0, 'another_cleaned': 0,
            'cookies_data_cleaned': 0, 'all_cookies_cleaned': 0,
            'complete_data_cleaned': 0,
            'movie_cleaned': 0, 'video_cleaned': 0, 'streaming_cleaned': 0,
            'image_cleaned': 0, 'series_cleaned': 0,
            'language_cleaned': 0, 'system_cleaned': 0,
            'gws_cleaned': 0, 'esf_cleaned': 0,
            'apikey_cleaned': 0, 'cooldown_cleaned': 0,
            'google_account_cleaned': 0, 'google_suspicious_cleaned': 0,
            'telegram_cleaned': 0, 'tiktok_cleaned': 0,
            'discord_cleaned': 0, 'pinterest_cleaned': 0,
            'whatsapp_cleaned': 0, 'facebook_cleaned': 0,
            'instagram_cleaned': 0, 'twitter_cleaned': 0,
            'vpn_cleaned': 0, 'freevpn_cleaned': 0,
            'privatevpn_cleaned': 0, 'protocolvpn_cleaned': 0,
            'honeypot_wall_broken': 0, 'firewall_wall_broken': 0,
            'factory_restarted': 0, 'okay_signals': 0,
            'auto_cleaned': 0, 'verified': 0, 'pipeline_runs': 0,
            'copyright_instant_cleaned': 0, 'copyright_full_cleaned': 0,
            'web_system_cleaned': 0, 'gws_system_cleaned': 0, 'esf_system_cleaned': 0,
            'apikey_system_cleaned': 0, 'cooldown_system_cleaned': 0,
            'google_account_system_cleaned': 0,
            'google_suspicious_system_cleaned': 0,
            'social_suspicious_system_cleaned': 0,
            'vpn_suspicious_system_cleaned': 0,
            'ai_robot_actions': 0,
            'ip_bypasses': 0,
        }

        # Advanced IP-Bypass state
        self.real_ip = self._detect_real_ip()
        self.current_bypass_ip = None

        # Subsystems
        self.ai_robots = AIRobotManager(self)
        self.cleaner = CleanerCore(self)
        self.copyright = CopyrightDetectors(self)
        self.social = SocialSuspiciousCleaner(self)
        self.vpn = VPNSuspiciousCleaner(self)
        self.google = GoogleSuspiciousCleaner(self)
        self.recon = ReconModules(self)
        self.ip_bypass_engine = AdvancedIPBypass(self)

        # Mode handlers
        self.url_handler = URLModeHandler(self)
        self.link_handler = LinkModeHandler(self)
        self.search_handler = SearchModeHandler(self)

        if self.target:
            self.parse_target()

    @staticmethod
    def _empty_result(*list_fields):
        r = {
            'is_copy': False, 'copy_score': 0,
            'body_hash': '', 'title': '', 'generator': '',
            'detected_at': '', 'destroyed': False, 'destroy_count': 0,
        }
        for f in list_fields:
            r[f] = []
        return r

    def _detect_real_ip(self):
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"

    def parse_target(self):
        if not self.target.startswith(('http://', 'https://')):
            self.target = 'http://' + self.target
        if self.target.endswith('/'):
            self.target = self.target[:-1]
        sp = urlparse(self.target)
        self.protocol = sp.scheme
        self.hostname = sp.hostname
        self.port = (getattr(self.args, 'port', None)
                     if self.args and getattr(self.args, 'port', None)
                     else sp.port or (443 if self.protocol == 'https' else 80))
        try:
            ipaddress.ip_address(self.hostname)
            self.ip = self.hostname
        except ValueError:
            try:
                self.ip = socket.gethostbyname(self.hostname)
            except Exception:
                self.ip = "0.0.0.0"
        if self.port in (80, 443):
            self.base_url = f"{self.protocol}://{self.hostname}"
        else:
            self.base_url = f"{self.protocol}://{self.hostname}:{self.port}"

    def _request(self, method, url, **kwargs):
        self.rate_limiter.wait()
        now = time.time()
        wait = 0.1 - (now - self._last_request)
        if wait > 0:
            time.sleep(wait)
        self._last_request = time.time()

        if self.stealth:
            time.sleep(random.uniform(0.3, 1.2))
            self.session.headers['User-Agent'] = random.choice(USER_AGENTS)

        kwargs.setdefault('timeout', TIMEOUT)
        kwargs.setdefault('verify', False)

        last_exc = None
        for attempt in range(self.retries + 1):
            try:
                self.request_count += 1
                return self.session.request(method, url, **kwargs)
            except Exception as e:
                last_exc = e
                if attempt < self.retries:
                    time.sleep(0.3 * (attempt + 1))
        raise last_exc

    def _add_finding(self, sev, category, title, evidence="", url=""):
        self.findings.append({
            'severity': sev, 'category': category, 'title': title,
            'evidence': evidence, 'url': url,
            'time': datetime.datetime.now().isoformat(),
        })

    # ============================================
    # DELEGATION METHODS (to subsystems)
    # ============================================
    def ip_bypass(self):
        return self.ip_bypass_engine.run_advanced_bypass()

    def detect_copy(self):
        return self.copyright.detect_web_copy()

    def detect_movie_copy(self):
        return self.copyright.detect_movie_copy()

    def detect_video_copy(self):
        return self.copyright.detect_video_copy()

    def detect_streaming_copy(self):
        return self.copyright.detect_streaming_copy()

    def detect_image_copy(self):
        return self.copyright.detect_image_copy()

    def detect_series_copy(self):
        return self.copyright.detect_series_copy()

    def detect_language_copy(self):
        return self.copyright.detect_language_copy()

    def detect_system_copy(self):
        return self.copyright.detect_system_copy()

    def detect_gws_copy(self):
        return self.copyright.detect_gws_copy()

    def detect_esf_copy(self):
        return self.copyright.detect_esf_copy()

    def detect_apikey_copy(self):
        return self.copyright.detect_apikey_copy()

    def detect_cooldown_copy(self):
        return self.copyright.detect_cooldown_copy()

    def detect_google_account_copy(self):
        return self.google.detect_google_account_copy()

    def detect_google_suspicious_server(self):
        return self.google.detect_google_suspicious_server()

    def detect_social_suspicious_server(self, platform):
        return self.social.detect_social_suspicious_server(platform)

    def detect_vpn_suspicious_server(self):
        return self.vpn.detect_vpn_suspicious_server()

    def universal_google_account_clean(self):
        return self.google.universal_google_account_clean()

    def universal_google_suspicious_clean(self):
        return self.google.universal_google_suspicious_clean()

    def universal_social_suspicious_clean(self, platform):
        return self.social.universal_social_suspicious_clean(platform)

    def universal_all_social_suspicious_clean(self):
        return self.social.universal_all_social_suspicious_clean()

    def universal_vpn_suspicious_clean(self):
        return self.vpn.universal_vpn_suspicious_clean()

    def universal_all_copy_detect(self):
        p_apollo("=== ALL 18 COPYRIGHT DETECTION ===")
        self.detect_copy()
        self.detect_movie_copy()
        self.detect_series_copy()
        self.detect_video_copy()
        self.detect_streaming_copy()
        self.detect_image_copy()
        self.detect_language_copy()
        self.detect_system_copy()
        self.detect_gws_copy()
        self.detect_esf_copy()
        self.detect_apikey_copy()
        self.detect_cooldown_copy()
        self.detect_google_account_copy()
        self.detect_google_suspicious_server()
        for platform in ['Telegram', 'TikTok', 'Discord', 'Pinterest',
                         'WhatsApp', 'Facebook', 'Instagram', 'Twitter']:
            self.detect_social_suspicious_server(platform)
        self.detect_vpn_suspicious_server()

    def universal_copyright_clean(self):
        p_cright("=== TITAN_APEX_OMEGA: COPYRIGHT CLEAN (18 types) ===")
        detected = []
        for label, fn in [
            ('IMAGE', self.detect_image_copy), ('VIDEO', self.detect_video_copy),
            ('STREAMING', self.detect_streaming_copy),
            ('MOVIE', self.detect_movie_copy), ('SERIES', self.detect_series_copy),
            ('WEB', self.detect_copy), ('LANGUAGE', self.detect_language_copy),
            ('SYSTEM', self.detect_system_copy),
            ('GWS', self.detect_gws_copy), ('ESF', self.detect_esf_copy),
            ('APIKEY', self.detect_apikey_copy),
            ('COOLDOWN', self.detect_cooldown_copy),
            ('GOOGLE-ACCOUNT', self.detect_google_account_copy),
            ('GOOGLE-SUSPICIOUS', self.detect_google_suspicious_server),
        ]:
            p_info(f"--- Copyright {label} Detection ---")
            r = fn()
            if r['is_copy']:
                detected.append(label)
        if detected:
            p_cright(f"⚠️  DETECTED: {', '.join(detected)}")
        else:
            p_ok("No copyright detected")
        return detected

    def run_clean_pipeline(self):
        return self.cleaner.run_32_step_pipeline()

    def run_all_recon(self):
        return self.recon.run_all_recon()

    def run_full_recon(self):
        return self.recon.run_full_recon()

    def run_ai_robots(self):
        self.cleaner_stats['ai_robot_actions'] += self.ai_robots.run_all()

    def break_honeypot_wall(self):
        return self.cleaner.break_honeypot_wall()

    def break_firewall_wall(self):
        return self.cleaner.break_firewall_wall()

    def factory_restart(self):
        return self.cleaner.factory_restart()

    def api_token_attack(self):
        return self.cleaner.api_token_attack()

    def account_action_destroyer(self):
        return self.cleaner.account_action_destroyer()

    # ============================================
    # MODE DISPATCHERS
    # ============================================
    def run_url_mode(self):
        """--url mode: direct URL target with full stack."""
        p_urlm("=" * 70)
        p_urlm("URL MODE HANDLER - Direct URL Target")
        p_urlm(f"Target: {self.target}")
        p_urlm("=" * 70)
        return self.url_handler.run(self.args)

    def run_link_mode(self):
        """--link mode: specific link (file/endpoint) with recursive follow."""
        p_link("=" * 70)
        p_link("LINK MODE HANDLER - Specific Link/Endpoint Target")
        p_link(f"Link: {self.target}")
        p_link("=" * 70)
        return self.link_handler.run(self.args)

    def run_search_mode(self):
        """--search mode: search URL with query placeholder + multi-page crawl."""
        p_search("=" * 70)
        p_search("SEARCH MODE HANDLER - Search URL + Query Parser")
        p_search(f"Search URL: {self.target}")
        p_search("=" * 70)
        return self.search_handler.run(self.args)

    def run_ultimate(self):
        p_titan("★ ULTIMATE MODE — EVERYTHING ★")
        p_apex(f"Mode: {self.mode.upper()}")
        self.ip_bypass()
        self.run_full_recon()
        self.universal_copyright_clean()
        self.run_clean_pipeline()
        self.run_ai_robots()
        self.break_honeypot_wall()
        self.break_firewall_wall()

    def run_autonomous(self):
        install_singularity_lock()
        print(f"\n{C.ROBOT}{'=' * 70}{C.RESET}")
        print(f"{C.ROBOT}★ FULLY AUTONOMOUS - NEVER STOPS ★{C.RESET}")
        print(f"{C.ROBOT}  18 Copyright Detectors → INSTANT Cleaners{C.RESET}")
        print(f"{C.ROBOT}  Google Account + Suspicious Server Instant Cleaner{C.RESET}")
        print(f"{C.ROBOT}  8 Social Suspicious Cleaners{C.RESET}")
        print(f"{C.ROBOT}  3 VPN Suspicious Cleaners (Free/Private/Protocol){C.RESET}")
        print(f"{C.ROBOT}  Advanced IP-Bypass (12 headers + proxy chain){C.RESET}")
        print(f"{C.ROBOT}  14 AI ROBOTS{C.RESET}")
        print(f"{C.ROBOT}  32-STEP CLEANER PIPELINE{C.RESET}")
        print(f"{C.ROBOT}  Mode: {self.mode.upper()}{C.RESET}")
        print(f"{C.ROBOT}{'=' * 70}{C.RESET}")

        if getattr(self.args, 'ai_robot_all', False):
            self.ai_robots.enable_all()
        else:
            for flag, name in [
                ('auto_heal', 'Auto-Healing'), ('auto_scale', 'Auto-Scaling'),
                ('auto_defend', 'Auto-Defense'), ('auto_recover', 'Auto-Recovery'),
                ('auto_clean', 'Auto-Clean'), ('auto_detect', 'Auto-Detect'),
                ('auto_destroy', 'Auto-Destroy'), ('auto_verify', 'Auto-Verify'),
                ('auto_report', 'Auto-Report'), ('neural_net', 'Neural-Network'),
                ('auto_quantum', 'Quantum-Route'), ('auto_stealth', 'Stealth-Mode'),
                ('auto_pivot', 'Auto-Pivot'), ('auto_replicate', 'Auto-Replicate'),
            ]:
                if getattr(self.args, flag, False):
                    self.ai_robots.enable(name)

        phases = [
            ("IP-BYPASS ADVANCED", self.ip_bypass),
            ("MODE-SPECIFIC PROCESSING", self._mode_specific_phase),
            ("GOOGLE-ACCOUNT-CLEAN", self.universal_google_account_clean),
            ("GOOGLE-SUSPICIOUS-CLEAN", self.universal_google_suspicious_clean),
            ("SOCIAL-SUSPICIOUS-CLEAN (ALL 8)", self.universal_all_social_suspicious_clean),
            ("VPN-SUSPICIOUS-CLEAN", self.universal_vpn_suspicious_clean),
            ("COPYRIGHT-CLEAN (18 TYPES)", self.universal_copyright_clean),
            ("CLEANER PIPELINE (32 STEPS)", self.run_clean_pipeline),
            ("AI ROBOTS (14)", self.run_ai_robots),
            ("FULL RECON", self.run_full_recon),
            ("HONEYPOT WALL", self.break_honeypot_wall),
            ("FIREWALL WALL", self.break_firewall_wall),
            ("API TOKEN ATTACK", self.api_token_attack),
            ("ACCOUNT DESTROY", self.account_action_destroyer),
            ("FACTORY RESTART", self.factory_restart),
            ("EXPORT", self.export_txt),
            ("FINAL SUMMARY", self.print_summary),
        ]
        iteration = 0
        while True:
            iteration += 1
            p_robot(f"\n{'=' * 60}")
            p_robot(f"★ AUTONOMOUS ITERATION #{iteration} ★")
            p_robot(f"  Target: {self.target}")
            p_robot(f"  Mode: {self.mode.upper()}")
            p_robot(f"  Cleaned: {self.cleaner_stats['total_cleaned']}")
            p_robot(f"{'=' * 60}")
            for label, fn in phases:
                p_robot(f"▶ {label}")
                try:
                    fn()
                except Exception as e:
                    p_err(f"{label} failed: {e}")
                time.sleep(0.1)
            p_robot(f"★ ITERATION #{iteration} COMPLETE ★")
            time.sleep(2)

    def _mode_specific_phase(self):
        """Run the mode-specific handler once during autonomous loop."""
        if self.mode == 'url':
            self.url_handler.process_once()
        elif self.mode == 'link':
            self.link_handler.process_once()
        elif self.mode == 'search':
            self.search_handler.process_once()

    def export_txt(self):
        os.makedirs(CONFIG['export_dir'], exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = f"{CONFIG['export_dir']}/titan_apex_omega_{self.hostname}_{ts}.txt"
        try:
            data = {
                'tool': RELEASE_NAME, 'version': VERSION,
                'target': self.target, 'mode': self.mode,
                'hostname': self.hostname, 'ip': self.ip, 'port': self.port,
                'time': datetime.datetime.now().isoformat(),
                'subdomains': self.subdomain_results,
                'dns': self.dns_results, 'whois': self.whois_results,
                'isp': self.isp_results, 'directories': self.directory_results,
                'ports': self.port_scan_results, 'vulns': self.vuln_scan_results,
                'secrets': self.secret_results, 'cors': self.cors_results,
                'cleaner_stats': self.cleaner_stats,
                'ai_robots': dict(self.ai_robots.stats),
                'copy_results': self.copy_results,
                'google_account': self.google_account_copy_results,
                'google_suspicious': self.google_suspicious_copy_results,
                'telegram_suspicious': self.telegram_suspicious_results,
                'tiktok_suspicious': self.tiktok_suspicious_results,
                'discord_suspicious': self.discord_suspicious_results,
                'pinterest_suspicious': self.pinterest_suspicious_results,
                'whatsapp_suspicious': self.whatsapp_suspicious_results,
                'facebook_suspicious': self.facebook_suspicious_results,
                'instagram_suspicious': self.instagram_suspicious_results,
                'twitter_suspicious': self.twitter_suspicious_results,
                'vpn_suspicious': self.vpn_suspicious_results,
                'freevpn_suspicious': self.freevpn_suspicious_results,
                'privatevpn_suspicious': self.privatevpn_suspicious_results,
                'protocolvpn_suspicious': self.protocolvpn_suspicious_results,
                'url_mode': self.url_mode_results,
                'link_mode': self.link_mode_results,
                'search_mode': self.search_mode_results,
                'real_ip': self.real_ip,
                'ip_bypasses': self.cleaner_stats['ip_bypasses'],
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"{RELEASE_NAME}\n")
                f.write("=" * 80 + "\n")
                f.write(json.dumps(data, indent=2, default=str))
            p_ok(f"TXT report: {filepath}")
            return filepath
        except Exception as e:
            p_err(f"Export failed: {e}")
            return None

    def print_summary(self):
        print(f"\n{C.BOLD}=== FINAL SUMMARY ==={C.RESET}")
        print(f"  Tool            : {RELEASE_NAME}")
        print(f"  Target          : {self.target}")
        print(f"  Mode            : {self.mode.upper()}")
        for label, r in [
            ('WEB', self.copy_results),
            ('MOVIE', self.movie_copy_results),
            ('VIDEO', self.video_copy_results),
            ('STREAM', self.stream_copy_results),
            ('IMAGE', self.image_copy_results),
            ('SERIES', self.series_copy_results),
            ('LANG', self.lang_copy_results),
            ('SYS', self.system_copy_results),
            ('GWS', self.gws_copy_results),
            ('ESF', self.esf_copy_results),
            ('APIKEY', self.apikey_copy_results),
            ('COOLDOWN', self.cooldown_copy_results),
            ('GOOGLE-ACC', self.google_account_copy_results),
            ('GOOGLE-SUS', self.google_suspicious_copy_results),
            ('TELEGRAM-SUS', self.telegram_suspicious_results),
            ('TIKTOK-SUS', self.tiktok_suspicious_results),
            ('DISCORD-SUS', self.discord_suspicious_results),
            ('PINTEREST-SUS', self.pinterest_suspicious_results),
            ('WHATSAPP-SUS', self.whatsapp_suspicious_results),
            ('FACEBOOK-SUS', self.facebook_suspicious_results),
            ('INSTAGRAM-SUS', self.instagram_suspicious_results),
            ('TWITTER-SUS', self.twitter_suspicious_results),
            ('VPN-SUS', self.vpn_suspicious_results),
            ('FREEVPN-SUS', self.freevpn_suspicious_results),
            ('PRIVATEVPN-SUS', self.privatevpn_suspicious_results),
            ('PROTOCOLVP-SUS', self.protocolvpn_suspicious_results),
        ]:
            v = f"YES (destroyed={r['destroy_count']})" if r['is_copy'] else 'NO'
            print(f"  {label:<14}: {v}")
        print(f"  Total Cleaned   : {self.cleaner_stats['total_cleaned']}")
        print(f"  AI Robot Actions: {self.cleaner_stats['ai_robot_actions']}")
        print(f"  IP-Bypasses     : {self.cleaner_stats['ip_bypasses']}")
        print(f"  Real IP         : {self.real_ip}")
        print(f"  Findings        : {len(self.findings)}")
        self.ai_robots.summary()
        print(f"{C.BOLD}==={C.RESET}")


# ============================================
# RATE LIMITER
# ============================================
class RateLimiter:
    def __init__(self, rate_per_sec=0):
        self.rate = rate_per_sec
        self.last = 0
        self.lock = threading.Lock()

    def wait(self):
        if self.rate <= 0:
            return
        with self.lock:
            now = time.time()
            min_interval = 1.0 / self.rate
            elapsed = now - self.last
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            self.last = time.time()


# ============================================
# BANNER
# ============================================
BANNER = r"""
================================================================================
   _______ _____ _______       _   _    _____  _____  ______ __   __
  |__   __|_   _|__   __|/\   | \ | |  / ____|/ __ \|  ____|\ \ / /
     | |    | |    | |  /  \  |  \| | | |  __| |  | | |__    \ V /
     | |    | |    | | / /\ \ | . ` | | | |_ | |  | |  __|    > <
     | |   _| |_   | |/ ____ \| |\  | | |__| | |__| | |____  / . \
     |_|  |_____|  |_/_/    \_\_| \_|  \_____|\____/|______|/_/ \_\

   _____   ____  _____  ______ _____ _______ ______ _____  ________   __
  / ____| / __ \|  __ \|  ____|  __ \__   __|  ____|  __ \|  ____\ \ / /
 | |  __ | |  | | |  | | |__  | |  | | | |  | |__  | |__) | |__   \ V /
 | | |_ || |  | | |  | |  __| | |  | | | |  |  __| |  _  /|  __|   > <
 | |__| || |__| | |__| | |____| |__| | | |  | |____| | \ \| |____ / . \
  \_____| \____/|_____/|______|_____/  |_|  |______|_|  \_\______/_/ \_\

  TITAN_APEX_OMEGA v17000 - TITAN APEX EDITION
  WEB SERVER ONLY | FULLY AUTONOMOUS | UNSTOPPABLE AI ROBOT

  ★ --ultimate + --full + --autonomous = ALL WORK TOGETHER
  ★ 18 COPYRIGHT DETECTORS → 18 INSTANT CLEANERS
  ★ GOOGLE SUSPICIOUS SERVER → INSTANT CLEANER
  ★ 8 SOCIAL SUSPICIOUS CLEANERS:
       Telegram / TikTok / Discord / Pinterest /
       WhatsApp / Facebook / Instagram / Twitter
  ★ 3 VPN SUSPICIOUS CLEANERS:
       Free VPN / Private VPN / Protocol VPN
  ★ ADVANCED IP-BYPASS: 12 headers + proxy chain rotation
  ★ 14 AI ROBOTS AUTOMATED FEATURES
  ★ 32-STEP CLEANER PIPELINE
  ★ THREE INPUT MODES (fully separate code paths):
       --url | --link | --search
  ★ --features flag (full feature matrix)
  ★ WEB SERVER ONLY - AUTHORIZED TESTING ONLY
================================================================================
"""


# ============================================
# FEATURES PRINT
# ============================================
def print_features():
    print(BANNER)
    print(f"""
{C.ULTIMATE}════════════════════════════════════════════════════════════════════════
  TITAN_APEX_OMEGA v{VERSION} - FULL FEATURE MATRIX
════════════════════════════════════════════════════════════════════════{C.RESET}

{C.COPY}18 COPYRIGHT TYPES → 18 INSTANT CLEANERS:{C.RESET}
  1. IMAGE       → Image Cleaner
  2. VIDEO       → Video Cleaner
  3. STREAMING   → Streaming Cleaner
  4. MOVIE       → Movie Cleaner
  5. SERIES      → Series Cleaner
  6. WEB         → Web Cleaner
  7. LANGUAGE    → Language Cleaner
  8. SYSTEM      → System Cleaner
  9. GWS         → GWS Cleaner
 10. ESF         → ESF Cleaner
 11. APIKEY      → APIKey Cleaner
 12. COOLDOWN    → Cooldown Cleaner
 13. GOOGLE-ACCOUNT     → Google Account Cleaner
 14. GOOGLE-SUSPICIOUS  → Google Suspicious Server Cleaner
 15. TELEGRAM-SUS       → Telegram Suspicious Cleaner
 16. TIKTOK-SUS         → TikTok Suspicious Cleaner
 17. DISCORD-SUS        → Discord Suspicious Cleaner
 18. PINTEREST-SUS      → Pinterest Suspicious Cleaner

{C.GOOGLE_SUS}GOOGLE SUSPICIOUS SERVER — INSTANT CLEANER:{C.RESET}
  accounts.google.com + myaccount.google.com
  Detects: suspicious server / activity / unusual / compromised /
           breach / attack / intrusion / anomaly
  → INSTANT CLEANER DATA on all suspicious paths

{C.SOCIAL_SUS}8 SOCIAL PLATFORM SUSPICIOUS CLEANERS:{C.RESET}
  • Telegram    (telegram.dog + t.me)
  • TikTok      (vm.tiktok.com)
  • Discord     (dgg.gg + discord.gg)
  • Pinterest   (pin.it)
  • WhatsApp    (wa.me + whatsapp.com)
  • Facebook    (fb.com + facebook.com)
  • Instagram   (instagram.com)
  • Twitter     (x.com + twitter.com)
  Detects: suspicious / compromised / breach / attack /
           intrusion / anomaly / banned / session revoked
  → INSTANT CLEANER DATA on all suspicious paths (deep scan)

{C.VPN_SUS}3 VPN SUSPICIOUS CLEANERS:{C.RESET}
  • Free VPN      : Hola / Psiphon / Windscribe / ProtonVPN / Betternet
  • Private VPN   : NordVPN / ExpressVPN / Surfshark / CyberGhost /
                    PrivateVPN / IPVanish / PureVPN / Mullvad
  • Protocol VPN  : OpenVPN / WireGuard / Shadowsocks / V2Ray /
                    SoftEther / VPN Gate
  Detects: suspicious vpn / tunnel anomaly / exit-node compromised /
           breach / attack / cert revoked / key revoked /
           session revoked / banned / blocked

{C.IPBYPASS}ADVANCED IP-BYPASS:{C.RESET}
  • 12 headers rotated: User-Agent, X-Forwarded-For, X-Real-IP,
    Client-IP, X-Originating-IP, X-Remote-IP, X-Remote-Addr,
    Forwarded, X-ProxyUser-Ip, CF-Connecting-IP, True-Client-IP,
    X-Client-IP
  • Proxy chain rotation (--proxy multiple)
  • Tor-mode support (--tor)
  • Prints "[IP-BYPASS] IP Rotated! Using Real IP"
  • Works on web server AND VPN server targets

{C.ROBOT}14 AI ROBOTS AUTOMATED FEATURES:{C.RESET}
  1. Auto-Healing       6. Auto-Detect       11. Auto-Report
  2. Auto-Scaling       7. Auto-Destroy      12. Neural-Network
  3. Auto-Defense       8. Auto-Verify       13. Quantum-Route
  4. Auto-Recovery      9. Auto-Clean        14. Stealth-Mode
  5. Auto-Pivot        10. Auto-Replicate

{C.CLEAN}32-STEP CLEANER PIPELINE:{C.RESET}
  1. Honeypot wall break
  2. Firewall wall break
  3-10. HTTP/HTTPS/Another/Cookies/All/Complete data
 11-15. Movie/Video/Streaming/Image/Series data
 16-19. Language/System/GWS/ESF data
 20-21. APIKey/Cooldown data
 22-24. Google Account / Google Suspicious / Social Suspicious data
 25-27. Telegram/TikTok/Discord social data
 28-30. Pinterest/WhatsApp/Facebook/Instagram/Twitter social data
 31. VPN Suspicious data + tokens
 32. IP-Bypass + API tokens + account + factory

{C.TITAN}THREE DEDICATED INPUT MODES (separate code paths):{C.RESET}
  --url    "https://www.example.com"     → URLModeHandler
  --link   "https://www.example.com/robots.txt" → LinkModeHandler
  --search "https://www.google.com/search?q=" → SearchModeHandler

{C.SAFETY}SAFETY:{C.RESET}
  WEB SERVER ONLY — NOT for local computer
  Local hostnames & private IPs are BLOCKED
  Authorized testing only

{C.ULTIMATE}════════════════════════════════════════════════════════════════════════{C.RESET}
""")


# ============================================
# ARGUMENT PARSER
# ============================================
def parse_arguments():
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=f"{RELEASE_NAME}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )

    g = parser.add_argument_group('Input Mode (choose exactly one)')
    g.add_argument("--url", metavar="URL",
                   help="URL mode: direct URL target")
    g.add_argument("--link", metavar="LINK",
                   help="LINK mode: specific link/endpoint with recursive follow")
    g.add_argument("--search", metavar="SEARCH_URL",
                   help="SEARCH mode: search URL with query placeholder + multi-page crawl")

    g = parser.add_argument_group('Modes')
    g.add_argument("--ultimate", action="store_true")
    g.add_argument("--autonomous", action="store_true")
    g.add_argument("--all", action="store_true")
    g.add_argument("--full", action="store_true")
    g.add_argument("--features", action="store_true")

    g = parser.add_argument_group('Copyright Detection')
    for m in ['detect-copy', 'detect-movie-copy', 'detect-video-copy',
              'detect-streaming-copy', 'detect-image-copy', 'detect-series-copy',
              'detect-lang-copy', 'detect-system-copy', 'detect-gws-copy',
              'detect-esf-copy', 'detect-apikey-copy', 'detect-cooldown-copy',
              'detect-google-account-copy', 'detect-google-suspicious-copy',
              'detect-all-copy']:
        g.add_argument(f"--{m}", action="store_true", dest=m.replace('-', '_'))

    g = parser.add_argument_group('Copyright Clean')
    for m in ['copyright-clean', 'copyright-instant-clean', 'copyright-full-clean',
              'copy-web-clean', 'google-account-clean', 'google-account-full-clean',
              'google-suspicious-clean', 'google-suspicious-full-clean']:
        g.add_argument(f"--{m}", action="store_true", dest=m.replace('-', '_'))

    g = parser.add_argument_group('Social Suspicious Cleaner')
    g.add_argument("--social-suspicious-clean", action="store_true",
                   dest="social_suspicious_clean")
    g.add_argument("--social-suspicious-full-clean", action="store_true",
                   dest="social_suspicious_full_clean")
    g.add_argument("--all-social-suspicious-clean", action="store_true",
                   dest="all_social_suspicious_clean")
    g.add_argument("--platform",
                   choices=['telegram', 'tiktok', 'discord', 'pinterest',
                            'whatsapp', 'facebook', 'instagram', 'twitter'],
                   help="Social platform to clean")

    g = parser.add_argument_group('VPN Suspicious Cleaner')
    g.add_argument("--vpn-suspicious-clean", action="store_true",
                   dest="vpn_suspicious_clean")
    g.add_argument("--vpn-suspicious-full-clean", action="store_true",
                   dest="vpn_suspicious_full_clean")
    g.add_argument("--freevpn-clean", action="store_true", dest="freevpn_clean")
    g.add_argument("--privatevpn-clean", action="store_true", dest="privatevpn_clean")
    g.add_argument("--protocolvpn-clean", action="store_true", dest="protocolvpn_clean")

    g = parser.add_argument_group('IP-Bypass')
    g.add_argument("--ip-bypass", action="store_true", dest="ip_bypass_flag")
    g.add_argument("--tor", action="store_true", dest="tor_mode")

    g = parser.add_argument_group('Cleaner Flags (32 Steps)')
    for m in ['cleaner-data', 'clean-http-cookies', 'clean-https-cookies',
              'clean-another-cookies', 'clean-cookies-data', 'clean-all-cookies',
              'clean-complete-data', 'clean-pipeline', 'verify-clean']:
        g.add_argument(f"--{m}", action="store_true", dest=m.replace('-', '_'))

    g = parser.add_argument_group('14 AI Robots')
    for m in ['ai-robot-all', 'ai-robot-auto', 'auto-heal', 'auto-scale',
              'auto-defend', 'auto-recover', 'auto-clean', 'auto-detect',
              'auto-destroy', 'auto-verify', 'auto-report', 'neural-net',
              'auto-quantum', 'auto-stealth', 'auto-pivot', 'auto-replicate']:
        g.add_argument(f"--{m}", action="store_true", dest=m.replace('-', '_'))

    g = parser.add_argument_group('Recon')
    for m in ['subdomain', 'dns', 'whois', 'ssl', 'headers', 'isp', 'dirbrute',
              'portscan', 'crawl', 'vuln', 'tech-detect', 'secret-scan',
              'cors-scan', 'backup-hunt', 'git-hunt', 'env-hunt',
              'open-redirect', 'lfi', 'ssrf']:
        g.add_argument(f"--{m}", action="store_true", dest=m.replace('-', '_'))

    g = parser.add_argument_group('Destruction')
    for m in ['break-honeypot', 'break-firewall', 'factory-restart',
              'api-attack', 'account-destroy']:
        g.add_argument(f"--{m}", action="store_true", dest=m.replace('-', '_'))

    g = parser.add_argument_group('Performance')
    g.add_argument("-p", "--port", type=int)
    g.add_argument("--timeout", type=int, default=TIMEOUT)
    g.add_argument("--rate-limit", type=int, default=0, dest="rate_limit")
    g.add_argument("--retry", type=int, default=0)
    g.add_argument("--proxy")
    g.add_argument("--stealth", action="store_true")

    g = parser.add_argument_group('Reports')
    g.add_argument("--json-output", action="store_true", dest="json_output")
    g.add_argument("-nb", "--no-banner", action="store_true", dest="no_banner")
    g.add_argument("-h", "--help", action="store_true")
    g.add_argument("--version", action="version", version=f"TITAN_APEX_OMEGA v{VERSION}")

    return parser.parse_args()


# ============================================
# MAIN DISPATCHER
# ============================================
def main():
    try:
        args = parse_arguments()

        if args.features:
            print_features()
            return 0

        if args.help:
            print(BANNER)
            print(f"{RELEASE_NAME}\n")
            print("=" * 70)
            print("THE 3 DEDICATED COMMANDS (fully separate code paths)")
            print("=" * 70)
            print()
            print("  # URL mode")
            print("  python3 titan_apex_omega.py --url https://example.com/ --ultimate --full \\")
            print("    --cleaner-data --clean-http-cookies --clean-https-cookies \\")
            print("    --clean-another-cookies --clean-cookies-data --clean-all-cookies \\")
            print("    --clean-complete-data --autonomous")
            print()
            print("  # LINK mode")
            print('  python3 titan_apex_omega.py --link "https://example.com/robots.txt" --ultimate --full \\')
            print("    --cleaner-data --clean-http-cookies --clean-https-cookies \\")
            print("    --clean-another-cookies --clean-cookies-data --clean-all-cookies \\")
            print("    --clean-complete-data --autonomous")
            print()
            print("  # SEARCH mode")
            print('  python3 titan_apex_omega.py --search "https://www.example.com/search?q=" --ultimate --full \\')
            print("    --cleaner-data --clean-http-cookies --clean-https-cookies \\")
            print("    --clean-another-cookies --clean-cookies-data --clean-all-cookies \\")
            print("    --clean-complete-data --autonomous")
            print()
            print("=" * 70)
            print("Additional commands:")
            print("=" * 70)
            print("  # Google")
            print("  python3 titan_apex_omega.py --url https://accounts.google.com/ --google-account-clean")
            print("  python3 titan_apex_omega.py --url https://accounts.google.com/ --google-suspicious-clean")
            print()
            print("  # Social (8 platforms)")
            print("  python3 titan_apex_omega.py --url https://telegram.dog/ --social-suspicious-clean --platform telegram")
            print("  python3 titan_apex_omega.py --url https://vm.tiktok.com/ --social-suspicious-clean --platform tiktok")
            print("  python3 titan_apex_omega.py --url https://dgg.gg/ --social-suspicious-clean --platform discord")
            print("  python3 titan_apex_omega.py --url https://pin.it/ --social-suspicious-clean --platform pinterest")
            print("  python3 titan_apex_omega.py --url https://wa.me/ --social-suspicious-clean --platform whatsapp")
            print("  python3 titan_apex_omega.py --url https://fb.com/ --social-suspicious-clean --platform facebook")
            print("  python3 titan_apex_omega.py --url https://instagram.com/ --social-suspicious-clean --platform instagram")
            print("  python3 titan_apex_omega.py --url https://x.com/ --social-suspicious-clean --platform twitter")
            print()
            print("  # VPN (3 types)")
            print("  python3 titan_apex_omega.py --url https://nordvpn.com/ --vpn-suspicious-clean")
            print("  python3 titan_apex_omega.py --url https://hola.org/ --freevpn-clean")
            print("  python3 titan_apex_omega.py --url https://openvpn.net/ --protocolvpn-clean")
            print()
            print("  # Advanced IP-Bypass")
            print("  python3 titan_apex_omega.py --url https://example.com/ --ip-bypass")
            print("  python3 titan_apex_omega.py --url https://nordvpn.com/ --ip-bypass --tor")
            print()
            print("  # 14 AI Robots")
            print("  python3 titan_apex_omega.py --url https://example.com/ --ai-robot-all")
            print()
            print("  # Features")
            print("  python3 titan_apex_omega.py --features")
            return 0

        if not args.url and not args.link and not args.search:
            print(BANNER)
            print(f"{RELEASE_NAME}\n")
            print("Quick start (3 dedicated modes):")
            print()
            print("  # URL mode")
            print("  python3 titan_apex_omega.py --url https://example.com/ --ultimate --full \\")
            print("    --cleaner-data --clean-http-cookies --clean-https-cookies \\")
            print("    --clean-another-cookies --clean-cookies-data --clean-all-cookies \\")
            print("    --clean-complete-data --autonomous")
            print()
            print("  # LINK mode")
            print('  python3 titan_apex_omega.py --link "https://example.com/robots.txt" --ultimate --full \\')
            print("    --cleaner-data --clean-http-cookies --clean-https-cookies \\")
            print("    --clean-another-cookies --clean-cookies-data --clean-all-cookies \\")
            print("    --clean-complete-data --autonomous")
            print()
            print("  # SEARCH mode")
            print('  python3 titan_apex_omega.py --search "https://www.example.com/search?q=" --ultimate --full \\')
            print("    --cleaner-data --clean-http-cookies --clean-https-cookies \\")
            print("    --clean-another-cookies --clean-cookies-data --clean-all-cookies \\")
            print("    --clean-complete-data --autonomous")
            print()
            print("Features: python3 titan_apex_omega.py --features")
            print("Help    : python3 titan_apex_omega.py --help")
            return 1

        supplied = []
        if args.url: supplied.append(('url', args.url))
        if args.link: supplied.append(('link', args.link))
        if args.search: supplied.append(('search', args.search))
        if len(supplied) != 1:
            p_err("Only ONE input mode allowed: --url, --link, or --search")
            return 2
        mode, raw = supplied[0]

        if not raw:
            p_err(f"No value for --{mode}")
            return 2
        raw = raw.strip().strip('"').strip("'")
        if not raw:
            p_err(f"Empty value for --{mode}")
            return 2

        # Mode-specific validation
        if mode == 'search':
            if '?' not in raw:
                p_err("--search URL must contain a query placeholder (e.g. ?q=)")
                return 2
            if not raw.startswith(('http://', 'https://')):
                raw = 'https://' + raw

        if mode in ('url', 'link'):
            if not raw.startswith(('http://', 'https://')):
                raw = 'https://' + raw

        parsed = urlparse(raw)
        if not parsed.netloc:
            p_err(f"Invalid {mode}: {raw}")
            return 2

        input_info = {
            'mode': mode, 'raw': raw, 'target_url': raw,
            'protocol': parsed.scheme, 'hostname': parsed.hostname,
            'port': parsed.port, 'path': parsed.path or '/',
            'query': parsed.query,
        }

        bot = TitanApexOmega(input_info, args)

        if not safety_check_web_server_only(bot.hostname):
            p_err("SAFETY FAILED: target is not web server / is local computer")
            return 1

        if not args.no_banner:
            print(BANNER)
            print(f"Input mode : {bot.mode.upper()}")
            print(f"Target     : {bot.target}")
            print(f"Host       : {bot.hostname}")
            print(f"IP         : {bot.ip}")
            print(f"Port       : {bot.port}")
            print(f"Ultimate   : {args.ultimate}")
            print(f"Full       : {args.full}")
            print(f"Autonomous : {args.autonomous}")
            print("=" * 80 + "\n")

        # ---- Standalone flags ----
        if args.ip_bypass_flag:
            bot.ip_bypass()
            bot.export_txt()
            bot.print_summary()
            return 0

        if args.freevpn_clean:
            p_vpn("MODE: --freevpn-clean (Free VPN)")
            bot.ip_bypass()
            bot.vpn.universal_freevpn_clean()
            bot.export_txt()
            bot.print_summary()
            return 0

        if args.privatevpn_clean:
            p_vpn("MODE: --privatevpn-clean (Private VPN)")
            bot.ip_bypass()
            bot.vpn.universal_privatevpn_clean()
            bot.export_txt()
            bot.print_summary()
            return 0

        if args.protocolvpn_clean:
            p_vpn("MODE: --protocolvpn-clean (Protocol VPN)")
            bot.ip_bypass()
            bot.vpn.universal_protocolvpn_clean()
            bot.export_txt()
            bot.print_summary()
            return 0

        if args.vpn_suspicious_clean:
            p_vpn_sus("MODE: --vpn-suspicious-clean (All 3 VPN types)")
            bot.ip_bypass()
            bot.universal_vpn_suspicious_clean()
            bot.export_txt()
            bot.print_summary()
            return 0

        if args.social_suspicious_clean:
            if not args.platform:
                p_err("--social-suspicious-clean requires --platform")
                return 2
            platform_map = {
                'telegram': 'Telegram', 'tiktok': 'TikTok',
                'discord': 'Discord', 'pinterest': 'Pinterest',
                'whatsapp': 'WhatsApp', 'facebook': 'Facebook',
                'instagram': 'Instagram', 'twitter': 'Twitter',
            }
            platform = platform_map[args.platform]
            bot.ip_bypass()
            bot.universal_social_suspicious_clean(platform)
            bot.export_txt()
            bot.print_summary()
            return 0

        if args.all_social_suspicious_clean:
            bot.ip_bypass()
            bot.universal_all_social_suspicious_clean()
            bot.export_txt()
            bot.print_summary()
            return 0

        if args.google_suspicious_clean:
            bot.ip_bypass()
            bot.universal_google_suspicious_clean()
            bot.export_txt()
            bot.print_summary()
            return 0

        if args.google_account_clean:
            bot.ip_bypass()
            bot.universal_google_account_clean()
            bot.export_txt()
            bot.print_summary()
            return 0

        if args.copyright_clean:
            bot.universal_copyright_clean()
            bot.export_txt()
            bot.print_summary()
            return 0

        if args.copyright_instant_clean:
            bot.universal_all_copy_detect()
            bot.export_txt()
            bot.print_summary()
            return 0

        # ---- AI robot standalone ----
        ai_flags_set = any(getattr(args, f, False) for f in [
            'auto_heal', 'auto_scale', 'auto_defend', 'auto_recover',
            'auto_clean', 'auto_detect', 'auto_destroy', 'auto_verify',
            'auto_report', 'neural_net', 'ai_robot_all', 'ai_robot_auto',
            'auto_quantum', 'auto_stealth', 'auto_pivot', 'auto_replicate',
        ])
        if ai_flags_set and not (args.autonomous or args.ultimate or args.full):
            if args.ai_robot_all or args.ai_robot_auto:
                bot.ai_robots.enable_all()
            else:
                for flag, name in [
                    ('auto_heal', 'Auto-Healing'), ('auto_scale', 'Auto-Scaling'),
                    ('auto_defend', 'Auto-Defense'), ('auto_recover', 'Auto-Recovery'),
                    ('auto_clean', 'Auto-Clean'), ('auto_detect', 'Auto-Detect'),
                    ('auto_destroy', 'Auto-Destroy'), ('auto_verify', 'Auto-Verify'),
                    ('auto_report', 'Auto-Report'), ('neural_net', 'Neural-Network'),
                    ('auto_quantum', 'Quantum-Route'), ('auto_stealth', 'Stealth-Mode'),
                    ('auto_pivot', 'Auto-Pivot'), ('auto_replicate', 'Auto-Replicate'),
                ]:
                    if getattr(args, flag, False):
                        bot.ai_robots.enable(name)
            bot.run_ai_robots()
            bot.export_txt()
            bot.print_summary()
            return 0

        # ---- AUTONOMOUS ----
        if args.autonomous:
            bot.run_autonomous()
            return 0

        # ---- ULTIMATE ----
        if args.ultimate:
            bot.run_ultimate()

        # ---- FULL ----
        if args.full:
            bot.run_full_recon()

        # ---- Mode-specific handling (dedicated code paths) ----
        if bot.mode == 'url':
            bot.run_url_mode()
        elif bot.mode == 'link':
            bot.run_link_mode()
        elif bot.mode == 'search':
            bot.run_search_mode()

        # ---- Cleaner pipeline ----
        manual_cleaner = (
            args.cleaner_data or args.clean_http_cookies or
            args.clean_https_cookies or args.clean_another_cookies or
            args.clean_cookies_data or args.clean_all_cookies or
            args.clean_complete_data or args.clean_pipeline
        )
        if manual_cleaner:
            bot.run_clean_pipeline()

        # ---- Destructive ----
        if args.break_honeypot:   bot.break_honeypot_wall()
        if args.break_firewall:   bot.break_firewall_wall()
        if args.factory_restart:  bot.factory_restart()
        if args.api_attack:       bot.api_token_attack()
        if args.account_destroy:  bot.account_action_destroyer()

        bot.export_txt()
        bot.print_summary()
        print(f"\n{C.OKGREEN}[✓] Complete: {bot.target} ({bot.mode.upper()} mode){C.RESET}\n")
        return 0

    except KeyboardInterrupt:
        if _SINGULARITY_MODE:
            p_robot("KeyboardInterrupt absorbed - use kill -9 to force stop")
            return 0
        print(f"\n{C.RED}[-] Interrupted{C.RESET}")
        return 130
    except Exception as e:
        print(f"\n{C.RED}[-] Error: {e}{C.RESET}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
