#flask app

from flask import Flask, render_template
from datetime import datetime
from create_figure import script, div, cdn_js, cdn_css, bv
from ts_plotting import script2, div2
import requests

#instantiate the flask app
app = Flask(__name__)

#create index page function
@app.route("/",methods=['GET','POST'])
def index():
    return render_template("index.html",script=script, script2= script2, div=div, div2=div2, cdn_js=cdn_js, cdn_css=cdn_css, bv=bv)

#run the app
if __name__ == "__main__":
    app.run(port=33507, debug=True)
