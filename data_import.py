import requests ; from bs4 import BeautifulSoup
import io
import re


file_1 = open('listofurls.txt', 'r' )

for line in file_1:
    s = line
    result = re.search('/movie/(.*)/', s)
    fname = '%s.txt'%result.group(1)
    soup = BeautifulSoup(requests.get(line).text, "html.parser")
    #tags = soup.find_all('p')
    with io.open(fname, "w", encoding="utf-8") as file:
        for p in soup.find_all("div", {"class": "wogma-review"}):
            file.write(p.text)
        for p in soup.find_all("div", {"class": "teho_list"}):
            file.write(p.text)
        for a in soup.find_all("div", {"id": "parental_guidance"}):
            file.write(a.text)
    
    file.close() 

file_1.close()