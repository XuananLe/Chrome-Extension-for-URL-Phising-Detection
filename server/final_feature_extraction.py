import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
import requests
from googlesearch import search
import whois
import random
import requests
import networkx as nx
import hashlib
import networkx as nx
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import time
from dateutil.parser import parse as date_parse
from urllib.parse import urlparse
import threading
import concurrent.futures
from urllib.parse import urlparse
import csv
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from urllib.parse import urlparse
import csv
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import numpy as np
import pandas as pd
import pickle
import urllib
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
import ipaddress
import ssl
from urllib.parse import urlparse
import re
import requests
import json
import time
import threading
import random
import socket
import ssl
import math
from datetime import datetime
import sys
from concurrent.futures import ThreadPoolExecutor
import asyncio
import socket
import re
import aiohttp
import aiodns
import whois
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import tldextract
import os
import aiohttp
import time
import concurrent.futures
import difflib
import redis 
'''
-1 mean phishing, 0 mean suspicious, 1 mean legitimate
'''
client = redis.Redis(host='localhost', port=6379, decode_responses=True)

with open('/home/xuananle/Documents/Chrome_Extension/core/ML-core-test/test.txt', 'r') as f:
    chrome_warning_contents = f.read()


async def contains_IP_address(url, socurce_code, soup, whois_response):
    domain = urlparse(url).hostname
    try:
        ip_address = socket.gethostbyname(domain)
    except:
        return -1
    if ip_address in domain:
        return -1
    else:
        return 1


async def UrlLength(url, source_code, soup, whois_response):
    if (len(url) < 54):
        return 1
    elif (len(url) >= 54 and len(url) <= 75):
        return 0
    return -1


shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"


async def TinyURL(url, source_code, soup, whois_response):
    match = re.search(shortening_services, url)
    if match:
        return -1
    return 1


async def Have_At(url, source_code, soup, whois_response):
    if ('@' in url):
        return -1
    return 1


async def redirection(url, source_code, soup, whois_response):
    if (url.rfind('//') > 6):
        return -1
    return 1


async def PrefixSuffix(url, source_code, soup, whois_response):
    if ('-' in url):
        return -1
    return 1


async def subDomains(url, source_code, soup, whois_response):
    x = tldextract.extract(url).subdomain + "." + tldextract.extract(url).domain
    if(x.count('.') == 1):
      return 1
    elif (x.count('.') == 2):
      return 0
    else:
      return -1


async def HTTPS(url, source_code, soup, whois_response):
    if (url.startswith('https')):
        return 1
    return -1


async def Domain_Registration_Len(url, source_code, soup, whois_response):
    try:
        expiration_date = whois_response.expiration_date
        creation_date = whois_response.creation_date
        try:
            if (len(expiration_date)):
                expiration_date = expiration_date[0]
        except:
            return -1
        try:
            if (len(creation_date)):
                creation_date = creation_date[0]
        except:
            return -1
        age = (expiration_date.year - creation_date.year)
        if (age >= 12):
            return 1
        return -1
    except:
        print("Error at the Domain_Registration_Len")
        return -1


   

async def Favicon(url, source_code, soup, whois_response):
    try:
        x = url
        x = tldextract.extract(x).subdomain + "." + tldextract.extract(x).domain
        if(x.endswith('/')):
            x = requests.get(x + '/favicon.ico')
        else :
            x = requests.get(x + 'favicon.ico')
        if (x.status_code == 200):
            return 1
        a = soup.find_all('link', rel='shortcut icon')
        if(len(a) !=  0):
            return 1
        return -1
    except:
        print("Error at has_favicon")
        return -1


async def nonStdPort(url, source_code, soup, whois_response):
    try:
        port = urlparse(url).port
        if (port):
            if (port == 80 or port == 443):
                return 1
            else:
                return -1
        else:
            return 1
    except:
        return -1


async def HTTPSDomain(url, source_code, soup, whois_response):
    try:
        domain = urlparse(url).netloc.lower()
        if("https" in domain):
            return -1
        else:
            return 1
    except:
        print("Error at HTTPSDomain")
        return -1


async def RequestURL(url, source_code, soup, whois_response):
    try:
        urls = []
        urls += [img['src'] for img in soup.find_all('img', src=True)]
        urls += [audio['src'] for audio in soup.find_all('audio', src=True)]
        urls += [embed['src'] for embed in soup.find_all('embed', src=True)]
        urls += [iframe['src'] for iframe in soup.find_all('iframe', src=True)]
        num_urls = len(urls)
        num_external_urls = 0

        for url in urls:
            parsed_url = urlparse(url)
            if parsed_url.netloc != urlparse(url).netloc:
                num_external_urls += 1

        percentage_external = num_external_urls / num_urls * 100
        if percentage_external < 22:
            return 1
        elif percentage_external < 61:
            return 0
        else:
            return -1

    except:
        return -1


