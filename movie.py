from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
import requests
import mysql.connector

#the prompt that was assigned to me was to create a CRUD app to maintain a movies databases with the database stored in sql and use
#postman in implementation.

#As much i understood all postman was doing was a get request to the site and returning the data so i didn't knew how to implement it
#Then i use selenium to scrape the web over requests mainly cause the site that i was gonna scrape has restriction against requests
#For instance if i send a request to bookmyshow, it shows a cloudflare error (error code 1020)
#Also why does it open an window to run the program
#I tried testing it without opening any window by passing another arguement '--headless' but that led to google to show a captcha when 
#trying to access the page
# But other than these limitations, this program can be run 24/7 as it check the bookmyshow at 4:00 pm as i think it is the time they
# update their site data.
# It then extracts the movie name, rating and language from the site and add it to a list
# then it check the list with the rows already present in the table
# if it is present then it is deleted from the list and then the remaining elements are added to the table to avoid duplicates
# It also check if all the rows in the table are still showing in theatre or not by comparing it with the movie list
# it is not screening anymore it is deleted from the table 

def read(a):
    for i in a:
        print(i[0],'\t',i[1],'\t',i[2])


def fun():
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--incognito')
    s = Service('')#give the location of the chromedriver which can be downloaded from https://chromedriver.chromium.org/downloads
    driver = webdriver.Chrome(service=s,options=options)
    driver.get('https://in.bookmyshow.com/explore/movies-vellore')
    time.sleep(15)
    source = driver.page_source
    #source = requests.get(url='https://www.google.com/search?q=all+movies+showing+in+vellore').text
    soup = BeautifulSoup(source,'html.parser')
    #print(soup.prettify())
    for i in soup.find_all("div",class_ = 'cBsijw'):
        movie.append(i.text)
    for i in soup.find_all("div",class_= 'bMPkUy'):
        rating_and_lang.append(i.text)

movie = []
rating_and_lang = []
con = mysql.connector.connect(host="localhost",password="",user="",charset="utf8")#enter the password and username as per your mysql
cur = con.cursor()
check = False
try:
    cur.execute('Use movie')
except Exception:
    cur.execute('Create database movie')
    cur.execute('Use movie')
    cur.execute('Create Table movie (movie_name varchar(255), Rating varchar(10), Languages varchar(255))')
    check = True
try:
    cur.execute("select * from movie")
    if cur.fetchall() == []:
        check = True
except Exception:
    cur.execute('Create Table movie (movie_name varchar(255), Rating varchar(10), Languages varchar(255))')
    check = True
con.commit()
con.close()
if check or time.localtime().tm_hour == 15:
    check = False
    con = mysql.connector.connect(host="localhost",password="",user="",charset="utf8")#enter the username and password as per the sql
    cur = con.cursor()
    fun()
    cur.execute('use movie')
    cur.execute("select * from movie")
    a = cur.fetchall()
    for i in a:
        if i[0] not in movie:
            cur.execute('delete from movie where movie_name = \''+ i[0]+'\'')
        else:
            movie.remove(i[0])
    for i in range(len(movie)):
        cur.execute('insert into movie values (\''+ movie[i] + '\',\'' + rating_and_lang[2*i] + '\',\'' + rating_and_lang[2*i+1]+'\')')
    cur.execute("select * from movie")
    a = cur.fetchall()
    read(a)
    con.commit()
    con.close()
