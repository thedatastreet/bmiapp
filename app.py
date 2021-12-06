from flask import Flask, render_template, request
from flask_material import Material

# pip install flask flask_material pandas numpy 

# Exploratory Data Analysis Pkg import
import pandas as pd
import numpy as np

# ML Package imports
import sys
import joblib

# lookup table for messages and quotes
message_lookup = {
    0 : {'quote': 500.0,
         'message':"BMI is in right range"},
    1 : {'quote': 750.0,
         'message':"Age is between 18 to 39 and BMI is either less than 17.49 or greater than 38.5"},
    2 : {'quote': 1000.0,
         'message':"Age is between 40 to 59 and BMI is either less than 18.49 or greater than 38.5"},
    2 : {'quote': 750.0,
         'message':"Age is greater than 60 and BMI is either less than 18.49 or greater than 45.5"}
}

# Building a Flask application with Material UI
app = Flask(__name__)
Material(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=["POST"])
def analyze():
    if request.method == 'POST':
        Ins_Age = float(request.form['Ins_Age'])
        Ins_Gender = 1 if request.form['Ins_Gender']== 'Male' else 0
        Wt = float(request.form['Wt'])
        meters = float(request.form['meters'])
        BMI = round(Wt/(meters*meters),2)
        
        # Clean the data by convert from unicode to float
        sample_data = [Ins_Age, Ins_Gender, Wt, meters, BMI]
        df = pd.DataFrame([sample_data], columns=['Ins_Age','Ins_Gender','Wt','meters','BMI'])
        
        model = joblib.load('model/insurance_quote_model.pkl')
        result_prediction = model.predict(df)[0]

        quote = message_lookup[result_prediction]['quote']

        # calculate discount as per gender
        if Ins_Gender == 0:
            discount = quote * 0.1
        else:
            discount = 0 
        
        total = quote - discount

        message = message_lookup[result_prediction]['message']

    return render_template('index.html', Ins_Age=Ins_Age,
                           Ins_Gender=request.form['Ins_Gender'],
                           Wt=Wt,
                           meters=meters,
                           BMI=BMI,
                           message= message,
                           discount = discount,
                           total = total,
                           quote=quote)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
