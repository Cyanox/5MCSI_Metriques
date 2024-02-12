from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

# Maj repo
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')


@app.route('/paris/')
def meteo():
    response = urlopen(
        'https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15  # Conversion de Kelvin en °c
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)


@app.route('/commits/')
def get_commits():
    url = 'https://api.github.com/repos/Cyanox/5MCSI_Metriques/commits'
    response = urlopen(url)
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    commit_minutes = {}
    for commit in json_content:
        commit_time = datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
        minute = commit_time.minute
        commit_minutes[minute] = commit_minutes.get(minute, 0) + 1

    results = [{'minute': minute, 'commits': count} for minute, count in commit_minutes.items()]

    return jsonify(results=results)

# https://api.github.com/repos/Cyanox/5MCSI_Metriques/commits
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route("/commits/")
def mescommits():
    return render_template("commits.html")




if __name__ == "__main__":
    app.run(debug=True)
