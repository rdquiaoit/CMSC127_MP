from flask import Flask, render_template, json, request, jsonify
import json, requests
from db import connection, execute_read_query

app = Flask(__name__)

@app.route('/')
def index():
	#returns an exception if something is wrong in dataset A link
	dataset_a = requests.get('https://pomber.github.io/covid19/timeseries.json')
	if dataset_a.status_code != 200:
		raise Exception(f"Unexpected status code {dataset_a.status_code}")

	#returns an exception if something is wrong in dataset B link
	dataset_b = requests.get('https://github.com/benhur07b/covid19ph-doh-data-dump/blob/master/data-modified/case-information.csv')
	if dataset_b.status_code != 200:
		raise Exception(f"Unexpected status code {dataset_b.status_code}")

	ageGroup = execute_read_query('''
		SELECT ageGroup, count(*)
		FROM case_information 
		GROUP BY `ageGroup`
		''')
	ageLabel = json.dumps( [x[0] for x in ageGroup] )
	ageData = json.dumps( [x[1] for x in ageGroup] )

	regProvRes = execute_read_query('''
		SELECT regProvRes, count(*)
		FROM case_information 
		GROUP BY `regProvRes`
		''')
	regProvResLabel = json.dumps( [x[0] for x in regProvRes] )
	regProvResData = json.dumps( [x[1] for x in regProvRes] )

	sex = execute_read_query('''
		SELECT sex, count(*)
		FROM case_information 
		GROUP BY `sex`
		''')
	sexLabel = json.dumps( [x[0] for x in sex] )
	sexData = json.dumps( [x[1] for x in sex] )

	muniCityRes = execute_read_query('''
		SELECT muniCityRes, count(*)
		FROM case_information 
		GROUP BY `muniCityRes`
		''')
	muniCityResLabel = json.dumps( [x[0] for x in muniCityRes] )
	muniCityResData = json.dumps( [x[1] for x in muniCityRes] )

	return render_template('datasetb.html',
		ageLabel = ageLabel,
		ageData = ageData,
		regProvResLabel = regProvResLabel,
		regProvResData = regProvResData,
		sexLabel = sexLabel,
		sexData = sexData,
		muniCityResLabel = muniCityResLabel,
		muniCityResData = muniCityResData)
	

@app.route('/data')
def data():
	req = requests.get('https://pomber.github.io/covid19/timeseries.json')
	values = req.json()
	return (values)


if __name__ == '__main__':
	app.run(debug=True)
