import subprocess
import requests
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "X-XSS-Protection",
    "Referrer-Policy",
    "Permissions-Policy",
    "Cross-Origin-Resource-Policy",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Opener-Policy"
]

def get_raw_headers(url):
    try:
        print("\n[+] Raw HTTP Response Headers")
        print(f"[+] curl -I {url}:\n")
        result = subprocess.run(["curl", "-I", "-s", url], capture_output=True, text=True)
        print(result.stdout.strip())
        return result.stdout
    except Exception as e:
        print(f"[!] Error fetching raw headers: {e}")
        return ""

def check_security_headers(response):
    print("\n[+] Present Security Headers:")
    present = False
    for header in SECURITY_HEADERS:
        if header in response.headers:
            print(f"   - {header}: {response.headers[header]}")
            present = True
    if not present:
        print("   - None")

    print("\n[-] Missing Security Headers:")
    for header in SECURITY_HEADERS:
        if header not in response.headers:
            print(f"   - {header}")

def get_options_output(url):
    try:
        print(f"\n[+] curl -X OPTIONS {url}:\n")
        result = subprocess.run(["curl", "-X", "OPTIONS", "-i", "-s", url], capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        for line in lines:
            if line.startswith("HTTP/"):
                print(line)
        for line in lines:
            if line.lower().startswith("allow:"):
                print(line)
                return
        print("Method not allowed (No 'Allow' header found)")
    except Exception as e:
        print(f"[!] Error checking OPTIONS method: {e}")

def verify_methods(url):
    common_methods = [
        "GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "PATCH",
        "TRACE", "CONNECT", "PROPFIND", "PROPPATCH", "MKCOL",
        "COPY", "MOVE", "LOCK", "UNLOCK", "SEARCH", "BIND", "REBIND",
        "UNBIND", "ACL", "REPORT", "MKACTIVITY", "CHECKOUT", "MERGE",
        "M-SEARCH", "NOTIFY", "SUBSCRIBE", "UNSUBSCRIBE", "PURGE",
        "LINK", "UNLINK", "VIEW", "DEBUG"
    ]

    actually_allowed = []

    for method in common_methods:
        if method in [
            "POST", "PUT", "PATCH", "DELETE", "PROPPATCH", "MKCOL", "COPY", "MOVE",
            "LOCK", "UNLOCK", "REPORT", "MKACTIVITY", "CHECKOUT", "MERGE",
            "SUBSCRIBE", "UNSUBSCRIBE", "PURGE", "LINK", "UNLINK", "BIND",
            "REBIND", "UNBIND"
        ]:
            cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", method, "-d", "test=data", url]
        else:
            cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", method, "-I", url]

        try:
            resp = subprocess.run(cmd, capture_output=True, text=True)
            status_code = resp.stdout.strip()
            if status_code.startswith(("2", "3")):
                actually_allowed.append(method)
        except Exception:
            pass

    return actually_allowed

def main():
    url = input("Enter the URL (e.g. https://example.com): ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    print(f"\n[+] Fetching security headers for: {url}")

    try:
        response = requests.get(url, verify=False, timeout=10)
        raw_headers = get_raw_headers(url)
        check_security_headers(response)
        get_options_output(url)

        allowed = verify_methods(url)
        if allowed:
            print("\n[+] Actually Allowed HTTP Methods:")
            for m in allowed:
                print(f"   - {m}")
        else:
            print("\n[-] No HTTP methods allowed (based on live testing).")
    except requests.exceptions.RequestException as e:
        print(f"\n[!] Error: {e}")

if __name__ == "__main__":
    main()