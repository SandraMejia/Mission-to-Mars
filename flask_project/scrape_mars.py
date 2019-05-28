# Sandra Mejía

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
import pymongo
import re

def main():
    # documentResult = {}
    _nasaMarsNews = nasaMarsNews()
    _marsSpacemages = marsSpacemages()
    _marsWeather = marsWeather()
    _marsFacts = marsFacts()
    _marsHemispheres = marsHemispheres()
    return {**_nasaMarsNews, **_nasaMarsNews, **_marsWeather, **_marsFacts, **_marsHemispheres, **_marsSpacemages}

def initBrowser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def nasaMarsNews():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    latestNewsTitlesArray = soup.select('div.content_title > a')
    latestNewsAbstractArray= soup.select('.image_and_description_container .rollover_description_inner')


    # for i in range(0, len(latestNewsTitlesArray) -1 ):
    #     print(latestNewsTitlesArray[i].text)
    #     print(latestNewsAbstractArray[i].text)

    news_title = latestNewsTitlesArray[0].text
    news_p = latestNewsAbstractArray[0].text

    return {
        'news_title': news_title,
        'news_p': news_p
    }
    
def marsSpacemages():
    browser = initBrowser()
    marsPageUrl = 'https://www.jpl.nasa.gov/'
    marsImagesUrl ='spaceimages/?search=&category=Mars'
    browser.visit(marsPageUrl + marsImagesUrl)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    fullImagePath = soup.select('article.carousel_item')[0]['style']
    # fullImagePath = re.search("'\s*((?:.|\n)*?)'", fullImagePath, 0)
    # fullImagePath = fullImagePath.group().replace("'", "")
    fullImagePath = fullImagePath[fullImagePath.find("url('/")+5:][:fullImagePath.find("');'")-2]
    featured_image_url = marsPageUrl + fullImagePath

    return {
        'featured_image_url': featured_image_url
    }

def marsWeather():
    marsWeatherUrl = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(marsWeatherUrl)
    soup = BeautifulSoup(response.text, 'lxml')

    tweetsElements = soup.select('.js-tweet-text-container p')
    tweetsElements[0].select("twitter-timeline-link")
    marsWeatherLastTweet = tweetsElements[0].text.strip().replace('\n', ' ')
    return {
        'marsWeatherLastTweet': marsWeatherLastTweet
        }

def marsFacts():
    marsFactsUrl = 'https://space-facts.com/mars/'
    marsFactsTables = pd.read_html(marsFactsUrl)
    # type(marsFactsTables)
    # marsFactsTables[0]

    # marsFactsDf = marsFactsTables[0].set_index(0)
    # marsFactsDf = marsFactsDf.rename(columns={0:'',1:''})

    marsFactsDf = marsFactsTables[0]
    marsFactsDf = marsFactsDf.set_index(marsFactsDf.iloc[:,0].values).drop(0,1).rename(columns={1:''})

    marsFactsHtml = marsFactsDf.to_html()
    marsFactsHtml = marsFactsHtml.replace('\n', '')
    return{
        'marsFactsHtml': marsFactsHtml
    }

def marsHemispheres():
    browser = initBrowser()
    astrogeologyMarsBaseUrl = 'https://astrogeology.usgs.gov'
    astrogeologyMarsSearchUrl = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astrogeologyMarsBaseUrl + astrogeologyMarsSearchUrl)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    hemisphere_image_urls = []

    itemsToVisit = soup.select('.item div.description a.itemLink')
    
    for itemToVisit in itemsToVisit:
        browser.visit(astrogeologyMarsBaseUrl + itemToVisit['href'])
        _html = browser.html
        _soup = BeautifulSoup(_html, 'lxml')
        hemisphereName = _soup.select('div.content h2.title')
        downloadLinks = _soup.select('div.downloads ul li a')
        print(downloadLinks[0]['href'])
        print(hemisphereName[0].text)
        hemisphere_image_urls.append({
            'title': hemisphereName[0].text,
            'image_url': downloadLinks[0]['href']
        })

    return {
        'hemisphere_image_urls':hemisphere_image_urls
        }







# # setup mongo connection
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)

# # connect to mongo db and collection
# db = client.MarsAssignament
# collection = db.MarsFacts