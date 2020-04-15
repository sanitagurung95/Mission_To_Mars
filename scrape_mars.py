#import dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
import pymongo
import time

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': r'\Users\sanitagurung\Desktop\KU-OVE-DATA-PT-01-2020-U-C-master\02-Homework\12-Web-Scraping-and-Document-Databases\Instruction\chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)
def scrape():
    browser = init_browser()
    listings = {}

    #visit url
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #pull html text and parse
    html_code = browser.html
    soup = BeautifulSoup(html_code, "html.parser")

    #grab needed info
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text


    # # Latest Featured Image

    # Featured Image URL & visit
    #Uncomment here##
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    #navigate to link
    #uncomment here
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    #get html code once at page
    #uncomment here
    image_html = browser.html

    #parse
    #uncomment
    soup = BeautifulSoup(image_html, "html.parser")

    #find path and make full path
    #uncomment
    image_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov" + image_path

    # # Mars Weather
     #weather url and html
    marsweather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsweather_url)
    weather_html = browser.html

    #get lastest tweet
    soup = BeautifulSoup(weather_html, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    # # Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    #get html
    facts_html = browser.html
    soup = BeautifulSoup(facts_html, 'html.parser')

    #get the entire table
    table_data = soup.find('table', class_="tablepress tablepress-id-mars")

    #find all instances of table row
    table_all = table_data.find_all('tr')

    #set up lists to hold td elements which alternate between label and value
    labels = []
    values = []

    #for each tr element append the first td element to labels and the second to values
    for tr in table_all:
        td_elements = tr.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)
            
#uncomment    #make a data frame
    mars_facts_df = pd.DataFrame({
        "Label": labels,
        "Values": values
    })

     # get html code for DataFrame
    fact_table = mars_facts_df.to_html(header = False, index = False, escape=False)
    fact_table

#Hemisphere Images Scraping
    hemispheres_url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    soup = BeautifulSoup(hemispheres_html, 'html.parser')
    mars_hemispheres = soup.find_all('h3')
	
	
    hemisphere_image_urls = []
	#Loop to scrape all hemispheres
    for row in mars_hemispheres:
        title= row.text
        browser.click_link_by_partial_text(title)
        time.sleep(1)
        img_html = browser.html
        soup_h = BeautifulSoup(img_html, 'html.parser')
        url_img = soup_h.find('div',class_='downloads').a['href']
        print ("Hemisphere Name :  "+ str(title))
        print ("Hemisphere URL:  " + str(url_img))

        img_dict = {}
        img_dict['title']= title
        img_dict['img_url']= url_img
        hemisphere_image_urls.append(img_dict)	
        
        browser.visit(hemispheres_url)


    listings = {
        "id": 1,
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
       "fact_table": fact_table,
       "hemisphere_images": hemisphere_image_urls
    }

    #return mars_dict

    return listings
