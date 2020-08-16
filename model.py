from wtforms import Form, FloatField, BooleanField, StringField,validators
from math import pi

class InputForm(Form):
    M = StringField('Method (kmeans, Iso, SVM)', [validators.Length(min=3, max=6)])
    S = StringField('Sensor (co2_1, temp_1, dew_1, relH_1)', [validators.Length(min=5, max=6)])
        
    