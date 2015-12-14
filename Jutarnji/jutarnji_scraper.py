__author__ = 'kath'

#<div class="span-6 last"> <p class="head"> Objavljeno: 30.11.2009.></p> <h1> Cemu takav strah od mutavih minareta </h1> </div>
#url: http://www.jutarnji.hr/cemu-takav-strah-od--mutavih--minareta/380838/ ----> moze i http://www.jutarnji.hr/380838/
#pretrazivanje: http://www.jutarnji.hr/search.do?searchString=izbjeglice&publicationId=1&sortString=by_date_desc
#za datum clanka u pretrazivanju --> http://www.jutarnji.hr/search.do?timePeriod=2015&publishDate=2015-09-12&newPhrase=&publicationId=1&searchString=izbjeglice&sortString=by_date_desc



from bs4 import BeautifulSoup
import requests, re
import simplejson as json
import time


def parseRad(clanci):
    url = clanci
    r = requests.get(url)

    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    sadrzaj = []
    autor= []
    datum = []

    for p in soup.find_all('div', class_='dr_article'):
        sadrzaj.append(p.text)

    for a in soup.find_all('div', class_='author'):
        autor.append(a.text)

    for div in soup.find_all('div', class_='published'):
        datum.append(div.text)

    endValues = dict()
    endValues['Sadrzaj'] = sadrzaj[0]
    endValues['Autor'] = autor[0].replace("Autor:\n", " ")
    endValues['Datum'] = datum[0].replace("Objavljeno:","")

    print(json.dumps(endValues,  ensure_ascii=False))


def parseSearch(tag):

    scrapedIDs = []
    searchURL = "http://www.jutarnji.hr/sve_teme/" + tag
    r = requests.get(searchURL)
    data = r.text
    clanci = []
    #ids = []
    soup = BeautifulSoup(data, "html.parser")
    linkovi = soup.find_all('a', class_='image')

    print(linkovi)

    for link in linkovi:
        clanci.append(link["href"])
        print(clanci)


    #for link in clanci:
     #   ids.append(int(re.search('rad=(.+?)$', link).group(1)))

    return clanci

    # for link in scrapedIDs:
    #
    #     print re.search("rad=(.+?)\"", link)

idevi = parseSearch('izbjeglice')
for rad in idevi:
    parseRad(rad)
    time.sleep(2)