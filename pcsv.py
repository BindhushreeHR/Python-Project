import csv
import urllib.request,urllib.parse, urllib.error 
from bs4 import BeautifulSoup 
import ssl
import re
import sys
globalist=[]
csvtuple=[]
l={}
stocktags=[]
def part1_extract(rows,globalist):
  i=0
  temp=""
  while(i!=len(rows)):
    tick= rows[i].text.split(" ")[0]
    for j in rows[i].text.split(" ")[1:]:
      temp+=j+" "
      element=[]
      element.append((temp))
    l=dict({tick:element})
    globalist.append(l)
    temp=""
    i=i+4

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
        pc=children[i+1].text
      if children[i].text=="Today’s open":
        to=children[i+1].text
      if children[i].text=="Volume":
        vol=children[i+1].text
      if children[i].text=="Market cap":
        mc=children[i+1].text
      i=i+1        
    for j in globalist:
        if j.get(key)!=None:
          j.get(key).append(pc)
          j.get(key).append(to)
          j.get(key).append(vol)
          j.get(key).append(mc)
def user_input():
	print("\nEnter valid Stock ticker from list OR  press E to exit anytime")
	user_iptick=input()
	if (user_iptick == 'E'):
		print('see user_stock.csv file for your stock entries')
		print('see stocks.csv file for all stock  entries')
		print("Good Bye")
	else:
		print("\nUser inputs : "+user_iptick+"\n")
		user_iptick=user_iptick.replace(" ","")
		user_iptick=user_iptick.lower()
		stock_record=None
		index=0
		for i in globalist:
			if(i.get(user_iptick.upper()))!=None:
				stock_record=i.get(user_iptick.upper())
				index=globalist.index(i)
				break
		if stock_record!=None:
			print(user_iptick.upper()+" "+stock_record[0])
			print("OPEN: "+stock_record[1])
			print("PREV CLOSE: "+stock_record[2])
			print("VOLUME: "+stock_record[3])
			print("MARKET CAP: "+stock_record[4])
			if(index<=9):
				tag="Most Actives"
			if(index>9 and index <=19):	
				tag="Gainers"
			if(index>19):	
				tag="Losers" 
			with open('user_stock.csv', 'a',newline='') as csvfile:
				names  = ['Category','Ticker_Sym','Stock Name', 'Open','Prev Close','Volume','Market Cap']
				writer = csv.DictWriter(csvfile,fieldnames=names)
				writer.writerow({'Category':tag,'Ticker_Sym':user_iptick.upper(),'Stock Name':stock_record[0],'Open': stock_record[1],'Prev Close':stock_record[2],'Volume':stock_record[3],'Market Cap':stock_record[4]})
				user_input()
		else:
			user_input()


def user_menu():
	global globalist
	print(" \n This is a program to scrape data from the https://money.cnn.com/data/hotstocks/  for a class project \n") 
	print("Which stock are you interested in: ")
	count=0;
	for item in globalist:
		if(count==0 or count==10 or count==20):
			print ("\n")
			print (stocktags[int(count/10)])
		count=count+1
		for k,v in item.items():
			print(k+" "+ v[0])	
	user_input()

 
def main():
  global globalist
  global l
  global stocktags
  ctx=ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  print("..........")
  html = urllib.request.urlopen("https://money.cnn.com/data/hotstocks/", context=ctx).read()
  soup1 = BeautifulSoup(html, 'html.parser')
  divs = soup1.findAll("table", {"class": "wsod_dataTableBigAlt"})  
  print("Getting information from https://money.cnn.com/data/hotstocks/")
  print("..........")
  headers=soup1.findAll("h3", {"class":""}) 
  for h in headers:
    stocktags.append(h.text)
  print("Getting Stock tickers and list.")
  print("..........")
  for table in divs:
    row = ''
    rows= table.findAll('td')
    part1_extract(rows,globalist)
  print("Getting all attributes of Stocks")
  print("..........")
  for table in divs:
    row = ''  
    anchor=table.findAll('a')
    part2_extract(anchor,ctx)
  with open('user_stock.csv', 'w',newline='') as csvfile:
  	names  = ['Category','Ticker_Sym','Stock Name', 'Open','Prev Close','Volume','Market Cap']
  	writer = csv.DictWriter(csvfile,fieldnames=names)
  	writer.writeheader()
  csvfile.close()
  global csvtuple
  i=0
  for g in globalist:
    templist=[]
    for key, values in g.items():
      templist.append(key)
      for v in values:
        templist.append(v)  
    csvtuple.insert(i,templist)
    i=i+1
  print("Writing Content to CSV file")
  print("..........")
  with open('stocks.csv', 'w',newline='') as csvfile:
  	names  = ['Ticker_Sym','Stock Name', 'Open','Prev Close','Volume','Market Cap']
  	writer = csv.DictWriter(csvfile,fieldnames=names)
  	writer.writeheader()
  	for item in csvtuple:
  		writer.writerow({'Ticker_Sym': item[0],'Stock Name':item[1],'Open': item[2],'Prev Close':item[3],'Volume':item[4],'Market Cap':item[5]})
  print("Loading User Menu")
  print("..........")
  user_menu()
main()





