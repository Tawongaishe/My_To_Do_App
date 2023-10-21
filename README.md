
Running the backend of the app: 
1. cd tawo_to_do into the top level directory
2. FLASK_APP=run.py
3. flask run 

Some issues
1. downloads of the login manager throws an error relating to the Werkzeug version

Kill current processes:
lsof -i :5000
kill -9 1916 