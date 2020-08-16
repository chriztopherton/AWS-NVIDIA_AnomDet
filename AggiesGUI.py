from model import InputForm

from flask import Flask, flash, redirect, render_template, request, session, abort
import matplotlib.pylab as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
from pathlib import Path
import time
import os
import dash
import dash_html_components as html
import sys

from data import *
from compute import anomaly_det

app = Flask(__name__)


try:
    template_name = sys.argv[1]
except IndexError:
    template_name = 'view'

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tables")
def show_tables():
    #rows = request.args['rows']
    return render_template( template_name + '.html',tables=[weekdayData_scaled[['co2_1', 'temp_1', 'dew_1','relH_1']].head(20).to_html(classes='data')], titles=weekdayData_scaled[['co2_1', 'temp_1', 'dew_1','relH_1']].columns.values)

@app.route("/viz",methods=['GET', 'POST'])
def method():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = anomaly_det(form.M.data, form.S.data)
    else:
        result = None
    return render_template( 'options.html',
                           form=form, result=result)


if __name__ == "__main__":
    app.run(debug=True)