async def AnchorURL(url, source_code, soup, whois_response):
    try:
        urls = [a['href'] for a in soup.find_all('a', href=True)]
        num_urls = len(urls)
        num_external_urls = 0

        for url in urls:
            if url.startswith('#') or url.lower().startswith('javascript') or url.lower().startswith('mailto'):
                continue
            parsed_url = urlparse(url)
            if parsed_url.netloc != urlparse(url).netloc:
                num_external_urls += 1

        percentage_external = num_external_urls / num_urls * 100
        if percentage_external < 31:
            return 1
        elif percentage_external < 67:
            return 0
        else:
            return -1

    except:
        print("Error at AnchorURL")
        return -1


async def LinksInScriptTags(url, source_code, soup, whois_response):
    try:
        url_parse = urlparse(url)
        domain = url_parse.netloc
        metas = soup.find_all('meta')
        scripts = soup.find_all('script')
        links = soup.find_all('link')

        meta_count = 0
        script_count = 0
        link_count = 0
        total_count = 0

        for meta in metas:
            if 'http-equiv' in meta.attrs:
                if domain in meta.attrs['content']:
                    meta_count += 1
            elif 'name' in meta.attrs:
                if domain in meta.attrs['content']:
                    meta_count += 1

        for script in scripts:
            if 'src' in script.attrs:
                if domain in script.attrs['src']:
                    script_count += 1

        for link in links:
            if 'href' in link.attrs:
                if domain in link.attrs['href']:
                    link_count += 1

        total_count = meta_count + script_count + link_count

        percent_links = (total_count / len(soup.find_all())) * 100

        if percent_links < 17:
            return 1
        elif percent_links >= 17 and percent_links <= 81:
            return 0
        else:
            return -1
    except:
        return -1


async def ServerFormHandler(url, source_code, soup, whois_response):
    try:
        forms = soup.find_all('form')
        if not forms:
            return 1
        for form in forms:
            if form.has_attr('action') and (form['action'] == 'about:blank' or form['action'] == ''):
                return -1
            elif form.has_attr('action'):
                parsed_url = urlparse(form['action'])
                domain_name = parsed_url.hostname
                if domain_name and domain_name != urlparse(url).hostname:
                    return 0
        return 1
    except:
        return -1


async def InfoEmail(url, source_code, soup, whois_response):
    try:
        elements = soup.find_all(lambda tag: (tag.name == 'a' or tag.name == 'button') and tag.has_attr('href') and tag['href'].startswith('mailto:'))
        for element in elements:
            return -1
        return 1
    except:
        print("Error at InfoEmail")
        return -1


async def AbnormalURL(url, source_code, soup, whois_response):
    try:
        whois_response = whois_response.text

        if whois_response and 'Domain Name' in whois_response:
            return 1
        else:
            return -1
    except:
        return -1


async def WebsiteForwarding(url, source_code, soup, whois_response):
    try:
        response = requests.get(url, allow_redirects=False, timeout=3)
        count = 0
        while 300 <= response.status_code < 400:
            count += 1
            location = response.headers['location']
            response = requests.get(location, allow_redirects=False, timeout=3)
        if count <= 1:
            return 0 # Legitimate
        elif 2 <= count < 4:
            return 1 # Suspicious
        else:
            return -1 # Phishing
    except:
        print("Error at WebsiteForwarding")
        return -1

async def StatusBarCustomization(url, source_code, soup, whois_response):
    try:
        if (re.search("<script>.+onmouseover.+</script>", source_code)):
            return -1
        else:
            return 1
    except:
        print("Error at the StatusBarCustomization")
        return -1

async def DisablingRightClick(url, source_code, soup, whois_response):    
    try:
        elements = soup.find_all(lambda tag: tag.has_attr('onmousedown'))
        for element in elements:
            event_str = element['onmousedown']
            if(re.search(r'event\.button\s*==\s*2', event_str)):
                return -1
        return 1
    except:
        print("Error at DisablingRightClick")
        return -1

async def UsingPopupWindow(url, source_code, soup, whois_response):
    try:
        if (re.findall(r"alert\(", str(soup)) == 0):
            return -1
        else:
            return 1
    except:
        print("Error at UsingPopupWindow")
        return -1    

async def IframeRedirection(url, source_code, soup, whois_response):
    try:
        if (re.findall(r"[<iframe> | <frameBoder>]", str(soup))):
            return 1
        else:
            return -1
    except:
        print("Error in IframeRedirection")
        return -1

async def AgeOfDomain(url, source_code, soup, whois_response):
    try:
        creation_date = whois_response.creation_date
        try:
            if (len(creation_date)):
                creation_date = creation_date[0]
        except:
            print("Error in AgeOfDomain")
            return -1
        today = date.today()
        age = (today.year - creation_date.year)
        if (age >= 6):
            return 1
        return -1
    except:
        print("Error in AgeOfDomain")
        return -1

async def DNS_Recording(url, source_code, soup, whois_response):
    try:
        if(whois_response.status is None):
            return -1
        else :
            return 1    
    except:
        print("Error at DNS_Recording")
        return -1

async def websiteTraffic(url, source_code, soup, whois_response):
    return 1

