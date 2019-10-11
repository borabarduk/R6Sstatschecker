import traceback
from configparser import ConfigParser

class Screenshotchecker(object):

    def __init__(self,config):

        self._url = config['DATA']['Url']

if __name__ == "__main__":

    try:

        # Initialize objects
        config = ConfigParser()
        config.read("config.cfg") # Config file contains session and address id information which is essential for requests

        checker  = Screenshotchecker(config)

    except:
        traceback.print_exc()