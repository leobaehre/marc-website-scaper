from zipfile import ZipFile
from bs4 import BeautifulSoup
import requests
import os

# 4799

counter = 0

pages = 45

if not os.path.exists("output"):
    os.mkdir("output")

# make abc, def, ghi, jkl, mno, pqr, stu, vw, xyz folders
folderNames = ["abc", "def", "ghi", "jkl", "mno", "pqr", "stu", "vw", "xyz"]
for folderName in folderNames:
    if not os.path.exists("output/" + folderName):
        os.mkdir("output/" + folderName)

for page in range(1, pages):

    print("Page: " + str(page) + "/" + str(pages))

    mainPage = requests.get(
        "https://www.vera-groningen.nl/photos/page/" + str(page) + "/?category=marc-de-krosse&lang=nl")
    mainSoup = BeautifulSoup(mainPage.content, 'html.parser')

    itemDiv = mainSoup.find("div", {"class": "row blocks-12 equal-height"})
    items = itemDiv.find_all("div", {"class": "col-xs-60"})

    for item in items[1:]:
        imgDiv = item.find("a", {"class": "link-wrap"})

        textPart = item.find("div", {"class": "text-part"})
        teaser = textPart.find("div", {"class": "teaser"}).text

        url = imgDiv.find("div", {"class": "image"})["style"].split("'")[1]
        link = imgDiv["href"]
        title = textPart.find("div", {"class": "block-title"}).text
        date = teaser.split(", ")[1]

        title = title.replace(":", "%colon%")
        title = title.replace("?", "%question%")

        date = date.replace("/", "-").replace(" ", "")

        folderName = title + ", " + date

        thumbnailRequest = requests.get(url, allow_redirects=True)

        itemPage = requests.get(link)
        itemSoup = BeautifulSoup(itemPage.content, 'html.parser')

        itemDiv = itemSoup.find("div", {"class": "row bg-white"})
        items = itemDiv.find_all("div", {"class": "col-xs-60"})

        images = []

        imageCounter = 0

        for imageItem in items[1:]:
            imgDiv = imageItem.find("div", {"class": "image"})
            url = imgDiv["style"].split("'")[1]
            counter += 1
            imageCounter += 1
            r = requests.get(url, allow_redirects=True)
            print("image: " + str(imageCounter) + " count: " + str(counter))
            images.append(r.content)

        # get folder name alphabet
        folderNameAlphabet = folderName[0].lower()

        for folder in folderNames:
            if folderNameAlphabet in folder:
                parentFolder = folder
                break

        zipfile = ZipFile('output/' + parentFolder + '/' + folderName + '.zip', 'w')
        zipfile.writestr("thumbnail.jpg", thumbnailRequest.content)

        for i in range(len(images)):
            zipfile.writestr(str(i) + ".jpg", images[i])

        zipfile.close()

        print("zipped: " + folderName + ".zip" + " in " + parentFolder + " folder")