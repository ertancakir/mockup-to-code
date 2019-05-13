# -*- coding: utf-8 -*-
import os
import numpy as np
from random import *
import random
import string

class Html(object):

    def __init__(self):
        self.html_output = ""

    def get_tag(self, types, location):
        
        width = location[2]- location[0]
        height = location[3] - location[1]
        name = ""
        for i in range(0,width/10):
            name += random.choice(string.ascii_letters)
        if types == "Button":
            return self.get_button(width, height, name)
        elif types == "TextInput":
            return self.get_textInput(width, height)
        elif types == "Text":
            return self.get_text(name,height)
        elif types == "Image":
            return self.get_image(width, height)

    def get_button(self, width, height, text):
        button = "<button class='btn-sm btn btn-info' style='height:{}px;width:{}px'>{}</button>\n"
        return button.format(height, width, text)

    def get_image(self, width, height):
        image = "<img src='./web/image.png' width={} height={}>\n"
        return image.format(width, height)

    def get_text(self,text,height):
        if height > 50:
            t = "<h1>{}</h1>\n"
        else:
            t = "<span>{}</span>\n"
        return t.format(text)

    def get_textInput(self, width, height):
        text_box = "<input type='text' style='height:{}px;width:{}px'>\n"
        return text_box.format(height, width)

    def get_padding(self, width):
        width /= 3
        span = "<span style='padding-left:{}px'></span>\n"
        return span.format(width)

    def get_hr(self, height):
        height /= 3
        hr = "<hr style='height:{}px; visibility:hidden;' />\n"
        return hr.format(height)