import requests ; from bs4 import BeautifulSoup
import io


file_1 = open('listofurls.txt', 'r' )
i = 0
for line in file_1:
    i +=1
    soup = BeautifulSoup(requests.get(line).text, "html.parser")
    tags = soup.find_all('p')
    fname = 'sample%d.txt'%i
    with io.open(fname, "w", encoding="utf-8") as file:
        for p in tags:
            file.write(p.text)
    
        for a in soup.find_all("div", {"id": "parental_guidance"}):
            file.write(a.text)
    
    file.close() 

file_1.close()