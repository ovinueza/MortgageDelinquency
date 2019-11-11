import os

import pandas as pd
import numpy as np
from scipy import stats

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
# import VaxRegression

app = Flask(__name__)


#################################################
# Database Setup
#################################################

postgresURI = "postgres://postgres:~Data2020$@canuezadb.ckvuctle6mvr.us-east-2.rds.amazonaws.com:5432/canueza"
                                                                                                                


app.config["SQLALCHEMY_DATABASE_URI"] = postgresURI
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

class Parent(Base):
    __tablename__ = 'acq'
    id = 'LoanIdentifier'
    children = relationship("Child")

class Child(Base):
    __tablename__ = 'per'
    id = 'UniqueID'
    parent_id = 'LoanIdentifier'

# Save references to each table #
acq_data = Base.classes.acq
per_data = Base.classes.per

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("indexModel.html")


@app.route("/states")
def statenames():
    """Return a list of states present in data."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(acq_data).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    # df = acq_data
    states = df["PropertyState"].unique()
    states.sort()
    # Return a list of the  states
    print(states)
    return jsonify(list(states))


@app.route("/metadata/<state>")
def state_metadata(state):
    """Return the MetaData for a given state."""
    print(state)
    selBoth = [
        acq_data.LoanIdentifier,
        acq_data.SellerName,
        acq_data.OriginalInterestRate,
        acq_data.OriginalUPB,
        acq_data.OriginalLoanTerm,
        acq_data.OriginationDate,
        acq_data.FirstPaymentDate,
        acq_data.OriginalLoanToValueLTV,
        acq_data.PrimaryMortgageInsurancePercent,
        acq_data.OriginalDebtToIncomeRatio,
        acq_data.NumberofBorrowers,
        acq_data.FirstTimeHomeBuyerIndicator,
        acq_data.BorrowerCreditScoreAtOrigination,
        acq_data.PropertyState,
        acq_data.ZipCodeShort,
        acq_data.CoBorrowerCreditScoreAtOrigination,
        per_data.UniqueID,
        per_data.MonthlyReportingPeriod,
        per_data.LoanAge,
        per_data.RemainingMonthstoMaturity,
        per_data.AdjustedMonthstoMaturity,
        per_data.MaturityDate,
        per_data.MetropolitanStatisticalAreaMSA,
        per_data.CurrentLoanDelinquencyStatus,
        per_data.ForeclosureDate
    ]
    results = db.session.query(*selBoth).filter(acq_data.LoanIdentifier == per_data.LoanIdentifier, acq_data.PropertyState==state).all()

    # results = db.session.query(*selBoth).filter(acq_data.PropertyState==state).all()

    # Create alist of dictionaries for each row of metadata information
    loanItems = []
    
    for result in results:
        state_metadata = {}
        state_metadata["LoanIdentifier"] = result[0]
        state_metadata["SellerName"] = result[1]
        state_metadata["OriginalInterestRate"] = str(result[2])
        state_metadata["OriginalUPB"] = result[3]
        state_metadata["OriginalLoanTerm"] = result[4]
        state_metadata["OriginationDate"] = result[5]
        state_metadata["FirstPaymentDate"] = result[6]
        state_metadata["OriginalLoanToValueLTV"] = result[7]
        state_metadata["PrimaryMortgageInsurancePercent"] = str(result[8])
        state_metadata["OriginalDebtToIncomeRatio"] = result[9]
        state_metadata["NumberofBorrowers"] = result[10]
        state_metadata["FirstTimeHomeBuyerIndicator"] = result[11]
        state_metadata["BorrowerCreditScoreAtOrigination"] = result[12]
        state_metadata["PropertyState"] = result[13]
        state_metadata["ZipCodeShort"] = result[14]
        state_metadata["CoBorrowerCreditScoreAtOrigination"] = result[15]
        state_metadata["PerformanceIdentifier"] = result[16]
        state_metadata["MonthlyReportingPeriod"] = result[17]
        state_metadata["LoanAge"] = result[18]
        state_metadata["RemainingMonthstoMaturity"] = result[19]
        state_metadata["AdjustedMonthstoMaturity"] = result[20]
        state_metadata["MaturityDate"] = result[21]
        state_metadata["MetropolitanStatisticalAreaMSA"] = result[22]
        state_metadata["CurrentLoanDelinquencyStatus"] = result[23]
        state_metadata["ForeclosureDate"] = result[24]
        loanItems.append(state_metadata)

    return jsonify(loanItems)

#create route for hazard model data
@app.route("/model/hazard/<state>")
def hazardfit(state):
    """Returns the hazard model of a chosen state."""

    #pull and merge vaccination and life expectancy data
    selTest = [
        acq_data.LoanIdentifier,
        acq_data.SellerName,
        acq_data.OriginalInterestRate,
        acq_data.OriginalUPB,
        acq_data.OriginalLoanToValueLTV,
        acq_data.PropertyState,
        per_data.LoanAge,
        per_data.CurrentLoanDelinquencyStatus
    ]

    session =Session(db.engine)
    testResult = session.query(*selTest).filter(acq_data.LoanIdentifier == per_data.LoanIdentifier, acq_data.PropertyState==state).all()
    session.close()

    #organize the list of tuples into a collection of list an zip into a dataframe
    stateTup = []
    OriginalInterestRateTup = []
    LoanAgeTup = []
    for tup in testResult:
        stateTup.append(tup[5])
        OriginalInterestRateTup.append(float(tup[2]))
        LoanAgeTup.append(tup[6])
    tup_df = pd.DataFrame(zip(stateTup, OriginalInterestRateTup, LoanAgeTup), columns = ["PropertyState","OriginalInterestRate","LoanAge"])

    #remove missing data
    test_df = tup_df.dropna()
    print("In the hazard app")
    #define series for regresion analysis
    int_rate = test_df["OriginalInterestRate"]
    age = test_df["LoanAge"]
    #regress life_exp = m*age + b
    test_slope, test_int, test_r, test_p, test_std_err = stats.linregress(
        age, int_rate)
    test_fit = test_slope * age + test_int
    print(f"slope ${test_slope} and intercept ${test_int}")
    #collect regression results in a dictionary
    result = {
    "age": age.to_list(),
    "int_rate": int_rate.to_list(),
    "test_slope": test_slope, 
    "test_int": test_int, 
    "test_r": test_r, 
    "test_p": test_p, 
    "test_std_err": test_std_err,
    "test_fit": test_fit.to_list(),
   }
    return jsonify(result)

# #create route for hazard model data
# @app.route("/model/logisticreg/<state>")
# def logitfit(state):
#     """Returns the logistic regression model of a chosen state."""

#     #pull and merge acquisition and performance data
#     selTest = [
#         acq_data.LoanIdentifier,
#         acq_data.SellerName,
#         acq_data.OriginalInterestRate,
#         acq_data.OriginalUPB,
#         acq_data.OriginalLoanToValueLTV,
#         acq_data.PropertyState,
#         per_data.LoanAge,
#         per_data.CurrentLoanDelinquencyStatus
#     ]

#     session =Session(db.engine)
#     testResult = session.query(*selTest).filter(acq_data.LoanIdentifier == per_data.LoanIdentifier, acq_data.PropertyState==state).all()
#     session.close()

#     #organize the list of tuples into a collection of list an zip into a dataframe
#     stateTup = []
#     OriginalInterestRateTup = []
#     LoanAgeTup = []
#     for tup in testResult:
#         stateTup.append(tup[5])
#         OriginalInterestRateTup.append(tup[2])
#         LoanAgeTup.append(tup[6])
#     tup_df = pd.DataFrame(zip(stateTup, OriginalInterestRateTup, LoanAgeTup), columns = ["PropertyState","OriginalInterestRate","LoanAge"])

#     #define X and y
#     test_df = tup_df.dropna()

#     #split data into test and train
#     from sklearn.model_selection import train_test_split
#     X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)

#     #Create logistic regression model and fit training data
#     from sklearn.linear_model import LogisticRegression
#     classifier = LogisticRegression(C = 1e9)
#     classifier.fit(X_train, y_train)
#     train_score = classifier.score(W_train, y_train)
#     test_score = classifier.score(X_test, y_test)


#     #calculate summary statisics of train and test data

#     #define series for regresion analysis
#     int_rate = test_df["OriginalInterestRate"]
#     age = test_df["LoanAge"]
#     #regress life_exp = m*age + b
#     test_slope, test_int, test_r, test_p, test_std_err = stats.linregress(
#         age, int_rate)
#     test_fit = test_slope * age + test_int

#     #collect regression results in a dictionary
#     result = {
#     "age": age.to_list(),
#     "int_rate": int_rate.to_list(),
#     "test_slope": test_slope, 
#     "test_int": test_int, 
#     "test_r": test_r, 
#     "test_p": test_p, 
#     "test_std_err": test_std_err,
#     "test_fit": test_fit.to_list(),
#    }
#     return jsonify(result)


if __name__ == "__main__":
    #when you upload to heroku, take out debug
    app.run(debug = True, port = 5044)
    # app.run()
