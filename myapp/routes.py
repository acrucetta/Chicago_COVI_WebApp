from myapp import app
import json, plotly
from flask import render_template
from wrangling_scripts.wrangle_data import return_figures

@app.route('/')
@app.route('/index')

def index():

    figures = return_figures()

    # plot ids for the html id tag
    #ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    return render_template('index.html',figuresJSON=figuresJSON
                           
                           