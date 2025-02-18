from flask import Flask, render_template,request
from wrangling_scripts.wrangle_data import return_figures
import json
import plotly

app = Flask(__name__)

@app.route('/')
def home():

    figures = return_figures()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)

@app.route('/phases')
def phases():
    figures = return_figures()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('phases.html', ids=ids,figuresJSON=figuresJSON)

if __name__ == '__main__':
    app.debug = True
    app.run()
