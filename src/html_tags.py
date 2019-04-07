# -*- coding: utf-8 -*-
import os
import numpy as np

class Html(object):

    def __init__(self):
        self.html_output = ""

    def get_button(self, width, height, text):
        button = "<button class='btn btn-info' style='height:{}px;width:{}px'>{}</button>"
        return button.format(height, width, text)

    def get_image(self, width, height):
        image = "<img src='image.png' width={} height={}>"
        return image.format(width, height)

    def get_textbox(self, width, height):
        text = "<input type='text' class='form-control' style='height:{}px;width:{}px'>"
        return text.format(height, width)