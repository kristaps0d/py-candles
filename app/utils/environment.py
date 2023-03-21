import os, dotenv

class Environment(object):
    def __init__(self):
        dotenv.load_dotenv()

    def getenv(self, key):
        return os.getenv(key)