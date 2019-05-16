# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np
from html_tags import Html

class CodeCreator(object):
    def __init__(self, locations, result, name):
        self.locations = locations
        self.result = result
        self.name = name

    def is_between(self, line1, line2):
        if((line2[0] < line1[1] and line2[0] > line1[0]) or line1[0] == line2[0]):
            return True
        return False
        
    def create_code(self):
        html = Html()

        output = ""
        types = self.result[:,-1]
        
        #y ekseninde en üstteki tag ı ekle
        between_tags = [[self.locations[0,0],0]]
        all_tags = []

        #y1 ve y2 koordinatları
        tag1 = [self.locations[0,1], self.locations[0,3]]
        tag2 = []
        for i in range(0,len(types)):
            if(i + 1 < len(types)):
                l = self.locations[i + 1]
                tag2 = [l[1],l[3]]
                if(self.is_between(tag1,tag2)):
                    between_tags.append([l[0], i + 1])
                else:
                    between_tags = np.array(between_tags)
                    between_tags = between_tags[between_tags[:,0].argsort()]
                    all_tags.append(between_tags)
                    between_tags = []
                    between_tags = [[self.locations[i + 1,0], i + 1]]
                tag1 = [l[1],l[3]]
        
        if between_tags is not None:
            all_tags.append(between_tags)

        all_tags = np.array(all_tags)
        y_value = 0
        for b_tags in all_tags:
            b_tags = np.array(b_tags)
            x_value = 0
            for j in b_tags[:,1]:
                location = self.locations[j]
                t = types[j]
                output += html.get_padding(location[0] - x_value)
                output += html.get_tag(t,location)
                x_value = location[0]
            
            output += html.get_hr(location[3] - y_value)
            y_value = location[3]

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
        
        output_name = str(self.name) + ".html"
        path = os.path.join("./outputs",output_name)
        f = open(path, "w")
        f.write(html_output)
        f.close()