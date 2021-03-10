

import pandas as pd
import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


url = 'https://mars.nasa.gov/news/'
html = urlopen(url)


# In[3]:


soup = bs(html, 'lxml')
type(soup)


# In[4]:


title = soup.find_all("div", {"class": "content_title"})[0].text
news_title = title.strip('\n')
news_title


# In[5]:


news = soup.find_all("div", {"class": "rollover_description_inner"})[0].text
news_para = news.strip('\n')
news_para


# In[6]:


def init():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser


# # Splinter to image: https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html

# In[7]:


browser=init()
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)
print(url)


# In[8]:


html = browser.html
# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')
# Retrieve all elements that contain book information

imgLinkString=soup.find_all("a",{"class": "showimg fancybox-thumbs"})#[0].href

for a in imgLinkString:
    imgLink=a['href']

featured_image_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"+imgLink
featured_image_url


# # Pulling in table from: https://space-facts.com/mars/

# In[9]:


url = 'https://space-facts.com/mars/'
# browser.visit(url)
print(url)


# In[10]:


tables = pd.read_html(url)
tables
df = tables[0]
html_table = df.to_html()
html_table=html_table.replace('\n', '')
df.to_html('MarsTable.html')
html_table
# !open MarsTable.html
# df.head(10)


# #  dictionary of urls from: https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

# In[11]:


browser=init()
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[31]:


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


# In[32]:


image_urls


# In[ ]:




