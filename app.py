from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
from flask import send_file
import os

app = Flask(__name__)

movie_data = []
word_freq_data = []

# Load movie data from CSV
with open('df.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        movie_data.append(row)

# Load word frequency data from another CSV (wordfreq.csv)
with open('wordfreq.csv', 'r') as wordfreq_file:
    wordfreq_reader = csv.DictReader(wordfreq_file)
    for row in wordfreq_reader:
        word_freq_data.append(row)

def get_matching_movies(dialogue):
    # Find the first movie that matches the dialogue text
    first_matching_movie = next((movie for movie in movie_data if dialogue.lower() == movie['Text'].lower()), None)

    # If a matching movie is found, return all movies with the same movie name or movie index
    if first_matching_movie:
        matching_movies = [movie for movie in movie_data if movie['Movie_Name'] == first_matching_movie['Movie_Name']]
        return matching_movies
    else:
        return []

def get_word_frequency(movie_name):
    word_frequency = []
    with open('wordfreq.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['Movie_Name'] == movie_name:
                word_frequency.append(row['Word'])
    return word_frequency[:50]  # Limit to the first 50 words


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dialogue = request.form.get('dialogue')
        if dialogue:
            # Redirect to /result route with dialogue parameter in the URL
            #return redirect(url_for('result', dialogue=dialogue))
            return redirect(url_for('prac3', dialogue=dialogue))
    return render_template('index.html')

def get_matching_movie(dialogue):
    # Find the first movie that matches the dialogue text
    return next((movie for movie in movie_data if dialogue.lower() == movie['Text'].lower()), None)

@app.route('/result', methods=['GET', 'POST'])
def result():
    # Retrieve dialogue from the URL parameters
    dialogue = request.form.get('hiddenDialogue', '')

    # Get the first matching movie
    matching_movie = get_matching_movie(dialogue)

    print("Received Dialogue from URL:", dialogue)

    if matching_movie:
        # Display movie details (name, genre, rating)
        movie_name = matching_movie['Movie_Name']
        genre = matching_movie['Genre']
        rating = matching_movie['Rating']
        print("Movie Name:", movie_name)
        print("Genre:", genre)
        print("Rating:", rating)

        # Get word frequency for the movie
        word_frequency = get_word_frequency(movie_name)

        # Pass movie details and word frequency to the template
    else:
        # If no matching movie found, display a message
        print("No matching movie found for the given dialogue.")
        movie_name = None
        word_frequency = []

    return render_template('result.html', dialogue=dialogue, movie_name=movie_name, rating=rating, word_frequency=word_frequency)

@app.route('/prac3', methods=['GET', 'POST'])
def prac3():
    # Retrieve dialogue from the URL parameters
    dialogue = request.form.get('hiddenDialogue', '')

    # Get the first matching movie
    matching_movie = get_matching_movie(dialogue)

    print("Received Dialogue from URL:", dialogue)

    if matching_movie:
        # Display movie details (name, genre, rating)
        movie_name = matching_movie['Movie_Name']
        genre = matching_movie['Genre']
        rating = matching_movie['Rating']
        print("Movie Name:", movie_name)
        print("Genre:", genre)
        print("Rating:", rating)

        # Get word frequency for the movie
        word_frequency = get_word_frequency(movie_name)

        # Pass movie details and word frequency to the template
    else:
        # If no matching movie found, display a message
        print("No matching movie found for the given dialogue.")
        movie_name = None
        word_frequency = []

    return render_template('prac3.html', dialogue=dialogue, movie_name=movie_name, rating=rating, word_frequency=word_frequency)



@app.route('/get_wordfreq_csv')
def get_wordfreq_csv():
    wordfreq_path = os.path.join(os.path.dirname(__file__), 'wordfreq.csv')
    return send_file(wordfreq_path, as_attachment=True)

def get_freqchar_data(movie_name):
    freqchar_data = []
    with open('freqchar.csv', 'r') as freqchar_file:
        freqchar_reader = csv.DictReader(freqchar_file)
        for row in freqchar_reader:
            if row['Movie_Name'] == movie_name:
                freqchar_data.append({
                    "Character": row["Character"],
                    "Frequency": int(row["Frequency"]),
                    "Movie_Name": row["Movie_Name"],
                    "Speaker": row["Speaker"],
                    "Reply_To": row["Reply_To"],
                    "Dialogue": row["Dialogue"],
                    "Sentiment": float(row["Sentiment"])
                })

    return freqchar_data[:50]

def get_first_matching_movie_data(dialogue):
    # Find the first movie that matches the dialogue text
    matching_movie = next((movie for movie in movie_data if dialogue.lower() == movie['Text'].lower()), None)

    if matching_movie:
        movie_name = matching_movie['Movie_Name']

        # Get data from 'df.csv' associated with the first movie for the first 50 entries
        with open('df.csv', 'r') as df_file:
            df_reader = csv.DictReader(df_file)
            movie_data_entries = [
                {"Speaker": row["Speaker"], "Reply_To": row["Reply_To"], "Emotion": row["Emotion"]}
                for row in df_reader if row["Movie_Name"] == movie_name
            ][:50]

        # Get data from 'freqchar.csv' associated with the first movie for the first 50 entries
        freqchar_data_entries = get_freqchar_data(movie_name)

        return movie_data_entries, freqchar_data_entries
    else:
        return [], []

@app.route('/get_df_csv', methods=['GET', 'POST'])
def get_df_csv():
    wordfreq_path = os.path.join(os.path.dirname(__file__), 'df.csv')
    return send_file(wordfreq_path, as_attachment=True)
# @app.route('/get_df_csv', methods=['GET', 'POST'])
@app.route('/get_freqchar_csv', methods=['GET', 'POST'])
def get_freqchar_csv():
    wordfreq_path = os.path.join(os.path.dirname(__file__), 'freqchar.csv')
    return send_file(wordfreq_path, as_attachment=True)

@app.route('/prac2', methods=['GET', 'POST'])
def prac2():
    if request.method == 'POST':
        # Get the dialogue from the form submission
        dialogue = request.form.get('dialogue', '')

        if dialogue:
            # Call prac2's API to get data based on the dialogue
            movie_data_entries, freqchar_data_entries = get_first_matching_movie_data(dialogue)
           
            matching_movie = get_matching_movie(dialogue)
            if matching_movie:
                # Display movie details (name, genre, rating)
                movie_name = matching_movie['Movie_Name']
            return render_template('prac2.html', dialogue=dialogue,movie_name=movie_name, movie_data_entries=movie_data_entries, freqchar_data_entries=freqchar_data_entries)

    return render_template('prac2.html')
if __name__ == '__main__':
    app.run(debug=True)
