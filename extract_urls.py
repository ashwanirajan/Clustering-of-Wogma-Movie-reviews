from lxml import html
import requests


i=1
prefix='review_'
#save_path='D:\Unfound'

def getallurls():
   f=open('listofurls.txt', 'w')
   begin_url = 'http://wogma.com'
   page=requests.get('http://wogma.com/movies/basic/')
   tree=html.fromstring(page.text)
   reviews=tree.xpath('//div[@class="button related_pages review "]/a/@href')
   for review in reviews:
       f.write(begin_url+str(review)+'\n')
   f.close()
   
   
getallurls()