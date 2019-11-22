import os

import pandas as pd
import numpy as np
from scipy import stats

from flask import Flask, jsonify, render_template,redirect, request
from flask_sqlalchemy import SQLAlchemy
from sklearn import model_selection
import pickle
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

app = Flask(__name__)                                                                                                               

with open(f'LogisticOverSample.sav', "rb") as f:
    model = pickle.load(f)
with open(f'logistic_regression_scaler.pickle', "rb") as f2:
    scaler = pickle.load(f2)
with open(f'RandomForest.sav', "rb") as f3:
    model2 = pickle.load(f3)

# feature_names = model.get_booster().feature_names


@app.route("/", methods=["GET", "POST"])
def index():
    """Return the homepage."""
    output_message = ""
    # loaded_model = pickle.load(open('LogisticOverSample.sav', 'rb'))
    print(model)
    if request.method == "POST":
        PropertyState = "PropertyState_" +(request.form["PropertyState"])
        #Make a list of states and loop through to create a variable for each state
        state_list = ['OR', 'OH', 'CA', 'IL', 'WI', 'AL', 'MI', 'FL', 'NY', 'AZ', 'NE', \
       'NM', 'MN', 'AR', 'TN', 'NJ', 'WV', 'GA', 'NC', 'CT', 'NH', 'OK', \
       'UT', 'VA', 'MO', 'MS', 'WA', 'LA', 'TX', 'IA', 'PA', 'IN', 'ME', \
       'KY', 'SD', 'MA', 'AK', 'CO', 'MT', 'ND', 'NV', 'MD', 'SC', \
       'ID', 'KS', 'DE', 'PR', 'VT', 'DC', 'RI']
        PropertyStateDict = {}
        for state in state_list:
            var_name = "PropertyState_"+state
            if PropertyState == state:
                PropertyStateDict[var_name] = 1
            else :
                PropertyStateDict[var_name] = 0
        locals().update(PropertyStateDict)

        SellerName2 = "SellerName_" +(request.form["SellerName2"])
        SellerName3 = SellerName2.replace(" ","").replace(",","").replace(".","")
        #Make a list of Seller Names and loop through to create a variable for each
        SellerNameList = ["LAKEVIEWLOANSERVICINGLLC","WELLSFARGOBANKNA","FLAGSTARBANKFSB"]
        SellerNameDict = {}
        for seller in SellerNameList :
            var_name = "SellerName2_"+seller
            if SellerName3 == seller:
                print("var_name =",var_name) 
                SellerNameDict[var_name] = 1
            else: 
                # var_name = "blah"
                SellerNameDict[var_name] = 0
        locals().update(SellerNameDict)
        # print(SellerNameDict)
        # print(SellerNameDict[SellerName2_FLAGSTARBANKFSB])

        OriginalInterestRate = float(request.form["OriginalInterestRate"])
        OriginalUPB = (request.form["OriginalUPB"])
        OriginalLoanTerm = (request.form["OriginalLoanTerm"])
        OriginalLoanToValueLTV = (request.form["OriginalLoanToValueLTV"])
        PrimaryMortgageInsurancePercent = (request.form["PrimaryMortgageInsurancePercent"])
        OriginalDebtToIncomeRatio = float(request.form["OriginalDebtToIncomeRatio"])
        NumberofBorrowers = (request.form["NumberofBorrowers"])
        FirstTimeHomeBuyerIndicator = (request.form["FirstTimeHomeBuyerIndicator"])
        BorrowerCreditScoreAtOrigination = (request.form["BorrowerCreditScoreAtOrigination"])
        CoBorrowerCreditScoreAtOrigination = (request.form["CoBorrowerCreditScoreAtOrigination"])
        LoanAge = (request.form["LoanAge"])

        col_list = ['OriginalInterestRate', 'OriginalUPB', 'OriginalLoanTerm',\
       'OriginalLoanToValueLTV', 'PrimaryMortgageInsurancePercent',\
       'OriginalDebtToIncomeRatio', 'NumberofBorrowers',\
       'FirstTimeHomeBuyerIndicator', 'BorrowerCreditScoreAtOrigination',\
       'CoBorrowerCreditScoreAtOrigination', 'LoanAge',\
        'SellerName2_FLAGSTAR BANK, FSB',\
        'SellerName2_LAKEVIEW LOAN SERVICING, LLC',\
       'SellerName2_WELLS FARGO BANK, N.A.', 'PropertyState_AK',\
       'PropertyState_AL', 'PropertyState_AR', 'PropertyState_AZ',\
       'PropertyState_CA', 'PropertyState_CO', 'PropertyState_CT',\
       'PropertyState_DC', 'PropertyState_DE', 'PropertyState_FL',\
       'PropertyState_GA', 'PropertyState_IA', 'PropertyState_ID',\
       'PropertyState_IL', 'PropertyState_IN', 'PropertyState_KS',\
       'PropertyState_KY', 'PropertyState_LA', 'PropertyState_MA',\
       'PropertyState_MD', 'PropertyState_ME', 'PropertyState_MI',\
       'PropertyState_MN', 'PropertyState_MO', 'PropertyState_MS',\
       'PropertyState_MT', 'PropertyState_NC', 'PropertyState_ND',\
       'PropertyState_NE', 'PropertyState_NH', 'PropertyState_NJ',\
       'PropertyState_NM', 'PropertyState_NV', 'PropertyState_NY',\
       'PropertyState_OH', 'PropertyState_OK', 'PropertyState_OR',\
       'PropertyState_PA', 'PropertyState_PR', 'PropertyState_RI',\
       'PropertyState_SC', 'PropertyState_SD', 'PropertyState_TN',\
       'PropertyState_TX', 'PropertyState_UT', 'PropertyState_VA',\
       'PropertyState_VT', 'PropertyState_WA', 'PropertyState_WI',\
       'PropertyState_WV']


        list_of_things = [OriginalInterestRate,OriginalUPB, OriginalLoanTerm,\
        OriginalLoanToValueLTV, PrimaryMortgageInsurancePercent,\
        OriginalDebtToIncomeRatio, NumberofBorrowers,\
        FirstTimeHomeBuyerIndicator, BorrowerCreditScoreAtOrigination,\
        CoBorrowerCreditScoreAtOrigination, LoanAge]
        list_of_banks = [SellerNameDict[key] for key in SellerNameDict.keys()]
        list_of_states = [PropertyStateDict[key] for key in PropertyStateDict.keys() ]
        list_of_things2 = list_of_things +list_of_banks + list_of_states
        # list_of_things.append(list_of_states)

        data = pd.DataFrame(np.array([list_of_things2]), columns=col_list)

        scaled = scaler.transform(data)
        result = model.predict(scaled)
        result2= model2.predict(data)
        if result == 1:
            output_message1 = "Logistic regression says you will default"
        else:
            output_message1 = "Logistic regression says you will not default"  

        if result2 == 1:
            output_message2 = "Random Forest says you will default"
        else:
            output_message2 = "Random Forest says you will not default"  
        output_message= output_message1+"&"+output_message2  
    
    return render_template("indexModel.html", message = output_message)




if __name__ == "__main__":
    #when you upload to heroku, take out debug
    app.run(debug = True, port = 5044)
    # app.run()
