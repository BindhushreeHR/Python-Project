import urllib.request,urllib.parse, urllib.error 
from bs4 import BeautifulSoup 
import ssl
import re
globalist=[]
l={}
stocktags=[]
def part1_extract(rows,globalist):
  i=0
  temp=""
  while(i!=len(rows)):
    tick= rows[i].text.split(" ")[0]
  #print(rows[i].text.split(" ")[1:])
    for j in rows[i].text.split(" ")[1:]:
      temp+=j+" "
      element=[]
      element.append((temp))
    l=dict({tick:element})
    #print(l)
    globalist.append(l)
    #print(tick)
    #print(temp)
    temp=""
    i=i+4
  #print(globalist)  

def part2_extract(anchor,ctx):
  links=[]
  plist=[]
  for a in anchor:
    links.append('https://money.cnn.com/'+a.get('href'))
  for l in links:
    key=(l.split("=")[1])
    html = urllib.request.urlopen(l, context=ctx).read()
    soup1 = BeautifulSoup(html, 'html.parser')
    tdata = soup1.findAll("div", {"class": "clearfix wsod_DataColumnLeft"})  
    children = tdata[0].findChildren("td" , recursive=True)
    i=0
    while(i<11):
      if children[i].text=="Previous close":
        #print(children[i].text+children[i+1].text)
        pc=children[i+1].text
      if children[i].text=="Today’s open":
       # print(children[i].text+children[i+1].text)
        to=children[i+1].text
      if children[i].text=="Volume":
        #print(children[i].text+children[i+1].text)
        vol=children[i+1].text
      if children[i].text=="Market cap":
       # print(children[i].text+children[i+1].text)
        mc=children[i+1].text
      i=i+1        
    for j in globalist:
        if j.get(key)!=None:
          j.get(key).append(pc)
          j.get(key).append(to)
          j.get(key).append(vol)
          j.get(key).append(mc)
          #print(j.get(key))
def main():
  global globalist
  global l
  global stocktags
  ctx=ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  url = input('Enter - ')
  html = urllib.request.urlopen("https://money.cnn.com/data/hotstocks/", context=ctx).read()
  soup1 = BeautifulSoup(html, 'html.parser')
  divs = soup1.findAll("table", {"class": "wsod_dataTableBigAlt"})  

#Stock Tag info 
  headers=soup1.findAll("h3", {"class":""}) 
  for h in headers:
    stocktags.append(h.text)
#for div in divs:

  for table in divs:
    row = ''
    rows= table.findAll('td')
    part1_extract(rows,globalist)
  #print(globalist)  
  #print(stocktags)  

  for table in divs:
    row = ''  
    anchor=table.findAll('a')
    #part2_extract(anchor,ctx)
  #print(globalist)  
  #print(stocktags)



  #list.append()
# MetaData  

main()
