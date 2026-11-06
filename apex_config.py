#!/usr/bin/env python3
"""apex_config.py - All wordlists, signatures, and paths for TITAN_APEX_OMEGA"""

VERSION = "17000.0"
BUILD_NUMBER = "17000.001"
DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443
TIMEOUT = 5
REQ_HEADERS = {"User-Agent": "Mozilla/5.0 (Titan-Apex-Omega/17000)"}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
]

CONFIG = {
    'timeout': TIMEOUT,
    'export_dir': 'titan_apex_omega-results',
    'checkpoint_file': 'titan_apex_omega-results/checkpoint.json',
    'diff_file': 'titan_apex_omega-results/last_scan.json',
}

COMMON_SUBS = ["www","mail","ftp","webmail","smtp","pop","ns1","ns2","dev","test",
    "staging","api","admin","portal","blog","shop","cdn","static","media","app",
    "mobile","vpn","git","gitlab","jenkins","ci","db","mysql","postgres","ns","m",
    "imap","pop3","forum","news","old","support","docs","beta","secure","demo",
    "web","email","images","download","dns","intranet","jira","nexus",
    "accounts","myaccount","login","auth","oauth","signin",
    "telegram","tiktok","discord","pinterest","whatsapp","facebook","instagram","twitter",
    "vpn","freevpn","privatevpn"]

COMMON_DIRS = ["admin","login","wp-admin","wp-login","backup","backups","bak","old",
    "config","configuration","settings","setup","install","db","database","sql",
    "mysql","phpmyadmin","adminer","test","tests","dev","stage","staging","private",
    "secret","internal","hidden","secure","uploads","upload","files","media","images",
    "img","js","css","assets","static","public","dist","docs","documentation","help",
    "support","faq","user","users","account","profiles","log","logs","error","debug",
    ".git",".git/config",".env",".htaccess","robots.txt","sitemap.xml","server-status",
    "server-info","phpinfo.php","info.php","web.config","cgi-bin","bin","scripts",
    "cron","jobs","portal","console","manager","management","control","auth","oauth",
    "sso","saml","ldap","login.php","signin","register","signup","password","invoice",
    "order","cart","checkout","payment","billing","api","api/v1","api/v2","graphql",
    "rest","honeypot","honey","trap","decoy","cleaner","factory-restart","tokens",
    "token","devices","device","suspicious","security/alert","system/suspicious",
    "telegram","tiktok","discord","pinterest","vpn","freevpn","privatevpn"]

COMMON_PORTS = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",
    110:"POP3",143:"IMAP",443:"HTTPS",445:"SMB",993:"IMAPS",995:"POP3S",
    1194:"OpenVPN",1433:"MSSQL",1521:"Oracle",1723:"PPTP",2049:"NFS",
    2082:"cPanel",2083:"cPanel-SSL",2181:"Zookeeper",2375:"Docker",3000:"Node",
    3306:"MySQL",3389:"RDP",4443:"HTTPS-Alt",5000:"App",51820:"WireGuard",
    5432:"PostgreSQL",5601:"Kibana",5672:"RabbitMQ",5900:"VNC",6379:"Redis",
    6443:"K8s-API",7001:"WebLogic",8000:"HTTP-Alt",8080:"HTTP-Proxy",
    8081:"HTTP-Alt2",8443:"HTTPS-Alt2",8888:"HTTP-Alt3",9000:"App",
    9090:"Prometheus",9200:"Elasticsearch",9300:"ES-Transport",
    10000:"Webmin",11211:"Memcached",15672:"RabbitMQ-Mgmt",
    27017:"MongoDB",27018:"MongoDB-2",50000:"SAP",50051:"gRPC"}

