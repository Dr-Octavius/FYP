# model.py
from enum import Enum
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

class ModelType(Enum):
    RFC = RandomForestClassifier
    LR = LogisticRegression
    SVM = SVC

def get_model_by_type(model_type):
    if model_type in ModelType:
        return model_type.value()
    else:
        raise ValueError("Unsupported model type")