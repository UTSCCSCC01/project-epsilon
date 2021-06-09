from flask import Flask
from flask_mysqldb import MySQL
from populatedatabase import populate

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'epsilon'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'epsilon_db'

mysql = MySQL(app)

@app.route("/")
def hello():
  return "Hello World! Welcome to Epsilon!"

# Only go to this page if your database is empty
@app.route("/create")
def create():
  populate(mysql)
  return "Database is populated!"

if __name__ == "__main__":
  app.run()