import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv
import random
import sys
import threading
import time

proxies = []
with open('proxies.txt', mode = 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        proxies.append(row[0])
def fetch_data(count, t) -> int:
    print(count)
    x = requests.get(f"https://phishtank.org/phish_search.php?page={count}&valid=y&Search=Search", proxies={'http': f"http://{t}"})
    if x.status_code != 200:
        print(f"Error: {x.status_code}  {t}")
        return 
    soup = BeautifulSoup(x.content, 'html.parser')
    table = soup.find_all('table', attrs={'class': 'data'})
    if len(table) == 0:
        return 
        pass
    table = table[0]
    table = table.find_all('tr')
    for i in range(1, len(table)):
        row = table[i]
        row = row.find_all('td')
        if row[3].find('strong') == None:
            continue
        x = row[3].find('strong').text
        x1 = row[1].text
        # strip all the white space into a list
        x1 = x1.split()
        with open('15/4/2023.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([x1[0], x])

def main():
    count = 2
    threads = []
    while count < 100000:
        for i in range(5):
            t = proxies[random.randint(0, len(proxies) - 1)]
            t = threading.Thread(target=fetch_data, args=(count, t))
            threads.append(t)
            count += 1
        for t in threads:
            time.sleep(1)
            t.start()
        for t in threads:
            time.sleep(1)
            t.join()
        threads = []
        time.sleep(1)

if __name__ == '__main__':
    main()
