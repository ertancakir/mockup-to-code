import sys
sys.path.insert(0,'./src')

from flask import Flask

from model import DeepModel
from detection import TagDetector
from code_creator import CodeCreator


app = Flask(__name__)

@app.route('/')
def index():
    model = DeepModel()

    train_data, train_labels_one_hot, test_data, test_labels_one_hot = model.load_data()
    model.load_weight()
    return "Index Page"