import traceback
import webbrowser
from configparser import ConfigParser
from PIL import Image,ImageOps
from pytesseract import image_to_string

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


if __name__ == "__main__":

    try:

        # Initialize objects
        config = ConfigParser()
        config.read("config.cfg") # Config file contains session and address id information which is essential for requests

        checker  = Screenshotchecker(config)
        processedIMG = checker.preprocess()
        names = checker.extractPlayers(processedIMG)
        checker.openBrowserTabs(names)


    except:
        traceback.print_exc()