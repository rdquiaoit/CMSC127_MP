import pandas as pd
import mysql.connector
from mysql.connector import Error

def create_database():
    connection = mysql.connector.connect(
                        host= "localhost",
                        user= "root",
                        passwd= ""
                        )
    cursor = connection.cursor()
    cursor.execute ("SHOW DATABASES LIKE 'covid19ph_db'")
    db_result = cursor.fetchall()
    if db_result == []:
        # creates a new database 
        command = "CREATE DATABASE covid19ph_db"
        cursor.execute(command)
        print("Database 'covid19ph_db' created.")
    else:
        print("The database 'covid19ph_db' already exists")


def transfer_data():
    create_database()
    connection = mysql.connector.connect(
                        host= "localhost",
                        user= "root",
                        passwd= "",
                        database= "covid19ph_db"
                        )
    cursor = connection.cursor()

    cursor.execute("SHOW TABLES LIKE 'case_information'")
    table_result = cursor.fetchall()
    if table_result == []:
        # creates a new table
        print("Creating table 'case_information' to database 'covid19ph_db'") 
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
        print("Table 'case_information' created.")
    else:
        print("The table 'case_information' already exists")

    #CSV to Pandas Dataframe
    print("Acquiring data from source...")
    url = "https://raw.githubusercontent.com/benhur07b/covid19ph-doh-data-dump/master/data-modified/case-information.csv"
    data = pd.read_csv(url, error_bad_lines = False)
    df = pd.DataFrame(data, columns = ['CaseCode', 'Age', 'AgeGroup', 'Sex', 'DateRepConf', 'DateRecover', 
        'DateDied', 'RemovalType', 'DateRepRem', 'Admitted', 'RegProvRes', 'MuniCityRes'])

    #Modifications to the Dataframe for empty cells
    df['Age'] = df['Age'].fillna(6969)
    df = df.fillna("None")

    #DataFrame to Table
    print("Transferring data to database...")
    for row in df.itertuples():
        command = f'''
            INSERT INTO case_information (caseCode, age, ageGroup, sex, regProvRes, muniCityRes)
            VALUES ("{row.CaseCode}", {row.Age}, "{row.AgeGroup}", "{row.Sex}", "{row.RegProvRes}", "{row.MuniCityRes}")
            '''
        cursor.execute(command)
    
    connection.commit()

    print("Transferred to the database successfully!")

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    while True:
        try:
            connection = mysql.connector.connect(
                        host=host_name,
                        user=user_name,
                        passwd=user_password,
                        database=db_name
                        )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
            print("Creating database...")
            transfer_data()
            continue
        break
    return connection


def execute_query(query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

connection = create_connection("localhost", "root", "","covid19ph_db")
