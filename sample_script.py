#!/usr/bin/env python3

#SAMPLE_SCRIPT [assuming ENGLISH Website]
#due to privacy reasons, website url & user agent not shared.



#Importing Important Libraries
import urllib.request,urllib.parse,urllib.error
from bs4 import BeautifulSoup
import ssl
from datetime import datetime
import re
import MySQLdb


#for calculating the time taken in scraping the data.
starttime=datetime.now()


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


#Connecting to a Database
conn=MySQLdb.connect(host='localhost',user='your_username',password='your_password', db='Scraped_Data')
cur=conn.cursor()


#To make MySQL store data in UTF-8
conn.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

cur.execute('CREATE DATABASE IF NOT EXISTS Scraped_Data')
cur.execute('USE Scraped_Data')
cur.execute('CREATE TABLE IF NOT EXISTS Cryptocurrency_Data(Published_Date TEXT, News_URL VARCHAR(255) UNIQUE , Title TEXT, Content TEXT, Images_URL TEXT, News_Source TEXT, Language TEXT)')



#First URL enter 
p_url='enter your url here'
#due to privacy reasons, website url & etc not shared.

try:
    #Opening the URL, by changing the User Agent
    p_req= urllib.request.Request(p_url, headers={'User-Agent': 'enter your user agent id here'})
    #due to privacy reasons user agent not shared...

    # parsing it using Beautiful Soup
    p_html= urllib.request.urlopen(p_req).read()
    p_soup=BeautifulSoup(p_html, 'html.parser')


    #Extracting Total Page Number
    last_url=p_soup.find('div',{'class':'pagination'}).findAll('a')[3]['href']
    page_total=re.search(r'[\d]{1,}',last_url).group()
    print(page_total)

except:
    pass


#Parsing Function
def parsing(arg):
    #'arg' or argument of the function is basically each news link of a particular page
    gc_url=arg['href']
    gc_req= urllib.request.Request(gc_url, headers={'User-Agent': 'enter your user agent id here'})
    #due to privacy reasons user agent not shared...
    gc_html=urllib.request.urlopen(gc_req).read()
    gc_soup=BeautifulSoup(gc_html, 'html.parser')

    db1=c_url  #News_Source.....Eg: page/1
    
    db2=gc_url #News_URL

    db3=arg['title']  #Title
    
    db4=gc_soup.find('meta',{'property':'og:description'})['content']  #Content
    
    db6=str(gc_soup.find('meta',{'property':'article:published_time'})['content']) #Published_Date

    gc_imageurl=gc_soup.find('div',{'class':'article-top-image-section'})['style']
    i=gc_imageurl.find('(')
    f=gc_imageurl.find('}')
    db5=gc_imageurl[i+2:f-1]    #Image_URL
    cur.execute("INSERT IGNORE INTO Cryptocurrency_Data (Published_Date,News_URL,Title,Content,Images_URL,News_Source,Language)  VALUES (%s,%s,%s,%s,%s,%s,'ENGLISH')", (db6,db2,db3,db4,db5,db1))



#Now sequentially moving from Page to Page & Parsing each page's data and putting in Database
for pg_no in range(1,int(page_total)+1):
    c_url='enter your url here'+str(pg_no)
    try:
        c_req= urllib.request.Request(c_url, headers={'User-Agent': 'enter your user agent id here'})
        #due to privacy reasons user agent not shared...
        c_html=urllib.request.urlopen(c_req).read()
        c_soup=BeautifulSoup(c_html, 'html.parser')
        gc_urls=c_soup.findAll('a',{'class':'standard-format-icon'})
        for gc in gc_urls:
            parsing(gc)            
            conn.commit()

    except:
        pass

cur.execute("SELECT * FROM Cryptocurrency_Data ORDER BY Published_Date DESC")
cur.close() 


endtime=datetime.now() 
print(endtime-starttime)




#[code by AAYUSH GADIA]


