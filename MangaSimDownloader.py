#! python3

import requests, os, bs4, time, sys, getpass

def separator():
    print('x-x-x-x-x-x-x-x-x-x')

#Takes your input for 'WHICH MANGA WOULD YOU LIKE TO DOWNLOAD?' and searches for it.
while True:
    searchManga = input('Which manga would you like to download? (Or type a keyword): ')
    separator()
    searchURL = 'http://mangasim.com/search/' + searchManga.replace(' ', '_')
    res = requests.get(searchURL)
    res.raise_for_status
    soupA = bs4.BeautifulSoup(res.text, 'html.parser')               #Gets the source code of SEARCH PAGE.
    chosenManga = soupA.select('h2[class="story-name"] a')           #Gets the title of the manga.
    authorName = soupA.select('div[class="story-item"] span')        #Gets the author of the manga.
    if chosenManga == []:
        print('We could not find the manga you were looking for. Try searching with another keyword.')
        separator()
        continue
    else:
        break

#Lists through all the manga on the SEARCH PAGE, showing the title and author of each option.
#Takes your input for 'IS THIS MANGA YOU'RE LOOKING FOR?' and clicks on it.
for j in range(len(chosenManga)):
    print('Title : ' + chosenManga[j].text)
    print(authorName[3*j].text)
    mangaYN = input('Is this the manga you were looking for? (Type [Y]es or [N]o): ').lower()
    separator()
    if mangaYN == 'y' or mangaYN == 'yes':
        break
    elif mangaYN == 'n' or mangaYN == 'no':
        continue
    else:
        print('Please rerun the program and type "[Y]es" or "[N]o" when prompted.')
        sys.exit()

initialTime = time.time()
website = 0
        
#Takes your input for 'BEGIN INSTALLING FROM WHICH CHAPTER?' and does it. Also, we're making folders!
chapterNo = int(input("Begin installing from which chapter? (Type a number): "))
separator()
scrapedURL = chosenManga[j].get('href')
url = scrapedURL[:20] + 'chapter/' + scrapedURL[20:] + '/chapter_%s' % chapterNo
chosenLength = len(url[:-len(str(chapterNo))])                                  #Gets the URL length, without the chapter number, which will be useful later.
newFolderName = 'C:\\Users\\%s\\Desktop\\%s' % (getpass.getuser(), chosenManga[j].text)
os.makedirs(newFolderName, exist_ok=True)                                       #Creates a main folder for the manga on your desktop.

while True:

    res = requests.get(url)
    res.raise_for_status
    soupB = bs4.BeautifulSoup(res.text, 'html.parser')          #Gets the source code of the chapter with images to download.
    imageList = soupB.select('div[class="vung_doc"] img')       #Gets a list of the links to the images.
    if website != 'manganelo':                                  #This took SO LONG LOL. It's so that the while loop won't get stuck redownloading the same chapter.
        website = 'mangasim'   
    if imageList == []:
        if website != 'manganelo':                              #This is for when mangasim.com redirects me to manganelo.com, which happens sometimes.
            scrapedURL = chosenManga[j].get('href')
            url = scrapedURL[:21] + 'chapter/' + scrapedURL[27:] + '/chapter_%s' % chapterNo
        chosenLength = len(url[:-len(str(chapterNo))])
        res = requests.get(url)
        res.raise_for_status
        soupB = bs4.BeautifulSoup(res.text, 'html.parser')
        imageList = soupB.select('div[class="vung-doc"] img')
        website = 'manganelo'
    print('Downloading from %s...' % url)
    
    #Actually downloads all the images from the source code of the chapter.
    for i in range(len(imageList)):
        newSubFolderName = newFolderName + '\\Chapter %s' % url[chosenLength:]  #Creates subfolders for each chapter within the main folder.
        os.makedirs(newSubFolderName, exist_ok=True)
        imageLink = imageList[i].get('src')                                     #Gets the individual links to the images from the list we got just now.
        res = requests.get(imageLink)
        res.raise_for_status
        fileName = 'Part %s.jpg' % (i+1)
        imageFile = open(os.path.join(newSubFolderName, fileName), 'wb')
        for chunk in res.iter_content(100000): 
            imageFile.write(chunk)                                              #Downloads the images, 100000 bytes at a time!
        imageFile.close
    
    #Goes to the next chapter until there aren't anymore, then breaks out of the loop.
    try:
        if website == 'mangasim':
            nextChapter = soupB.select('div[class="panel-btn-changes"] a')[3]
        elif website == 'manganelo':
            nextChapter = soupB.select('div[class="btn-navigation-chap"] a')[3]
        url = nextChapter.get('href')
    except IndexError:
        print('Downloaded till the latest updated chapter.')
        break

#Prints out how long it took to download all that shit.
downloadTime = time.time() - initialTime
print('The download took %s seconds.' % str(downloadTime/60))

'''
Extra features to try to implement:
-Multithreading to make it run faster
-Merging the images in one subfolder into a single PDF so that it's less messy
-How do I make the interface look like an actual program instead of me typing on the command line like a neanderthal?
-How do I make this program downloadable, like an .exe file?
'''