async def pageRank(url, source_code, soup, whois_response):
    try:
        links = soup.find_all('a')

        G = nx.DiGraph()
        for link in links:
            href = link.get('href')
            if href:
                if href.startswith('https'):
                    G.add_edge(url, href)
                else:
                    G.add_edge(url, url + href)

        pr = nx.pagerank(G, alpha=0.9)
        if(pr[url] > 0.02):
            return 1
        else:
            return  -1

    except:
        print("Error in page_rank")
        return -1

async def GoogleIndex(url, source_code, soup, whois_response):
    try:
        site = search(url, 5)
        print("the site is" , site)
        if (site):
            return 1
        else:
            return -1
    except:
        print("Error in GoogleIndex")
        return -1


async def LinksPointingToPage(url, source_code, soup, whois_response):
    try:
        num_of_links = len(soup.find_all(r"<a href=", soup))
        if (num_of_links == 0):
            return 1
        elif num_of_links <= 2:
            return 0
        else:
            return -1
    except:
        print("Error in LinksPointingToPage")
        return -1


async def StatsReport(url, source_code, soup, whois_response):
    try:
        url = urlparse(url)
        domain_name = url.hostname
        url_match = re.search(
            'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly', domain_name)
        ip_address = socket.gethostbyname(domain_name)
        ip_match = re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                             '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                             '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                             '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                             '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                             '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42', ip_address)
        if url_match:
            return -1
        elif ip_match:
            return -1
        return 1
    except:
        print("Error in StatsReport")
        return -1


# list all the function name
funcs = [contains_IP_address, UrlLength, TinyURL, Have_At, 
        redirection, PrefixSuffix, subDomains, HTTPS, Domain_Registration_Len, Favicon, nonStdPort, HTTPSDomain,
        RequestURL,AnchorURL, LinksInScriptTags, ServerFormHandler,
        InfoEmail, AbnormalURL, WebsiteForwarding, StatusBarCustomization,DisablingRightClick , UsingPopupWindow,
        IframeRedirection, AgeOfDomain,DNS_Recording,  websiteTraffic, pageRank, GoogleIndex, LinksPointingToPage, StatsReport]
feature_names = ['contains_IP_address', ' UrlLength', ' TinyURL', ' Have_At',
       ' redirection', ' PrefixSuffix', ' subDomains', ' HTTPS',
       ' Domain_Registration_Len', ' Favicon', ' nonStdPort', ' HTTPSDomain',
       'RequestURL', 'AnchorURL', ' LinksInScriptTags', ' ServerFormHandler',
       'InfoEmail', ' AbnormalURL', ' WebsiteForwarding',
       ' StatusBarCustomization', 'DisablingRightClick ', ' UsingPopupWindow',
       'IframeRedirection', ' AgeOfDomain', 'DNS_Recording',
       '  websiteTraffic', ' pageRank', ' GoogleIndex', ' LinksPointingToPage',
       ' StatsReport']

async def run_whois(url):
    return whois.whois(url)
async def extract_features(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            x = time.time()
            source_code = await response.text()
            print(f"the get request takes {time.time() - x}")
        
        soup = BeautifulSoup(source_code, 'html.parser')
        x1 = time.time()
        whois_time = time.time()
        whois_response = await run_whois(url)
        print(f"the whois process takes {time.time() - whois_time}")
        
        features = []
        tasks = [func(url, source_code, soup, whois_response) for func in funcs]
        start_time = time.monotonic()        
        results = await asyncio.gather(*tasks)
        for i, result in enumerate(results):
            features.append(result)
            print(f"{funcs[i]} took {time.monotonic()-start_time} seconds to complete.")
            print(f"{funcs[i]}: {result}")
        return features

model = pickle.load(open("model.pkl", "rb"))

black_list = redis.Redis(host='localhost', port=6379, decode_responses=True, db = 0)
white_list = redis.Redis(host='localhost', port=6379, decode_responses=True, db = 1)

async def predict(url):
    try:
        response = requests.get(url, timeout= 3)
    except:
        print("Cannot connect to the website")
        return -1
    
    if(response.status_code >= 400):
        print("the link is not valid")
        return -1
    
    if(black_list.sismember("black_list", url) == True):
        print("The url is in the black list")
        return -1
    #move top level domain to the end
    new_url = tldextract.extract(url).domain + "." + tldextract.extract(url).suffix
    print(new_url)
    sys.exit(1)
    if(white_list.sismember("white_list", new_url) == True):
        print("The url is in the white list")
        return 1
    
    content_type = response.headers.get("content-type")
    if "charset" in content_type:
        encoding = content_type.split("charset=")[-1]
        content = response.content.decode(encoding)
    else:
        content = response.content
        
    matcher = difflib.SequenceMatcher(None, chrome_warning_contents, content)
    ratio = matcher.ratio()
    print("the ratio is: ", ratio)
    if(ratio >= 0.9):
        return -1
    
    features = await extract_features(url)
    # First condition 
    if(features[5] + features[8] + features[23] == -3):
        return -1
    
    features = np.array(features).reshape(1, -1)
    features = pd.DataFrame(features, columns=feature_names)
    probabilities = model.predict_proba(features)    
    return probabilities[0][1]

def main(url):
    s = asyncio.run(predict(url))
    print("I am predicting  ", url)
    print("The result is: ", s)
    return s
