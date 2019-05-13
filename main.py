# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'./src')

from model import DeepModel
from detection import TagDetector
from code_creator import CodeCreator


if __name__ == "__main__":

    res = 0
    model = DeepModel()

    train_data, train_labels_one_hot, test_data, test_labels_one_hot = model.load_data()
    model.load_weight()
    while res != 4:
        print("1 - Train")
        print("2 - Test")
        print("3 - Resimi Koda Dönüştür")
        print("4 - Çıkış")
        res = int(raw_input("----------> "))
        if res == 1:
            model.train_model(train_data, train_labels_one_hot)
        elif res == 2:
            model.test_model(test_data, test_labels_one_hot)
        elif res == 3:
            path = ""
            path += "./samples/"
            path += str(raw_input("Path : "))
            detector = TagDetector(path)
            data, locations = detector.detect_tags()
            
            result, locations = model.predict(data,locations)

            code_creator = CodeCreator(locations, result)
            code_creator.create_code()
            detector.draw_rectange(result,locations)
        
        

    
    