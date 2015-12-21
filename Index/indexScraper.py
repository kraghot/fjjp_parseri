__author__ = 'kath'

#http://www.index.hr/tag/1556/imigranti/1.aspx

from bs4 import BeautifulSoup
import requests
import simplejson as json
from datetime import datetime

def parseRad(clanakURL):

    r = requests.get('http://www.index.hr' + clanakURL)
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

    print(json.dumps(endValues,  ensure_ascii=False))

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


tag = "1556/imigranti/"
#parseSearch(tag, 1)
parseRad('/clanak.aspx?id=851559')