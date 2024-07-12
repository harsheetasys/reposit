import cx_Oracle
import json
# Connect to the Oracle database
dsn = cx_Oracle.makedsn('localhost', 1521, 'orcl')
conn = cx_Oracle.connect(user='system', password='anweshagoel', dsn=dsn)

# Create a cursor object
cursor = conn.cursor()

# Create the movies table
#cursor.execute('CREATE TABLE movies (id NUMBER PRIMARY KEY,title VARCHAR2(255),release_year NUMBER,rating NUMBER(3,1),duration NUMBER(3),genres VARCHAR2(4000),directors VARCHAR2(4000),cast VARCHAR2(4000));')

# Insert some sample data into the movies table
sample_data = [
    (1, 'The Shawshank Redemption', 1994, 9.2, 142, json.dumps(['Drama']), json.dumps(['Frank Darabont']), json.dumps(['Tim Robbins', 'Morgan Freeman'])),
    (2, 'The Godfather', 1972, 9.2, 175, json.dumps(['Crime', 'Drama']), json.dumps(['Francis Ford Coppola']), json.dumps(['Marlon Brando', 'Al Pacino'])),
    (3, 'The Dark Knight', 2008, 9.0, 152, json.dumps(['Action', 'Crime', 'Drama']), json.dumps(['Christopher Nolan']), json.dumps(['Christian Bale', 'Heath Ledger'])),
    (4, 'Pulp Fiction', 1994, 8.9, 154, json.dumps(['Crime', 'Drama']), json.dumps(['Quentin Tarantino']), json.dumps(['John Travolta', 'Samuel L. Jackson'])),
    (5, 'The Lord of the Rings: The Return of the King', 2003, 8.9, 201, json.dumps(['Action', 'Adventure', 'Drama', 'Fantasy']), json.dumps(['Peter Jackson']), json.dumps(['Elijah Wood', 'Ian McKellen'])),
    (6, 'Inception', 2010, 8.8, 148, json.dumps(['Action', 'Adventure', 'Sci-Fi']), json.dumps(['Christopher Nolan']), json.dumps(['Leonardo DiCaprio', 'Joseph Gordon-Levitt'])),
    (7, 'Fight Club', 1999, 8.8, 139, json.dumps(['Drama']), json.dumps(['David Fincher']), json.dumps(['Brad Pitt', 'Edward Norton'])),
    (8, 'Forrest Gump', 1994, 8.8, 142, json.dumps(['Drama', 'Romance']), json.dumps(['Robert Zemeckis']), json.dumps(['Tom Hanks', 'Robin Wright'])),
    (9, 'The Matrix', 1999, 8.7, 136, json.dumps(['Action', 'Sci-Fi']), json.dumps(['Lana Wachowski', 'Lilly Wachowski']), json.dumps(['Keanu Reeves', 'Laurence Fishburne'])),
    (10, 'The Silence of the Lambs', 1991, 8.6, 118, json.dumps(['Crime', 'Drama', 'Thriller']), json.dumps(['Jonathan Demme']), json.dumps(['Jodie Foster', 'Anthony Hopkins'])),
    (11, 'Schindler\'s List', 1993, 8.9, 195, json.dumps(['Biography', 'Drama', 'History']), json.dumps(['Steven Spielberg']), json.dumps(['Liam Neeson', 'Ralph Fiennes'])),
    (12, 'Goodfellas', 1990, 8.7, 146, json.dumps(['Crime', 'Drama']), json.dumps(['Martin Scorsese']), json.dumps(['Robert De Niro', 'Ray Liotta'])),
    (13, 'The Green Mile', 1999, 8.6, 189, json.dumps(['Crime', 'Drama', 'Fantasy']), json.dumps(['Frank Darabont']), json.dumps(['Tom Hanks', 'Michael Clarke Duncan'])),
    (14, 'Se7en', 1995, 8.6, 127, json.dumps(['Crime', 'Drama', 'Mystery']), json.dumps(['David Fincher']), json.dumps(['Morgan Freeman','Brad Pitt'])),
    (21, 'The Matrix', 1999, 8.7, 136, json.dumps(['Action', 'Sci-Fi']), json.dumps(['Lana Wachowski', 'Lilly Wachowski']), json.dumps(['Keanu Reeves', 'Laurence Fishburne'])),
    (22, 'Inception', 2010, 8.8, 148, json.dumps(['Action', 'Adventure', 'Sci-Fi']), json.dumps(['Christopher Nolan']), json.dumps(['Leonardo DiCaprio', 'Joseph Gordon-Levitt'])),
    (23, 'Interstellar', 2014, 8.6, 169, json.dumps(['Adventure', 'Drama', 'Sci-Fi']), json.dumps(['Christopher Nolan']), json.dumps(['Matthew McConaughey', 'Anne Hathaway'])),
    (24, 'Fight Club', 1999, 8.8, 139, json.dumps(['Drama']), json.dumps(['David Fincher']), json.dumps(['Brad Pitt', 'Edward Norton'])),
    (25, 'The Dark Knight Rises', 2012, 8.4, 164, json.dumps(['Action', 'Crime', 'Drama']), json.dumps(['Christopher Nolan']), json.dumps(['Christian Bale', 'Tom Hardy'])),
    (26, 'The Prestige', 2006, 8.5, 130, json.dumps(['Drama', 'Mystery', 'Sci-Fi']), json.dumps(['Christopher Nolan']), json.dumps(['Christian Bale', 'Hugh Jackman'])),
    (27, 'The Departed', 2006, 8.5, 151, json.dumps(['Crime', 'Drama', 'Thriller']), json.dumps(['Martin Scorsese']), json.dumps(['Leonardo DiCaprio', 'Matt Damon'])),
    (28, 'Shutter Island', 2010, 8.2, 138, json.dumps(['Drama', 'Mystery', 'Thriller']), json.dumps(['Martin Scorsese']), json.dumps(['Leonardo DiCaprio', 'Mark Ruffalo'])),
    (29, 'The Wolf of Wall Street', 2013, 8.2, 180, json.dumps(['Biography', 'Crime', 'Drama']), json.dumps(['Martin Scorsese']), json.dumps(['Leonardo DiCaprio', 'Jonah Hill'])),
    (30, 'The Revenant', 2015, 8.0, 156, json.dumps(['Action', 'Adventure', 'Drama']), json.dumps(['Alejandro G. Iñárritu']), json.dumps(['Leonardo DiCaprio', 'Tom Hardy'])),
    (31, 'The Social Network', 2010, 8.0, 120, json.dumps(['Biography', 'Drama']), json.dumps(['David Fincher']), json.dumps(['Jesse Eisenberg', 'Andrew Garfield'])),
    (32, 'Gone Girl', 2014, 8.1, 149, json.dumps(['Drama', 'Mystery', 'Thriller']), json.dumps(['David Fincher']), json.dumps(['Ben Affleck', 'Rosamund Pike'])),
    (33, 'The Martian', 2015, 8.0, 141, json.dumps(['Adventure', 'Drama', 'Sci-Fi']), json.dumps(['Ridley Scott']), json.dumps(['Matt Damon', 'Jessica Chastain']))]

cursor.executemany("""
INSERT INTO movies (id, title, release_year, rating, duration, genres, directors, cast)
VALUES (:id, :title, :release_year, :rating, :duration, :genres, :directors, :cast)
""", sample_data)

# Commit the changes
conn.commit()

# Close the cursor and connection objects
cursor.close()
conn.close()