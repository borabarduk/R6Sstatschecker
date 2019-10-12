import traceback
import webbrowser
from configparser import ConfigParser
from PIL import Image,ImageOps
from pytesseract import image_to_string, pytesseract
#If running on windows
pytesseract.tesseract_cmd = """C:/Program Files/Tesseract-OCR/tesseract.exe"""
import requests
from bs4 import BeautifulSoup

class Screenshotchecker(object):

    def __init__(self,config):

        self._url = config['DATA']['Url']
        self._img = config['DATA']['Image']


    def preprocess(self):

        try:
            im = ImageOps.invert(Image.open(self._img))
            print("Image is loaded")

            width, height = im.size
            # Setting the points for cropped image
            left = 470
            top = 300
            right = 950
            bottom = 880
            playernameIMG = im.crop((left, top, right, bottom))


            return playernameIMG

        except:
            print("Image is not loaded")

    def extractPlayers(self,preprocessedIMG):

        names = image_to_string(preprocessedIMG).split("\n")
        filteredList = list(filter(None, names))
        return names


    def openBrowserTabs(self,names):

        for name in names:
            webbrowser.open(self._url.format(name), autoraise=True)

    def printSummaryView(self,names):

        for name in names:
            try:
                res = requests.get(self._url.format(name))
                html_page = res.content
                soup = BeautifulSoup(html_page)
                stats = soup.findAll("div", {"class": "trn-defstat__value"})
                level = stats[0].text.replace('\n','').strip()
                wins = stats[5].text.replace('\n','').strip()
                wlratio = stats[6].text.replace('\n','').strip()
                kdratio = stats[8].text.replace('\n','').strip()
                topops = ','.join( [x['title'] for x in stats[4].findAll()])
                time = stats[21].text.replace('\n','').strip()
                statStr = "Player Name:{}\nLVL:{} WINS:{} WL:{} KD:{} TOP:{} TIME: {}\n-------------\n"
                print(statStr.format(name,level,wins,wlratio,kdratio,topops,time))
            except:
                print( (name, '?') [name == '']  + ' not found\n')



if __name__ == "__main__":

    try:

        # Initialize objects
        config = ConfigParser()
        config.read("config.cfg") # Config file contains session and address id information which is essential for requests

        checker  = Screenshotchecker(config)
        processedIMG = checker.preprocess()
        names = checker.extractPlayers(processedIMG)

        # checker.openBrowserTabs(names)
        checker.printSummaryView(names)
        print("Completed successfully")

    except:
        traceback.print_exc()