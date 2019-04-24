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
        
        same_line_tags.append([comp_rect[0], 0 ,types[0]]) #[x, tag_indis,type]
        all_tags = []

        for i in range(1, len(self.result)- 1):
            #Taglar yanyana mı?
            if(comp_rect[3] > self.locations[i,1]):
                widht = self.locations[i,2] - self.locations[i,0]
                heigth = self.locations[i,3] - self.locations[i,1]
                same_line_tags.append([self.locations[i,0], i ,types[i]])
                continue
            
            #Alt satırdaki yanında olmayan tagı diğerleri ile karşılaştırmak için seç
            comp_rect = self.locations[i]

            same_line_tags = np.array(same_line_tags)
            same_line_tags = same_line_tags[same_line_tags[:,0].argsort()]
            same_line_tags = same_line_tags[::-1]
                
            all_tags.append(same_line_tags)
            same_line_tags = []
            same_line_tags.append([self.locations[i,0], i ,types[i]])
            
        all_tags.append(same_line_tags)

        tag_x_location = 0
        tag_y_location = 0
        all_tags = np.array(all_tags)
        html = Html()

        for line_tags in all_tags:
            idx = 0
            hr_heigth = 0
            for tags in line_tags:
                tag_indis = int(tags[1])
                tag_type = str(tags[2])

                if(idx == 0):
                    if(tag_y_location != 0):
                        hr_heigth = self.locations[tag_indis,1] - tag_y_location
                    tag_y_location = self.locations[tag_indis,3]
                idx += 1
                
                if(tag_x_location != 0):
                    padding = self.locations[tag_indis,0] - tag_x_location
                    print padding
                    output += html.get_padding(padding)

                tag_x_location = self.locations[tag_indis,2]
                tag_y_location = self.locations[tag_indis,3]
                widht = self.locations[tag_indis,2] - self.locations[tag_indis,0]
                heigth = self.locations[tag_indis,3] - self.locations[tag_indis,1]
                if(tag_type == 'Button'):
                    output += html.get_button(widht,heigth,"123123")
                elif(tag_type == 'Text'):
                    output += html.get_textbox(widht,heigth)
                elif(tag_type == 'Line'):
                    output += html.get_text("asdasdasd")
                elif(tag_type == 'Image'):
                    output += html.get_image(widht,heigth)
            
            tag_x_location = 0
            output += html.get_hr(hr_heigth)
        
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