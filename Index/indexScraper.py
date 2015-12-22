__author__ = 'kath'

#http://www.index.hr/tag/1556/imigranti/1.aspx

from bs4 import BeautifulSoup
import requests
import simplejson as json
from datetime import datetime
import os

def parseClanak(clanakURL):
    fullUrl = 'http://www.index.hr' + clanakURL
    r = requests.get(fullUrl)

    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    naslov = soup.h1.text.replace("\r", "").replace("\t", "").replace("\n", "")
    sadrzaj = soup.find('div', id='article_text').find_all('p')[1].text
    meta = soup.find('div', class_='writer').text.replace('\r', '').replace('\t', '').split('\n')
    autor= meta[2]
    datum = datetime.strptime(meta[3].split(',')[1], " %d.%m.%Y. %H:%M")

    endValues = dict()
    endValues['Sadrzaj'] = sadrzaj
    endValues['Naslov'] = naslov
    endValues['Autor'] = autor
    endValues['Datum'] = datum.isoformat(' ')

    #print(json.dumps(endValues,  ensure_ascii=False)) DEBUG PRINT


    text_file = open('fjjp_index_' + clanakURL[1:] + '.txt', 'w')
    text_file.write(json.dumps(endValues, ensure_ascii=False, indent=4*' ').encode("UTF_8"))
    # text_file.write("%s\n" % datum.isoformat(' '))
    # text_file.write("%s\n" % autor.encode('utf8'))
    # text_file.write("%s\n\n" % sadrzaj.encode('utf8'))
    text_file.close()

def parseSearch(tag, pageNumber):

    searchURL = "http://www.index.hr/tag/" + tag + `pageNumber` + ".aspx"
    r = requests.get(searchURL)
    data = r.text
    clanci = []

    soup = BeautifulSoup(data, "html.parser")

    linkovi = soup.find_all('h3')
    linkovi.pop(0)

    for link in linkovi:
        clanci.append(link.find('a').get('href'))

    print(clanci)
    return clanci

def fbComment():
       ###START FB PARSE###
    fullUrl = 'http://www.index.hr/clanak.aspx?id=851559'
    output = os.popen('curl -i -X GET "https://graph.facebook.com/v2.0/comments/?id=http%3A%2F%2Fwww.index.hr%2Fvijesti%2Fclanak%2Fjansa-kritizirao-zilet-zicu-na-granici-to-nema-nikakve-svrhe-sada-stavljena-je-prekasno%2F863757.aspx&access_token=CAACEdEose0cBAC9rtTivWgUi438rZB3kkIwS5k1i160ykbzKu8njOKhQiiZBJHhlvrEr3DGD1UmBh3gGq4RDWr9ZCTETbAgxtCPiDY2tEjTmqWleZCO2yp1UMZArlHuu7yGoGIBFBcr3wD03dMHZAgBRVsg0b7ln1sdunR8ZAEXBzqd4Nvmv0AA4dlD5o98eoLK7X2IWZAqIfiusNLx0W9p6"').read()
    print output
    print graph.get_object(fullUrl)



    commentsJsonObject = json.dumps(data, ensure_ascii=False)
    commentDictList = []

    for i in commentsJsonObject['data']:
        commentDict = dict()
        commentDict['Author Name'] = i['from']['name']
        commentDict['Message'] = i['message']
        commentDictList.append(commentDict)
    print commentDictList


    ###END FB PARSE###
tag = "1556/imigranti/"
#parseSearch(tag, 1)
#parseClanak('/clanak.aspx?id=851559')
fbComment()