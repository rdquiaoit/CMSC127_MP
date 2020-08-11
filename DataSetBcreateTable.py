import pandas as pd
import mysql.connector
from mysql.connector import Error

#CSV to Pandas Dataframe
url = "https://raw.githubusercontent.com/benhur07b/covid19ph-doh-data-dump/master/data-modified/case-information.csv"
data = pd.read_csv(url, error_bad_lines = False)
df = pd.DataFrame(data, columns = ['CaseCode', 'Age', 'AgeGroup', 'Sex', 'DateRepConf', 'DateRecover', 
	'DateDied', 'RemovalType', 'DateRepRem', 'Admitted', 'RegProvRes', 'MuniCityRes'])

#Modifications to the Dataframe for empty cells
df['Age'] = df['Age'].fillna(6969)
df = df.fillna("None")


#Creation of new database
connection = mysql.connector.connect(
                    host= "localhost",
                    user= "root",
                    passwd= ""
                    )
cursor = connection.cursor()

command = "CREATE DATABASE covid19ph_db"
cursor.execute(command)

#Creation of table
connection = mysql.connector.connect(
                    host= "localhost",
                    user= "root",
                    passwd= "",
                    database= "covid19ph_db"
                    )
cursor = connection.cursor()

command = '''
	CREATE TABLE case_information (
	caseCode VARCHAR(10),
	age INT,
	ageGroup VARCHAR(50),
	sex VARCHAR(10),
	regProvRes VARCHAR(50),
	muniCityRes VARCHAR(50)
	)
'''
cursor.execute(command)

#DataFrame to Table
for row in df.itertuples():
	command = f'''
		INSERT INTO case_information (caseCode, age, ageGroup, sex, regProvRes, muniCityRes)
		VALUES ("{row.CaseCode}", {row.Age}, "{row.AgeGroup}", "{row.Sex}", "{row.RegProvRes}", "{row.MuniCityRes}")
		'''
	cursor.execute(command)
	connection.commit()

print("Transfered to the database successfully!")