from bs4 import BeautifulSoup
import requests
import lxml

#Arrays initieren
name = []
menu = []
price = []

url = 'https://www.studierendenwerk-hamburg.de/speiseplan/?t=today&l=158'
page = requests.get(url).text

soup = BeautifulSoup(page, 'lxml')
rows = soup.find("div", attrs={"class":"tx-epwerkmenu-menu-location-wrapper", "data-location":"158"})


#print(rows)
#i = 0
#for i in range(len(rows)):
#    print(rows[i])

"""
for i in range(len((rows.find_all("h5", attrs={"class":"singlemeal__headline singlemeal__headline--"})))):
    #Menü in Array platzieren
    menu.append(rows.find_all("h5", attrs={"class":"singlemeal__headline singlemeal__headline--"})[i].text.strip())


    #Ausgabe
    print(f"{i+1}-> {menu[i]}")
"""

for i in range(len((rows.find_all("div", attrs={"class":"col-12 col-lg-6 mb-4 menue-tile"})))):
    #Menü in Array platzieren
    menu.append(rows.find_all("h5", attrs={"class":"singlemeal__headline singlemeal__headline--"})[i].text.strip())

    #Preis in Array platzieren
    price.append(rows.find_all("span", attrs={"class":"singlemeal__info--semibold"})[i].text.strip())

    #Ausgabe
    print(f"{i+1}-> {menu[i]} Preis:{price[i]}") #Preis noch fehlerhaft! Allergene und Zusatzstoffe werden manchmal mit rausgezogen