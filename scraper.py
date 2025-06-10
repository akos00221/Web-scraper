from bs4 import BeautifulSoup
import urllib3
import re


http = urllib3.PoolManager()
resp = http.request("GET", "https://www.arukereso.hu/notebook-c3100/")

soup = BeautifulSoup(resp.data, "lxml")

# A notebook nevek és linkek megtalálása és eltárolása:

nevek = []
linkek = []

lista = list(soup.find_all("a", string=re.compile(".Notebook")))
for elem in lista:
    nevek.append(elem.get_text()) 
    linkek.append(elem.get_attribute_list('href')[0])

linkek = list(dict.fromkeys(linkek))

# Az árak megtalálása és eltárolása

temp = list(soup.find_all("a", class_="price")) # Ideiglenes lista: A CSS osztályok azonossága miatt eltárolja a leárazás előtti és utáni értékeket is
akcio_elotti_arak = list(soup.find_all("a", class_="price pricedrop-from"))

temp = [ar.get_text() for ar in temp]
akcio_elotti_arak = [ar.get_text() for ar in akcio_elotti_arak]

arak = []
[arak.append(ar) for ar in temp if ar not in akcio_elotti_arak] # Kizárjuk a leárazás előtti árakat

with open("laptopok.txt", "w", encoding="utf-8") as file:
    for i in range(len(nevek)):
        file.write(f"{nevek[i]}\t{arak[i]}\t{linkek[i]}\n")