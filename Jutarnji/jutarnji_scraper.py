__author__ = 'kath'

#<div class="span-6 last"> <p class="head"> Objavljeno: 30.11.2009.></p> <h1> Cemu takav strah od mutavih minareta </h1> </div>
#url: http://www.jutarnji.hr/cemu-takav-strah-od--mutavih--minareta/380838/ ----> moze i http://www.jutarnji.hr/380838/
#pretrazivanje: http://www.jutarnji.hr/search.do?searchString=izbjeglice&publicationId=1&sortString=by_date_desc
#za datum clanka u pretrazivanju --> http://www.jutarnji.hr/search.do?timePeriod=2015&publishDate=2015-09-12&newPhrase=&publicationId=1&searchString=izbjeglice&sortString=by_date_desc



from bs4 import BeautifulSoup
import requests, re
import simplejson as json
import time
import codecs
from pprint import pprint
import urllib, json
rbr=0

def parseRad(clanci):
    global rbr
    url = clanci
    r = requests.get(url)
    data = r.text


    soup = BeautifulSoup(data, "html.parser")
    sadrzaj = ""
    autor= ""
    datum = ""
    title= ""

    replaceString="<!--"
    soup= BeautifulSoup(str(soup).replace("<script", replaceString))
    soup= BeautifulSoup(str(soup).replace("<h2>VEZANE VIJESTI", replaceString))
    soup= BeautifulSoup(str(soup).replace("<ul", replaceString))

    replaceString="-->"
    soup= BeautifulSoup(str(soup).replace("</script>", replaceString))
    soup= BeautifulSoup(str(soup).replace("ijesti</h3>", replaceString))
    soup= BeautifulSoup(str(soup).replace("</ul>", replaceString))



    for p in soup.find_all('div', class_='dr_article'):
        sadrzaj=p.text
        sadrzaj=sadrzaj.replace("\n\n\n", "")
    if sadrzaj == "":
        return

    for a in soup.find_all('div', class_='author'):
        autor=a.text

    for div in soup.find_all('div', class_='published'):
        datum=div.text
        datum=datum.replace("Objavljeno: ", "")

    for t in soup.find_all('title'):
        title=t.text

    comment_url="https://graph.facebook.com/comments/?id=" + url
    comment_data=urllib.urlopen(comment_url)

    comment=json.loads(comment_data.read())

    num_com = len(comment['data'])

    endValues = dict()
    endValues['Sadrzaj'] = sadrzaj
    endValues['Naslov'] = title
    endValues['Autor'] = autor.replace("Autor:\n", " ")
    endValues['Datum'] = datum
    for i in range(0,num_com):
        if num_com == 0:
            break
        endValues['Autor komentara'] = comment["data"][i]["from"]["name"]
        endValues['Komentar'] = comment["data"][i]["message"]

    title=title.replace("- Jutarnji.hr", "")

    rbr+=1

    article = open("jutarnji-" + datum + "-" + `rbr` +".txt", "w")

    print(json.dumps(endValues,  ensure_ascii=False))
    article.write("Naslov:\n%s\n" % title.encode('utf8'))
    article.write("Objavljeno: %s\n" % datum)
    article.write("%s" % autor.encode('utf8'))
    article.write("Sadrzaj:\n%s\n\n" % sadrzaj.encode('utf8'))
    article.close()

    comment_file = open("jutarnji-" + datum + "-" + `rbr` +"-komentari.txt", "w")
    for i in range(0,num_com):
        if num_com == 0:
            break
        comment_file.write("Autor komentara:\n%s\n\n" % comment["data"][i]["from"]["name"].encode('utf8'))
        comment_file.write("Komentar:\n%s\n\n" % comment["data"][i]["message"].encode('utf8'))
    comment_file.close()

def parseSearch(tag, page):

    scrapedIDs = []
    searchURL = "http://www.jutarnji.hr/search.do?searchString=" + tag + "&timePeriod=2015&publishDate=&publicationId=1&newPhrase=&method=navigate&pageNumber=" + `page` #http://www.jutarnji.hr/search.do?timePeriod=2015&publishDate=&newPhrase=&publicationId=1&searchString=izbjeglice
    r = requests.get(searchURL)
    data = r.text
    clanci = []
    #ids = []
    soup = BeautifulSoup(data, "html.parser")
    linkovi = soup.find_all('a', class_='black')
    if not linkovi:
        flag=False
        return

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

idevi=[]
tags = [line.rstrip('\n') for line in open('tagovi.txt')]

for tag in tags:
    flag=True
    page=0
    while(flag):
        page+=1
        idevi+=parseSearch(tag, page)
        #text_file = open("Output.txt", "w")
        if page == 3:
            break

for rad in idevi:
    parseRad(rad)
    time.sleep(2)
#text_file.close()