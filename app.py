# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 23:12:51 2021

@author: sambi
"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('Seoul_Bike_Sharing_Demand.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():  
    Seasons_Summer=0
    if request.method == 'POST':
        Hour = int(request.form['Hour'])
        Temperature = float(request.form['Temperature'])
        Humidity=int(request.form['Humidity'])
        Wind_speed=float(request.form['Wind_speed'])
        Visibility=int(request.form['Visibility'])
        Dew_point_temperature =float(request.form['Dew_point_temperature'])
        Solar_Radiation=float(request.form['Solar_Radiation'])
        Rainfall=float(request.form['Rainfall'])
        Snowfall=float(request.form['Snowfall'])
        Seasons_Spring=request.form['Seasons_Spring']
        
        
        if(Seasons_Spring=='Spring'):
            Seasons_Spring=1
            Seasons_Summer=0
            Seasons_Winter=0
        elif(Seasons_Spring == 'Summer'):
            Seasons_Spring=0
            Seasons_Summer=1
            Seasons_Winter=0
        elif(Seasons_Spring == 'Winter'):
            Seasons_Spring=0
            Seasons_Summer=0
            Seasons_Winter=1
        else:
            Seasons_Spring=0
            Seasons_Summer=0
            Seasons_Winter=0
            
        Holiday_No_Holiday=request.form['Holiday_No_Holiday']
        if(Holiday_No_Holiday=='No'):
            Holiday_No_Holiday=1
        else:
            Holiday_No_Holiday=0	
        Functioning_Day_Yes=request.form['Functioning_Day_Yes']
        if(Functioning_Day_Yes=='Yes'):
            Functioning_Day_Yes=1
        else:
            Functioning_Day_Yes=0
        
        
        prediction=model.predict([[Hour, Temperature, Humidity, Wind_speed,Visibility, Dew_point_temperature, Solar_Radiation, Rainfall,Snowfall, Seasons_Spring, Seasons_Summer,Seasons_Winter, Holiday_No_Holiday, Functioning_Day_Yes]])
        output=round(prediction[0],2)
        if (output<0):
            return render_template('index.html',prediction_texts="No need of bikes today, and this is quite rare")
        else:
            return render_template('index.html',prediction_texts="Looking at all the features and constraints, we need {} numbers of bikes at this hour of the day in Seoul".format(int(output)))
    else:
        return render_template('index.html')
        
    
if __name__=="__main__":
    app.run(debug=True)