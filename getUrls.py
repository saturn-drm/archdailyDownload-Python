#! /usr/bin/env Python3
# getUrls.py - Get the urls from the website.

import requests, bs4

proxies = {
    'https': 'https://127.0.0.1:1087',
    'http': 'http://127.0.0.1:1087'
}
headers = {
    'Referer': 'https://www.archdaily.com/898694/caja-de-tierra-equipo-de-arquitectura?ad_content=898694&ad_medium=widget&ad_name=featured_loop_main', 
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
}
# Get all the projects' urls and names from the search site.
def getProjectList(url):
    res = requests.get(url, proxies = proxies, headers = headers)
    res.raise_for_status()
    res.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    projectsElem = soup.select('#search-results > div.afd-main-content-search.afd-main-content-search--left > ul > li > a')
    nameElem = soup.select('#search-results > div.afd-main-content-search.afd-main-content-search--left > ul > li > a > h2')
    projectsUrlList = []
    nameList = []
    for project in projectsElem:
        projectsUrlList.append(project.get('href'))
    for name in nameElem:
        nameList.append(name.getText())
    return (projectsUrlList, nameList)

# Get the next page link.
def getNextLink(url):
    res = requests.get(url, proxies = proxies, headers = headers)
    res.raise_for_status()
    res.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    nextLink = soup.select('#pagination_container > div > div > a.next')[0].get('href')
    return nextLink

# Get all the picture links of one project.
def getAllPics(url):
    res = requests.get(url, proxies = proxies, headers = headers)
    res.raise_for_status()
    res.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    gallery = soup.select('#gallery-thumbs > li > a')
    picList = []
    for item in gallery:
        picList.append(item.get('href'))
    return picList

# Get each original img.
def getOriginalPicList(url):
    res = requests.get(url, proxies = proxies, headers = headers)
    res.raise_for_status()
    res.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    originalElem = soup.select('#gallery-thumbs > li')
    originalLinkList = []
    for item in originalElem:
        originalLinkList.append(item.img.get('data-src').replace('thumb_jpg', 'large_jpg'))
    return originalLinkList