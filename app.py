# import packages 
import flask
import pandas as pd
import pickle
import numpy as np
import warnings

from datetime import datetime

warnings.filterwarnings("ignore")

# import model
with open('covid_model.pkl', 'rb') as file:

    covid_model = pickle.load(file)


app = flask.Flask(__name__, template_folder="templates")

@app.route("/", methods=['GET', 'POST'])

def main():

    if flask.request.method == 'GET':
        return flask.render_template("index.html", result_covid=0)

    if flask.request.method == 'POST':

        # check what was inputing
        user_inputs = {
            "sexo": flask.request.form["sexo"],
            "idade": flask.request.form["idade"],
            "febre": flask.request.form["febre"],
            "tosse": flask.request.form["tosse"],
            "falta_ar": flask.request.form["falta_ar"],
            'dor_garganta': flask.request.form["dor_garganta"],
            'outros': flask.request.form["outros"]
            }

        # features_names = [['sexo','idade','febre','tosse','falta_ar','dor_garganta','outros']]

        # dataframe blank
        df = pd.DataFrame([user_inputs], columns=['sexo','idade','febre','tosse','falta_ar','dor_garganta','outros'])

        #
        df.replace({'sexo':{'F':0, 'M':1}}, inplace=True)
        df.replace({'febre':{'N':0, 'S':1}}, inplace=True)
        df.replace({'tosse':{'N':0, 'S':1}}, inplace=True)
        df.replace({'falta_ar':{'N':0, 'S':1}}, inplace=True)
        df.replace({'dor_garganta':{'N':0, 'S':1}}, inplace=True)
        df.replace({'outros':{'N':0, 'S':1}}, inplace=True)

        df = df.astype(int)

        #var_sexo = int(df[['sexo']].iloc[0].values)
        #var_idade = int(df[['idade']].iloc[0].values)
        #var_febre = int(df[['febre']].iloc[0].values)
        #var_tosse = int(df[['tosse']].iloc[0].values)
        #var_falta_ar = int(df[['falta_ar']].iloc[0].values)
        #var_dor_garganta = int(df[['dor_garganta']].iloc[0].values)
        #var_outros = int(df[['outros']].iloc[0].values)

        # make prevision
        y_pred = float(covid_model.predict(df)[0])

        if y_pred == 1:
            result = "Possivelmente Sim"
        else:
            result = "Possivelmente Não"

        return flask.render_template("index.html", result_covid=result)

if __name__ == "__main__":
   port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
