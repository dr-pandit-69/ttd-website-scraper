import bs4 as BS
import requests
import json
import re
import unicodedata
import csv
from datetime import datetime
import os

l=[]
for i in range((json.load(open('settings.json')))['pages_count']):

    p=i+1

    URL=f"https://news.tirumala.org/category/darshan/page/"+str(p)+"/"
    headers={'User Agent': 'Mozilla/5.0'}

    r = requests.get(URL)

    soup = BS.BeautifulSoup(r.content, 'html.parser')
    
    
    for h in soup.findAll('div',class_='entry-content'):
        k=(h.contents)
        if(len(k)>=2):
            k.pop(0)
            k.pop(-1)
        k=str(k[0])
        k=k[3:]
        k=k[:-4]
        l.append(k)


x=open("headlines.txt","w")
for ele in l:
    x.write(ele)
    x.write('\n')

x.close()


f=open("headlines.txt","r")
f1=open("output.csv","w",newline='')
l=f.readlines()
cw=csv.writer(f1,)
fields=['year','month','date','devotees_count','tonsens_count']
cw.writerow(fields)
for line in l:
    flag1=False

    line = unicodedata.normalize("NFKD", line)
    lezt=line.split(' ')
    for i in range(0,lezt.count('')):
        lezt.pop(lezt.index(''))

    for i in range(0,len(lezt)):
        d = re.findall(r'\b\d{2}\.\d{2}\.\d{4}\b:', lezt[i])
        if(d!=[]):
            date=d[0][:-1]

        if((',' in lezt[i]) and (flag1==False)):
            flag1=True                        
            dar_count=int(re.sub("[^0-9]", "", lezt[i]))

            if(date.replace('.','') in str(dar_count)):
                dar_count=int(str(dar_count)[8:])
 
        elif((',' in lezt[i]) and (flag1)):   
            ton_count=int(re.sub("[^0-9]", "", lezt[i]))
            if(ton_count<1000):
                ton_count=int(re.sub("[^0-9]", "", lezt[i]+lezt[i+1]))

     
    f=[]    
    k=date.split('.')
    k.reverse()
    for ele in k:
        f.append(int(ele))       

    if(datetime(f[0],f[1],f[2])):     
      f.append(dar_count)
      f.append(ton_count)      
      cw.writerow(f)
      print('Row Written Successfully',f)


os.remove('headlines.txt')




