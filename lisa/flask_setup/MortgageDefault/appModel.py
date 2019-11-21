import os

import pandas as pd
import numpy as np
from scipy import stats

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)                                                                                                               


@app.route("/")
def index():
    """Return the homepage."""
    from sklearn import model_selection
    import pickle
    loaded_model = pickle.load(open('LogisticOverSample.sav', 'rb'))
    print(loaded_model)

    # result = loaded_model.score(X_test, y_test)
    # print(result)
    return render_template("indexModel.html")

if __name__ == "__main__":
    #when you upload to heroku, take out debug
    app.run(debug = True, port = 5044)
    # app.run()
