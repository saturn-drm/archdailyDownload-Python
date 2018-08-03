#! /usr/bin/env Python3
# go141.py - Get all the information of the everyday girl on go141.com.
#            Create a workbook each time.

import requests
# import os
import openpyxl
import bs4
import datetime
import pprint
from openpyxl.styles import Font, Alignment

def getSoup(url):
    res = requests.get(url, proxies = proxies)
    try:
        res.raise_for_status()
    except:
        print (url + '页面丢失')
    res.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    return soup

def getChinese(string):
    chinese = ''
    for chunk in string:
        if chunk >= '\u4e00' and chunk <= '\u9fa5':
            chinese += chunk
    return chinese

url = 'http://go141.com/zh/'
proxies = {
    'https': 'https://127.0.0.1:1087',
    'http': 'http://127.0.0.1:1087'
}
# headers = {
#     'Referer': 'http://go141.com/zh/A28015-%E6%B7%B1%E6%B0%B4%E5%9F%97-%E6%A8%93%E4%B8%8A%E9%AA%A8-%E6%9F%94%E6%9F%94%E5%B0%88%E6%A5%AD%E6%8E%A8%E6%8B%BF.html?ref=Side+list+(Homepage)',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
# }
today = datetime.date.today() # e.g. 2018-07-30

gUrlList = []
gNameList = []
gDict = {}

soup = getSoup(url)
girlList = soup.select('div.newlist > ul > li > b > a')
for item in girlList:
    gUrlList.append('http://go141.com/zh/' + item.get('href')) # Url list.
    gNameList.append(item.getText()) # Name list.
    gDict.setdefault(item.getText(), {}) # {name:{}}

for nameIndex in range (len(gNameList)):
    gDict[gNameList[nameIndex]].setdefault('网址', gUrlList[nameIndex]) # {name:{网址:____}}
    infosoup = getSoup(gUrlList[nameIndex])
    infoKeyElem = infosoup.select('td > div.row > div.field-heading')
    infoValueElem = infosoup.select('td > div.row > div.field-content')
    for i in range (len(infoKeyElem)):
        if infoValueElem[i].getText():
            infoValue = infoValueElem[i].getText()
        if  not infoValueElem[i].getText():
            infoValue = ' '.join(infoValueElem[i].contents[0:3])
        infoValue = infoValue.replace('\n', '').replace('\r','').replace('\t', '')
        gDict[gNameList[nameIndex]].setdefault(infoKeyElem[i].getText().replace(':', ''), infoValue) #{name:{网址:____,电话:,...}}
# Got the dict like {'name1':{'a':'1','b':'2'},'name2':{'a':'1','c':'3'}}

# Write into an excel file.
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = 'The stars for today' + str(today)
sheet['A1'] = '姓名'
sheet['B1'] = '身高'
sheet['C1'] = '三围'
sheet['D1'] = '年龄'
sheet['E1'] = '地址'
sheet['F1'] = '电话'
sheet['G1'] = '时间'
sheet['H1'] = '国籍'
sheet['I1'] = '语言'
sheet['J1'] = '服务'
sheet['K1'] = '其他'
sheet['L1'] = '简评'
sheet['M1'] = '网址'

rowIndex = 1
fontObj = Font(bold=True)
for name in gDict.keys():
    rowIndex += 1
    sheet['A%s' % rowIndex] = name
    for infoName, infoContent in gDict[name].items():
        if infoName == '身高':
            sheet['B%s' % rowIndex] = infoContent
        elif infoName == '三圍':
            sheet['C%s' % rowIndex] = infoContent
        elif infoName == '年齡':
            sheet['D%s' % rowIndex] = infoContent
        elif infoName == '地址':
            sheet['E%s' % rowIndex] = infoContent
        elif infoName == '電話':
            sheet['F%s' % rowIndex] = infoContent
        elif infoName == '時間':
            sheet['G%s' % rowIndex] = infoContent
        elif infoName == '國籍':
            sheet['H%s' % rowIndex] = infoContent
        elif infoName == '語言':
            sheet['I%s' % rowIndex] = infoContent
        elif infoName == '服務':
            sheet['J%s' % rowIndex] = infoContent
        elif infoName == '其他':
            sheet['K%s' % rowIndex] = infoContent
        elif infoName == '簡評\xa0':
            sheet['L%s' % rowIndex] = infoContent
        elif infoName == '网址':
            sheet['M%s' % rowIndex] = infoContent

sheet.row_dimensions[1].font = Font(bold=True)
sheet.freeze_panes = 'A2'

wb.save('141Go-THE_STARS_FOR_TODAY-%s.xlsx' % (str(today)))
# text = open('./1.txt', 'w')
# text.write(pprint.pformat(gDict))
# text.close()