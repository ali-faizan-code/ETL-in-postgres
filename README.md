# Summary:
This project sets and refreshes a Sparkify database and creates 5 tables on it. Then it perform ETL by extracting data from JSON song and log files from their respective directories and use python and pandas library to filter and categorizes it into our desired table columuns. After which we load the data into our 5 tables on that database using the SQL insert commands in sql_queries.py. 

# Database Design:

## Fact Table
### Table 1: songplays - records in log data associated with song plays 
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

## Dimension Tables
### Table 2: users - users in the app
user_id, first_name, last_name, gender, level

### Table 3: songs - songs in music database
song_id, title, artist_id, year, duration

### Table 4: artists - artists in music database
artist_id, name, location, latitude, longitude

### Table 5: time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday

# How To Run:
This project by simply running the pythong script in create_tables.py followed by the etl.py script.

# Files:
data - directory containing song and log JSON files for input to our ETL
create_tables.py - python script used to setup and refresh our sparkify database with 5 empty tables
etl.ipynb - used to build the etl.py script step by step
etl.py - implements our ETL algorithm
README.md - current file
run_project.ipynb - runs the create_tables.py and etl.py files in one python notebook
sql_queries - create_tables.py relies on this file to setup the database and etl.py use this file for insert queries and more
test.ipynb - used to check on the database post our run to check for records and perform sanity tests.



