from flask import Flask, render_template, request
from markupsafe import escape
from config import binary_col, state_city, abbrev_to_us_state, weather_map, weather_types
import pickle
from datetime import datetime
import pandas as pd
app = Flask(__name__)

def predict_severity(temperatureF=65, visibility=10, hour=12, day_of_week=0, month=1, city="Miami", weather_cond="cloudy", twilight=0):
    """
    Input:
        temperatureF: input a number， default = 65
        visibility(mi): input a number, default = 10
        hour: input a number (0-23)
        day_of_week: input a number, (0-6)
        month: input a number, (1-12)
        City: choose a city (top 20 frequenct cities), map the city str to a number by the loaded city_dict
        Weather Condition: choose, I used 14 weather conditoins for training, will use dictionary to map some waeather conditions
        twilight: 0 means Day, 1 means Night
        city_dict: load city_dict.pkl
        scaler: load scaler.pkl
        model: load clf_dtc.pkl
        
    Set some features with default value, don't provide dropdown menu.
        Humidity(%): default = 68
        Pressure(in): default = 28
        Wind_Speed(mph): default = 5
        
    Output:
        Severity: 1, 2, 3, 4
    """
    with open('static/city_dict.pkl', 'rb') as f:
        city_dict = pickle.load(f)
    with open('static/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('static/clf_dtc.pkl', 'rb') as f:
        model = pickle.load(f)

    humidity = 68
    pressure = 28
    wind_speed = 5
    
    num_feature = 25
    X_input = [0] * num_feature
    
    #Here are the features (some features have been encoded)
    #index 0 - 8:  ['Temperature(F)', 'Humidity(%)', 'Pressure(in)', 'Visibility(mi)', 'Wind_Speed(mph)', 'hour', 'day_of_week', 'month', 'City', 
    #index 9 - 17:   'WC_Clear', 'WC_Cloudy', 'WC_Fair', 'WC_Fair / Windy', 'WC_Fog', 'WC_Haze', 'WC_Heavy Rain', 'WC_Light Rain', 'WC_Light Snow', 
    #index 18 - 22:  'WC_Mostly Cloudy', 'WC_Overcast', 'WC_Partly Cloudy', 'WC_Rain', 'WC_Scattered Clouds',
    #index 23 - 24:  'Clight_Day', 'Clight_Night']
    
    # 0: 'Temperature(F)'
    X_input[0] = temperatureF
    
    # 1: 'Humidity(%)'
    X_input[1] = humidity
    
    # 2: 'Pressure(in)'
    X_input[2] = pressure
    
    # 3: 'Visibility(mi)'
    X_input[3] = visibility
    
    # 4: 'Wind_Speed(mph)'
    X_input[4] = wind_speed
    
    # 5: 'hour'
    X_input[5] = hour
    
    # 6: 'day_of_week'
    X_input[6] = day_of_week
    
    # 7: 'month'
    X_input[7] = month
    
    # 8: 'City'
    X_input[8] = city_dict[city]

    #map the dropdown menu to my one-hot encoded featuers
    #9 - 22, weather condition
    X_input[weather_types.index(weather_cond)+9] = 1
    
    #23 - 24
    if twilight == 0: 
        X_input[23] = 1 #Day
    else: 
        X_input[24] = 1 #Night
    
    X_input2D = [X_input]
    #normalize the X
    X_scaled = scaler.transform(X_input2D)
    
    #predict severity
    y = model.predict_proba(X_scaled)
    
    return y

def model_bi(data, month, day_of_week, time):
    enc = pickle.load(open('static/enc_binary.sav','rb'))
    rf_clf = pickle.load(open('static/rf_binary.sav', 'rb'))    
    input_bi = {}
    # input_bi['weather_type'] = weather_map.get(data['weather'],'Cold')
    input_bi['weather_type'] = weather_map.get(data.get('weather', 'Cold'),'Cold')
    # input_bi['weather_severit'] = data['weather_lvl']
    input_bi['weather_severit'] = data.get('weather_lvl', 'Light')
    input_bi['month'] = month
    input_bi['day_of_week'] = day_of_week
    if 5<=time<11:
        time='morning'
    elif 11<=time<17:
        time='afternoon'
    elif 17<=time<23:
        time='night'
    else:
        time = 'mid_night'
    input_bi['part_of_day'] = time
    risk_bi_state = {}

    for state in state_city.keys():
        input_bi['State'] = state
        input_bi_df = pd.DataFrame([input_bi])
        input_bi_df = input_bi_df[binary_col]
        input_bi_df = enc.transform(input_bi_df)
        risk_bi_state[abbrev_to_us_state[state]] = rf_clf.predict_proba(input_bi_df)[0][1]/10
    return risk_bi_state

@app.route("/", methods=['GET', "POST"])
def map():
    data = request.form
    print(data)
    
    city = data.get('city','Talladega')
    # state = data['state']
    state = data.get('state', 'TX')
    # date = datetime.fromisoformat(data['date'])
    date = datetime.fromisoformat(data.get('date', "2022-04-15"))
    month = date.month
    day_of_week = date.weekday()    
    # time = int(data['time'][:2])
    time = int(data.get('time', "18:00")[:2])
    risk_bi = model_bi(data, month, day_of_week, time)   

    # temp = data['temperature']
    # visi = data['visibility']
    # weat = data['weather']
    temp = data.get('temperature', '65')
    visi = data.get('visibility', '10')
    weat = data.get('weather', 'Rain')
    y = predict_severity(temperatureF=temp, 
                        visibility=visi, 
                        hour=time, 
                        day_of_week=day_of_week, 
                        month=month, 
                        city=city, 
                        weather_cond=weat, 
                        twilight=0)[0]
    severity = {
        'level 1': y[0],
        'level 2': y[1],
        'level 3': y[2],
        'level 4': y[3],
    }
    return render_template(
        'choropleth.html', 
        risk_bi = risk_bi, 
        state_city = state_city, 
        severity = severity,
        city = city,
        state = abbrev_to_us_state[state],
        weather_types=weather_types
        )

if __name__ == '__main__':
    app.debug = True
    app.run(port = 5001)
