import pandas as pd
import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from splinter import Browser
import time
from webdriver_manager.chrome import ChromeDriverManager

def init():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape_news():
    browser=init()

    url = 'https://mars.nasa.gov/news/'
    html = urlopen(url)

    soup = bs(html, 'lxml')
    type(soup)

    title = soup.find_all("div", {"class": "content_title"})[0].text
    news_title = title.strip('\n')
    # news_title
    news = soup.find_all("div", {"class": "rollover_description_inner"})[0].text
    news_para = news.strip('\n')

    browser.quit()

    return news_para, news_title
    
    # # Splinter to image: https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html
def scrape_url():

    browser=init()
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    print(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    imgLinkString=soup.find_all("a",{"class": "showimg fancybox-thumbs"})#[0].href

    for a in imgLinkString:
        imgLink=a['href']

    featured_image_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"+imgLink
    
    browser.quit()

    return featured_image_url

def scrape_table():
    # # Pulling in table from: https://space-facts.com/mars/
    browser=init()
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    tables
    df = tables[0]
    html_table = df.to_html()
    html_table=html_table.replace('\n', '')
    # df.to_html('MarsTable.html')
   
    browser.quit()

    return html_table

    # #  dictionary of urls from: https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
def scrape_dict():

    browser=init()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    image_urls=[]

    for i in range(0,4):
        browser=init()
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        browser.find_by_css("a.product-item h3")[i].click()
        html = browser.html
        soup = bs(html, "html.parser")
        # print(soup)
        title = soup.find('h2').text
        # title
        image_url = soup.find_all('a','target'=='_blank')[4]["href"]
        # image_url
        image_url = {
            "title": title,
            "img_url": image_url}
        image_urls.append(image_url)

    browser.quit()

    return image_urls

def scrape_all():
    data_results = {"News_inputs": scrape_news(),
                 "Featured_image": scrape_url(),
                 "mars_table": scrape_table(),
                 "image_urls": scrape_dict() }
    return data_results

# print(scrape_all())  -- if name = main



