import cv2
import numpy as np


class TagDetector(object):

    def __init__(self,path):
        self.path = path

    def detect_tags(self):
        image = cv2.imread(self.path)
        #grayscale 
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        #binary 
        ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
        #dilation 
        kernel = np.ones((1,1), np.uint8) 
        img_dilation = cv2.dilate(thresh, kernel, iterations=1)
        #find contours 
        ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        #sort contours 
        sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[1])

        threshImage = cv2.imread(self.path,0)
        threshImage = cv2.medianBlur(threshImage,5)
        aGaussThreshold = cv2.adaptiveThreshold(threshImage.copy(), 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

        data = []
        locations = []
        #new_img = None
        idx = 0
        for i, ctr in enumerate(sorted_ctrs):
            x, y, w, h = cv2.boundingRect(ctr)
            if(cv2.contourArea(ctr) > 100):
                roi = aGaussThreshold[y:y+h, x:x+w]
                cv2.imwrite("tmp.png",roi)
                new_img = cv2.imread("tmp.png")
                new_img = cv2.resize(new_img,(120 ,80))
                #koordinatlar
                locations.append([x,y,x+w,y+h])
                data.append(new_img)
                idx += 1
        data = np.array(data, dtype = 'float32')
        locations = np.array(locations)
        
        data /= 255
        return data, locations

    def draw_rectange(self, result, locations):
        image = cv2.imread(self.path)
        indis = 0
        for i in range(0, len(result)):
            j = int(result[i,0])
            cv2.rectangle(image, (locations[j,0], locations[j,1]), (locations[j,2], locations[j,3]),(0,255,0),2)
            cv2.putText(image,result[i,1],(locations[j,0], locations[j,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, 127)
        cv2.imshow("Original Image",image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()