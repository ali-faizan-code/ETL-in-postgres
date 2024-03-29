import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description: This function is responsible for reading the given song data file,
    filter for the necessary columns for song data and artist data and inserting
    that data into their respective tables on the database.

    Arguments:
        cur: the cursor object.
        filepath: song data file path.
    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df.filter(["song_id","title","artist_id","year","duration"]).values.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df.filter(["artist_id", "artist_name", "artist_location", "artist_latitude",  "artist_longitude"]).values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: This function is responsible for reading the given log data file,
    obtaining and converting the timestamp data into columns for the time table, 
    filtering for the necessary columns for user and songplays data and inserting
    that data into their respective tables on the database.

    Arguments:
        cur: the cursor object.
        filepath: log data file path.
    Returns:
        None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"]=="NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit='ms')
    
    # insert time data records
    time_data = [df["ts"],t.dt.hour,t.dt.day,t.dt.week,t.dt.month,t.dt.year,t.dt.weekday]
    column_labels = ("TimeStamp","Hour","Day","Week","Month","Year","Weekday")
    time_df = pd.DataFrame(
    {column_labels[0]: time_data[0],
     column_labels[1]: time_data[1],
     column_labels[2]: time_data[2],
     column_labels[3]: time_data[3],
     column_labels[4]: time_data[4],
     column_labels[5]: time_data[5],
     column_labels[6]: time_data[6],
    })

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.filter(["userId", "firstName", "lastName", "gender", "level" ])

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts,row.userId,row.level,songid, artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description: This function is responsible for getting all files from the given filepath,
    iterating over each one using the appropiate process function and commiting any changes
    to the database.
    
    Arguments:
        cur: the cursor object.
        conn: connection to the database used to commit
        filepath: directory file path.
        func: function to be used on the files in directory
    Returns:
        None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    - executes the process data function for ingesting data from song and log files
    - Closes the connection. 
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()