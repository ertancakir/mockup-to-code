import numpy as np

class PageList(object):

    def __init__(self, page_names ,html_codes, images):
        self.page_names = page_names
        self.html_codes = html_codes
        self.images = images

    def getImages(self):
        return self.images

    def getPageNames(self):
        return self.page_names
    
    def getHtmlCodes(self):
        return self.html_codes