__author__ = 'kath'

#http://www.index.hr/tag/1556/imigranti/1.aspx

from bs4 import BeautifulSoup
from datetime import datetime
import os, urllib2, time, simplejson as json

indexBlack = []
lastDate = datetime.now()
rbr = 1
rbrKomentara = 0

def parseClanak(clanakURL):
    global rbr
    global lastDate
    fullUrl = 'http://www.index.hr' + clanakURL
    request = urllib2.Request(fullUrl)
    response = urllib2.urlopen(request)
    finalUrl = response.geturl()
    data = response.read()


    if finalUrl.startswith("http://www.index.hr/black"):
        indexBlack.append(finalUrl)
        return

    soup = BeautifulSoup(data, "html.parser")

    naslov = soup.h1.text.replace("\r", "").replace("\t", "").replace("\n", "")
    sadrzajContainer = soup.find('div', id='article_text').find_all('p')
    sadrzaj = []
    for i in range (1, len(sadrzajContainer)):
        sadrzaj.append(sadrzajContainer[i].text)
    sadrzaj = "\n".join(sadrzaj)

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

    if datum.date() == lastDate.date():
        rbr += 1
    else:
        lastDate = datum
        rbr = 1

    identifier = "%2d%2d%4d-%d-%s" % (datum.day, datum.month, datum.year, rbr, endValues['Autor'])

    htmlFile = open('index_html_' + identifier  + '.html', 'w')
    htmlFile.write(data)
    htmlFile.close()

    text_file = open('index_' + identifier + '.txt', 'w')
    text_file.write(endValues['Naslov'].encode("UTF_8"))
    text_file.write("\n".encode("UTF_8"))
    text_file.write(endValues['Sadrzaj'].encode("UTF_8"))
    text_file.close()

    rbrKomentara = 0
    fbComment(finalUrl, identifier)

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

def fbComment(urlclanak, identifier):

    global rbrKomentara
    rbrKomentara += 1
    #fbUrl = urllib.quote_plus(urlclanak)
    output = os.popen('curl -X GET "https://graph.facebook.com/v2.0/comments/?id=' + urlclanak +
                      '&access_token=CAACf7v6YTeMBAKQjlpusu8Jq63EAex6HPCqIrKTcyZB3fyvtWyxD2ZCpSkuqjASHuyPAH8DSIE7KuW4BeTKZBFZBpPewMe4Qro4k2hHK1RClbZCGhmH676ta8s6wVp7pZAnQiyPL3XBhCxohvx70dj4HIoEWPj048Emt27PlZAtziAGgGpA2PGy123dGaejZAAoZD"'
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
        commentFile = open('index-komentari-' + identifier + "_%d-%s" % (rbrKomentara, commentDict['Author Name']) + '.txt', 'w')
        commentFile.write(json.dumps(commentDictList, ensure_ascii=False, indent=4*' ', sort_keys=True).encode("UTF_8"))
        commentFile.close()
    except:
        print("FACEBOOK PARSE ERROR")


tag = "1556/imigranti/"

# parseSearch(tag, 1)
# parseClanak('/clanak.aspx?id=863851')
# fbComment('/clanak.aspx?id=863851')

for i in range (1, 21):
    clanci = parseSearch(tag, i)
    for clanak in clanci:
        parseClanak(clanak)
        time.sleep(2)

fileBlack = open("indexBlack.txt", "w")
fileBlack.write(indexBlack)
fileBlack.close()

print("\n\nDONE\n\n")
