#! /usr/bin/env Python3
# main.py - Download the pictures from Archdaily.

import os, getUrls, requests

os.makedirs('/Users/meizihan/Downloads/Archdaily', exist_ok=True)
os.chdir('/Users/meizihan/Downloads/Archdaily')
url = 'https://www.archdaily.com/search/projects'
proxies = {
    'https': 'https://127.0.0.1:1087',
    'http': 'http://127.0.0.1:1087'
}
headers = {
    'Referer': 'https://www.archdaily.com/898694/caja-de-tierra-equipo-de-arquitectura?ad_content=898694&ad_medium=widget&ad_name=featured_loop_main', 
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
}
print ('Project images will be saved to %s...' % ('/Users/meizihan/Downloads/Archdaily'))
pageNum = int(input('Enter the pages of the projects you want:\n'))

pageIndex = 1
while pageIndex <= pageNum:
    # Get the list of all the projects from the search site.
    (projectsUrlList, nameList) = getUrls.getProjectList(url)
    for i in range (len(projectsUrlList)):
        projectName = nameList[i].split('/')[0]
        # Make sure the project is new.
        exsistingProject = []
        for folderName, subFolders, fileNames in os.walk('.'):
            for subFolderName in subFolders:
                exsistingProject.append(subFolderName)
        if projectName not in exsistingProject:
            os.makedirs('./%s' % (projectName), exist_ok=True)
            print ('Downloading the project %s to %s' % (projectName, '/Users/meizihan/Downloads/Archdaily/' + projectName))
            # Get the original img url.
            originalPicUrlList = getUrls.getOriginalPicList('https://www.archdaily.com' + projectsUrlList[i])
            for j in range (len(originalPicUrlList)):
                picName = originalPicUrlList[j].split('?')[0]
                print ('Downloading the image %s' % (os.path.basename(picName)))
                # Download the img.
                res = requests.get(originalPicUrlList[j], proxies = proxies, headers = headers)
                try:
                    res.raise_for_status()
                except:
                    print ('The image %s does not exists.' % (os.path.basename(picName)))
                res.encoding = 'utf-8'
                imgFile = open(os.path.join('./%s' % (projectName), os.path.basename(picName)), 'wb')
                for chunk in res.iter_content(100000):
                    imgFile.write(chunk)
                imgFile.close()
        else:
            print ('The project %s already exists.' % (projectName))
        print ('')
    # Get the next link.    
    url = getUrls.getNextLink(url)
    pageIndex += 1
print ('Done.')
