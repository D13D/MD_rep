#Imports
from bs4 import BeautifulSoup
import requests
from datetime import datetime

#Config
amount = 5 #Anzahl an ausgegebenen Zugverbindungen

#Filter
t_ice = 0 #ICE-Züge
t_ic_ec = 0 #Intercity- und Eurocityzüge
t_interregio = 0 #Interregio- und Schnellzüge
t_nah = 1 #Nahverkehr, sonstige Züge
t_sbahn = 1 #S-Bahn
t_bus = 0 #Busse
t_ferry = 0 #Schiffe
t_ubahn = 0 #U-Bahn
t_tram = 0 #Straßenbahn
t_taxi = 0 #Anruf-Sammeltaxi

#-----------------------------------------------------

#Arrays initiieren
rows = []
j_time = []
j_platform = []
j_destination = []
j_train = []
j_delay = []

#Aktuelle Zeit
time = datetime.now().strftime("%H:%M")
date = datetime.now().strftime("%d.%m.%y")

#Zugriffs-URL
url = f"https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=4327&country=DEU&protocol=https:&rt=1&input=Hamburg-Heimfeld%238006749&time={time}&date={date}&ld=4327&productsFilter={t_ice}{t_ic_ec}{t_interregio}{t_nah}{t_sbahn}{t_bus}{t_ferry}{t_ubahn}{t_tram}{t_taxi}&start=1&boardType=dep&"
#url = f"https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=43151&country=DEU&protocol=https:&rt=1&input=Neum%FCnster%238000271&time={time}&date={date}&ld=4327&productsFilter={t_ice}{t_ic_ec}{t_interregio}{t_nah}{t_sbahn}{t_bus}{t_ferry}{t_ubahn}{t_tram}{t_taxi}&start=1&boardType=dep&"

#Request an URL
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

#Überprüfen, ob überhaupt Züge fahren
if soup.find("p",attrs={"class":"errormsg"}):
    print(soup.find("p",attrs={"class":"errormsg"}).text)
else:

    #Abfahrtstabelle finden
    table = soup.find("table",attrs={"class":"result stboard dep"})
    i = 0
    print("## DEBUG ##")
    print("-- Success Messages --")
    for i in range(amount+1):
        if table.find("tr", attrs={"id":f"journeyRow_{i}"}):
            rows.append(table.find("tr", attrs={"id":f"journeyRow_{i}"}))
            print(f"-> success_{i}")


    # Informationen raussuchen und in Arrays packen
    for i in range(len(rows)):
        
        #Abfahrtszeit [j_time]
        j_time.append(rows[i].find("td", attrs={"class":"time"}).string)
        
        #Endbahnhof [j_destination]
        class_route = rows[i].find("td", attrs={"class":"route"})
        j_destination.append(class_route.find("a").string.replace("\n", ""))
        
        #Bahnsteig [j_platform]
        class_platform = rows[i].find("td", attrs={"class":"platform"})
        if class_platform.find("strong"):
            j_platform.append(class_platform.find("strong").string)
        else:
            j_platform.append("|-|")
        
        #Zug [j_train]
        j_train.append(rows[i].text.split()[1] + rows[i].text.split()[2])

        #Verspätung [j_delay]
        class_delay = rows[i].find("td", attrs={"class":"ris"})
        if class_delay.find("span"):
            j_delay.append(class_delay.find("span").text)
        else:
            j_delay.append(j_time[i])

            
    #Ausgabe
    print("\n")
    print("## AUSGABE ##")
    print("-- Datum & Uhrzeit --")
    print(f"{date} - {time}")
    print("")
    print("-- Abfahrten --")
    for i in range(len(rows)):
        print(f"{j_time[i]} - {j_train[i]} nach {j_destination[i]} von Gleis {j_platform[i]} - Aktuelles: {j_delay[i]}")



from tkinter import *    # Python 2.7 "from Tkinter import *"
from tkinter import ttk  # Python 2.7 "import ttk"
from PIL import Image, ImageTk
from urllib.request import urlopen


mainWin = Tk()
#for i in range(len(rows)):
    #ausgabe = "Test"
ausgabe = f"{j_time[1]} - {j_train[1]} nach {j_destination[1]} von Gleis {j_platform[1]} - Aktuelles: {j_delay[1]}\n"
label_1 = ttk.Label(mainWin, justify=LEFT, anchor="w", text=ausgabe).grid()
    #label_2 = ttk.Label(mainWin, text = "\n").pack()

"""
url_image = "https://ssl.gstatic.com/onebox/weather/64/sunny.png"
u = urlopen(url_image)
raw_data = u.read()
u.close()

photo = ImageTk.PhotoImage(data=raw_data)
label = ttk.Label(image=photo)
label.image = photo
label.pack()
"""

mainWin.mainloop()