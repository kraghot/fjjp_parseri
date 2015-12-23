__author__ = 'kath'

#http://www.index.hr/tag/1556/imigranti/1.aspx

from bs4 import BeautifulSoup
from datetime import datetime
import os, urllib2, time, simplejson as json

indexBlack = []

def parseClanak(clanakURL):
    fullUrl = 'http://www.index.hr' + clanakURL
    request = urllib2.Request(fullUrl)
    response = urllib2.urlopen(request)
    finalUrl = response.geturl()
    data = response.read()

    if finalUrl.startswith("http://www.index.hr/black"):
        indexBlack.append(fullUrl)
        return

    soup = BeautifulSoup(data, "html.parser")

    naslov = soup.h1.text.replace("\r", "").replace("\t", "").replace("\n", "")
    sadrzaj = soup.find('div', id='article_text').find_all('p')[1].text
    meta = soup.find('div', class_='writer').text.replace('\r', '').replace('\t', '').split('\n')
    autor= meta[2]
    datum = datetime.strptime(meta[3].split(',')[1], " %d.%m.%Y. %H:%M")

    if datum.year < 2015:
        return

    endValues = dict()
    endValues['Sadrzaj'] = sadrzaj
    endValues['Naslov'] = naslov
    endValues['Autor'] = autor
    endValues['Datum'] = datum.isoformat(' ')

    text_file = open('index_' + clanakURL[-6:] + '.txt', 'w')
    text_file.write(json.dumps(endValues, ensure_ascii=False, indent=4*' ').encode("UTF_8"))
    text_file.close()

    fbComment(finalUrl)

def parseSearch(tag, pageNumber):

    searchURL = "http://www.index.hr/tag/" + tag + `pageNumber` + ".aspx"
    request = urllib2.Request(searchURL)
    response = urllib2.urlopen(request)
    data = response.read()
    clanci = []

    soup = BeautifulSoup(data, "html.parser")

    linkovi = soup.find_all('h3')
    linkovi.pop(0)

    for link in linkovi:
        clanci.append(link.find('a').get('href'))

    print(clanci)
    return clanci

def fbComment(urlclanak):

    #fbUrl = urllib.quote_plus(urlclanak)
    output = os.popen('curl -X GET "https://graph.facebook.com/v2.0/comments/?id=' + urlclanak +
                      '&access_token=CAACEdEose0cBAFPYaUK6uRrg05BnvAqwCzp2ZBrWw0FVyo1gDq4sKKaiM59zflMDeco1AnbpZCSsq0keG5ytjuZCGD8HrchGYbPXAzWQbQyPNrR8kKfdUH1IV8ZBInznQfjGAfI9fqB5ydJ4KWdzaUiS4K5tyQQbcXRhd3v30YHnZCtg5SSzRMpb58PXyt0dKocdqI8OZCWrO4zNMfMzh2"'
                      ).read()
    print output


    commentsJsonObject = json.loads(output)
    commentDictList = []
    try:
        for i in commentsJsonObject['data']:
            commentDict = dict()
            commentDict['Author Name'] = i['from']['name']
            commentDict['Message'] = i['message']
            commentDictList.append(commentDict)
        print commentDictList
        commentFile = open('index-komentari-' + urlclanak[-11:-5] + '.txt', 'w')
        commentFile.write(json.dumps(commentDictList, ensure_ascii=False, indent=4*' ', sort_keys=True).encode("UTF_8"))
        commentFile.close()
    except:
        print("FACEBOOK PARSE ERROR")


tag = "1556/imigranti/"

#parseSearch(tag, 1)
#parseClanak('/clanak.aspx?id=863851')
#fbComment('/clanak.aspx?id=863851')

for i in range (1, 21):
    clanci = parseSearch(tag, i)
    for clanak in clanci:
        parseClanak(clanak)
        time.sleep(2)

fileBlack = open("indexBlack", "w")
fileBlack.write(indexBlack)
fileBlack.close()

print("\n\nDONE\n\n")
