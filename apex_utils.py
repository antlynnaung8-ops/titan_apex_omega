#!/usr/bin/env python3
"""apex_utils.py - Shared print helpers"""


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
