from flask import Flask, request, render_template,jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def visualization():
    return render_template('graph2.html')

if __name__ == "__main__":
	app.run()