TECH_SIGNATURES = {
    'WordPress':['wp-content','wp-includes','wp-json'],'Joomla':['joomla','/components/com_'],
    'Drupal':['drupal','/sites/default/'],'Magento':['magento','/skin/frontend/'],
    'Shopify':['shopify','cdn.shopify.com'],'Laravel':['laravel_session','XSRF-TOKEN'],
    'Django':['csrftoken','django'],'Rails':['_rails','phusion'],'Express':['X-Powered-By: Express'],
    'Nginx':['nginx'],'Apache':['apache'],'IIS':['iis','Microsoft-IIS'],'Tomcat':['tomcat','coyote'],
    'Cloudflare':['cloudflare','cf-ray'],'React':['react','_reactRootContainer'],
    'Vue.js':['vue.js','v-cloak','__vue__'],'Angular':['ng-version','angular'],
    'jQuery':['jquery'],'Bootstrap':['bootstrap'],'PHP':['X-Powered-By: PHP','PHPSESSID'],
    'ASP.NET':['ASP.NET','__VIEWSTATE'],'Node.js':['X-Powered-By: Express','node'],
    'Python':['X-Powered-By: Python','gunicorn'],'Java':['JSESSIONID','X-Powered-By: Servlet'],
    'Google Sign-In':['accounts.google.com','gsi/client','google-signin'],
    'Google OAuth':['oauth2.googleapis.com','accounts.google.com/o/oauth2'],
    'Telegram':['telegram.org','telegram.dog','t.me','tgme','telegram-widget'],
    'TikTok':['tiktok.com','vm.tiktok.com','tiktokcdn','ttwstatic'],
    'Discord':['discord.com','discord.gg','dgg.gg','discordapp','discord-cdn'],
    'Pinterest':['pinterest.com','pin.it','pinimg','pinterest-widget'],
    'WhatsApp':['wa.me','whatsapp.com','whatsapp.net'],
    'Facebook':['facebook.com','fb.com','fbcdn.net'],
    'Instagram':['instagram.com','cdninstagram.com'],
    'Twitter':['twitter.com','x.com','t.co'],
    'OpenVPN':['openvpn','openvpn-server','openvpn-as','pritunl'],
    'WireGuard':['wireguard','wg-easy','wg-gen-web'],
    'NordVPN':['nordvpn','nordvpn.com','nordcdn'],
    'ExpressVPN':['expressvpn','expressvpn.com'],
    'ProtonVPN':['protonvpn','protonvpn.com'],
    'Surfshark':['surfshark','surfshark.com'],
    'CyberGhost':['cyberghost','cyberghostvpn.com'],
    'PrivateVPN':['privatevpn','privatevpn.com'],
    'IPVanish':['ipvanish','ipvanish.com'],
    'PureVPN':['purevpn','purevpn.com'],
    'Mullvad':['mullvad','mullvad.net'],
    'Windscribe':['windscribe','windscribe.com'],
    'Hotspot Shield':['hotspotshield','hotspotshield.com'],
    'Hola VPN':['hola.org','holavpn'],
    'Psiphon':['psiphon','psiphon3','psiphon.ca'],
    'Shadowsocks':['shadowsocks','ss-local','ss-server'],
    'V2Ray':['v2ray','v2ray-core','v2fly'],
}

SECRET_PATTERNS = {
    'AWS Access Key':r'AKIA[0-9A-Z]{16}',
    'AWS Secret':r'(?i)aws.{0,20}?[\'"][0-9a-zA-Z/+]{40}[\'"]',
    'Google API':r'AIza[0-9A-Za-z\-_]{35}','GitHub Token':r'gh[pousr]_[A-Za-z0-9_]{36,}',
    'Slack Token':r'xox[baprs]-[0-9a-zA-Z\-]{10,}','Stripe Key':r'sk_live_[0-9a-zA-Z]{24,}',
    'JWT Token':r'eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+',
    'Private Key':r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
    'Generic API Key':r'(?i)(api[_-]?key|apikey)[\'"]?\s*[:=]\s*[\'"]([a-zA-Z0-9\-_.]{20,})[\'"]',
    'Bearer Token':r'(?i)bearer\s+[a-zA-Z0-9\-_.=]{20,}',
    'Basic Auth':r'(?i)authorization:\s*basic\s+[a-zA-Z0-9+/=]{20,}',
    'Password Field':r'(?i)password[\'"]?\s*[:=]\s*[\'"][^\'"]{8,}[\'"]',
    'Telegram Bot Token':r'\d{8,10}:[A-Za-z0-9_-]{35}',
    'TikTok Session':r'(?i)tiktok.{0,20}?sessionid[\'"]?\s*[:=]\s*[\'"]([A-Za-z0-9]{20,})[\'"]',
    'Discord Token':r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}',
    'Pinterest Token':r'(?i)pinterest.{0,20}?(token|key)[\'"]?\s*[:=]\s*[\'"]([A-Za-z0-9]{20,})[\'"]',
    'VPN Key':r'(?i)(vpn|wireguard|openvpn).{0,20}?(key|secret|token)[\'"]?\s*[:=]\s*[\'"]([A-Za-z0-9+/=_-]{20,})[\'"]',
    'WireGuard Private Key':r'-----BEGIN WIREGUARD PRIVATE KEY-----',
    'OpenVPN Cert':r'-----BEGIN CERTIFICATE-----',
}

CORS_TEST_ORIGINS = ['https://evil.com','null','https://attacker.example']
HTTP_METHODS = ['GET','POST','PUT','DELETE','OPTIONS','PATCH','HEAD','TRACE','CONNECT']
BACKUP_EXTS = ['.bak','.old','.backup','.zip','.tar','.tar.gz','.tgz','.rar','.7z',
    '.sql','.sql.gz','.dump','.swp','~','.orig','.save']

# ... (all other signature blocks from v16000: COPYRIGHT_*, MOVIE_*, VIDEO_*,
#      STREAMING_*, SERIES_*, IMAGE_*, PROGRAMMING_LANGUAGE_*, WEB_SERVER_*,
#      GWS_*, ESF_*, GOOGLE_*, SOCIAL_*, VPN_*, API_KEY_*, COOLDOWN_*,
#      FRAMEWORK_*, CLEANER_*, HONEYPOT_*, FIREWALL_*, API_TOKEN_TARGETS,
#      FACTORY_PATTERNS, ACCOUNT_ACTION_PATTERNS)
# ── Copy the exact same blocks from v16000 here ──
# (They are unchanged; see previous file content for the full dict values.)
