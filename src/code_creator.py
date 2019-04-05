# -*- coding: utf-8 -*-
import cv2
import numpy as np

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
            else:
                br_height = self.locations[i,1] - comp_rect[3]
                print(br_height)
                #Alt satırdaki yanında olmayan tagı diğerleri ile karşılaştırmak için seç
                comp_rect = self.locations[i]

                same_line_tags = np.array(same_line_tags)
                same_line_tags = same_line_tags[same_line_tags[:,0].argsort()]
                same_line_tags = same_line_tags[::-1]
                
                output += self.get_item_code(same_line_tags[:,-1])
                same_line_tags = []
                same_line_tags.append([self.locations[i,0], types[i]])
                continue

            same_line_tags = np.array(same_line_tags)
            same_line_tags = same_line_tags[same_line_tags[:,0].argsort()]
            same_line_tags = same_line_tags[::-1]
            output += self.get_item_code(same_line_tags[:,-1])

        html_output = ""
        f = open("header.html","r")
        html_output += f.read()
        f.close()
        
        html_output += output

        f = open("footer.html","r")
        html_output += f.read()
        f.close()
        
        print html_output

    def get_item_code(self, types):
        output = ""
        for t in types:
            if(t == 'Button'):
                output += "<input type='submit' value='dk923d'>"
            elif(t == 'Text'):
                output += "<input type='text'>"
            elif(t == 'Line'):
                output += "e32e23 "
            elif(t == 'Image'):
                output += "<img src='image.png' width=200 height=200>"
        
        output += "<br>"
        return output