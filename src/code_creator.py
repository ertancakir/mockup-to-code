# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np
from html_tags import Html

class CodeCreator(object):
    def __init__(self, locations, result):
        self.locations = locations
        self.result = result
        
    def create_code(self):
        
        output = ""
        types = self.result[:,-1]
        comp_rect = self.locations[0]
        same_line_tags = []
        same_line_tags.append([self.locations[0,0], types[0]])
        br_height = 0
        for i in range(1, len(self.result)):
            #Taglar yanyana mı?
            if(comp_rect[3] > self.locations[i,1]):
                same_line_tags.append([self.locations[i,0], types[i]])
                continue
            else:
                br_height = self.locations[i,1] - comp_rect[3]
                #Alt satırdaki yanında olmayan tagı diğerleri ile karşılaştırmak için seç
                comp_rect = self.locations[i]

                same_line_tags = np.array(same_line_tags)
                same_line_tags = same_line_tags[same_line_tags[:,0].argsort()]
                same_line_tags = same_line_tags[::-1]
                
                output += self.get_item_code(same_line_tags[:,-1], br_height)
                same_line_tags = []
                same_line_tags.append([self.locations[i,0], types[i]])
                continue

            same_line_tags = np.array(same_line_tags)
            same_line_tags = same_line_tags[same_line_tags[:,0].argsort()]
            same_line_tags = same_line_tags[::-1]
            output += self.get_item_code(same_line_tags[:,-1])

        
        html_output = ""
        path = os.path.join("web","header.html")
        f = open(path,"r")
        html_output += f.read()
        f.close()
        
        html_output += output

        path = os.path.join("web","footer.html")
        f = open(path,"r")
        html_output += f.read()
        f.close()
        

        f = open("output.html", "w")
        f.write(html_output)
        f.close()
        

    def get_item_code(self, types, br_height):
        output = ""
        html = Html()
        for t in types:
            if(t == 'Button'):
                output += html.get_button(100,40,"123123")
            elif(t == 'Text'):
                output += html.get_textbox(100,40)
            elif(t == 'Line'):
                output += "e32e23"
            elif(t == 'Image'):
                output += html.get_image(200,200)
        
        br = "<hr style='height:{}pt; visibility:hidden;' />"
        output += br.format(br_height)
        return output