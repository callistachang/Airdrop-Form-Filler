#! python3

import requests, os, bs4, time

chapterNo = int(input("Begin installing from which chapter?: "))
url = 'http://mangasim.com/chapter/citrus_saburo_uta/chapter_%s' % chapterNo
chosenLength = len(url[:-len(str(chapterNo))]) #no. of characters in url except chapter. no
os.makedirs('Citrus', exist_ok=True)
initialTime = time.time()

while True:

    #Analyze the chapter's code.
    print('Downloading from %s...' % url)
    res = requests.get(url)
    res.raise_for_status

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    imageList = soup.select('div[class="vung_doc"] img')

    #Download all the images from the chapter's code.
    for i in range(len(imageList)):
        newFolderName = 'C:\\Users\\waitw\\Desktop\\Python Adventures\\Citrus\\Chapter %s' % url[chosenLength:]
        os.makedirs(newFolderName, exist_ok=True)
        imageLink = imageList[i].get('src')
        res = requests.get(imageLink)
        res.raise_for_status()
        fileName = 'Part %s.jpg' % (i+1)
        imageFile = open(os.path.join(newFolderName, fileName), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close

    #Go to the next chapter.
    try:
        nextChapter = soup.select('div[class="panel-btn-changes"] a')[3]
        url = nextChapter.get('href')
    except IndexError:
        print('Downloaded till the latest updated chapter.')
        break

downloadTime = time.time() - initialTime
print(downloadTime)

'''
Extra features to try to implement:
-Multithreading
-Merging the images from one chapter into a single PDF
'''
