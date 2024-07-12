import cx_Oracle
import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
import speech_recognition as sr

# Connect to Oracle database
dsn = cx_Oracle.makedsn('localhost', 1521, 'orcl')
conn = cx_Oracle.connect(user='system', password='anweshagoel', dsn=dsn)

# Create SQLAlchemy engine
engine = create_engine('oracle+cx_oracle://system:anweshagoel@localhost:1521/?service_name=orcl')

try:
    # Read sample data from Oracle database
    query = """
    SELECT id, title, genres, directors, cast
    FROM movies
    """
    movies = pd.read_sql(query, engine)

    # Preprocess data
    movies['genres'] = movies['genres'].apply(lambda x: x.split(','))
    movies['directors'] = movies['directors'].apply(lambda x: x.split(','))
    movies['cast'] = movies['cast'].apply(lambda x: x.split(','))
    movies['data'] = movies[['title', 'genres', 'directors', 'cast']].apply(lambda x: ' '.join(map(str, x)), axis=1)

    # Vectorize data
    vectorizer = CountVectorizer()
    vectorized = vectorizer.fit_transform(movies['data'])

    # Calculate cosine similarity
    similarities = cosine_similarity(vectorized)

    # Define a function to get recommendations for a movie
    def get_recommendations(movie_id):
        movie_index = movies[movies['id'] == movie_id].index[0]
        similarity_scores = list(enumerate(similarities[movie_index]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        print(similarity_scores[:5])
        recommendations = [movies.iloc[i]['title'] for i, _ in similarity_scores[1:]]
        return recommendations

    # Define a function to display movie details
    def display_movie_details(movie_id):
        selected_movie = movies[movies['id'] == movie_id].iloc[0]
        details_label.config(text=f"Title: {selected_movie['title']}\nGenres: {', '.join(selected_movie['genres'])}\nDirectors: {', '.join(selected_movie['directors'])}\nCast: {', '.join(selected_movie['cast'])}")

    # Define a function to display recommendations in a Tkinter window
    def display_recommendations(movie_id):
        recommendations = get_recommendations(movie_id)[:5]  # Limit to 5 recommendations
        recommendations_text.delete('1.0', 'end')
        recommendations_text.insert('end', '\n'.join(recommendations))


    # Define a function to handle movie selection from the dropdown menu
    def on_movie_dropdown_select(*args):
        movie_id = movies[movies['title'] == selected_movie_id.get()]['id'].values[0]
        display_recommendations(movie_id)
        display_movie_details(movie_id)

    def on_movie_button_click(movie_id):
        display_recommendations(movie_id)
        display_movie_details(movie_id)

    # Define a function to handle speech recognition
    def recognize_speech():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            # Check if the recognized text matches any movie title
            movie_title = text.lower()
            if movie_title in movies['title'].str.lower().values:
                movie_id = movies[movies['title'].str.lower() == movie_title]['id'].values[0]
                on_movie_button_click(movie_id)
            else:
                recommendations_text.delete('1.0', 'end')
                recommendations_text.insert('end', "Movie not found.")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    # Create a Tkinter window
    root = tk.Tk()
    root.title('Movie Recommendation System')
#using configure
    root.configure(bg="gray27")

    
    # Create a dropdown menu for movie selection
    selected_movie_id = tk.StringVar(root)
    movie_options = [movie_title for movie_title in movies['title']]
    movie_dropdown = tk.OptionMenu(root, selected_movie_id, *movie_options)
    movie_dropdown.pack()

    # Bind the dropdown selection event to the function
    selected_movie_id.trace('w', on_movie_dropdown_select)

    # Create a text widget to display recommendations
    recommendations_text = tk.Text(root, height=5, width=50, bg='cadetblue')
    recommendations_text.pack()

    # Create a label to display movie details
    details_label = tk.Label(root, text="")
    details_label.pack()

    # Create a button for speech recognition
    speech_button = tk.Button(root, text="Speak", command=recognize_speech)
    speech_button.pack()

    # Run the Tkinter event loop
    root.mainloop()

finally:
    # Close the Oracle database connection
    conn.close()
