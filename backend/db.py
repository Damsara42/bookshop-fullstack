import pyodbc

def get_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};' 
        'SERVER=DESKTOP-D91DH96\SQLEXPRESS;' 
        'DATABASE=NOVELLA;'
        'Trusted_Connection=yes;'
    )

    return conn