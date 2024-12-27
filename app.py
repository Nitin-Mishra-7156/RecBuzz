from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load preprocessed data
try:
    df_result = pd.read_csv('static/data/MovieRecommendations.csv') 
except FileNotFoundError:
    print("Error: MovieRecommendations.csv not found.")
    df_result = pd.DataFrame()  # Create an empty DataFrame for error handling

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        movie_name = request.form.get('movie_name')
        if not movie_name:
            return jsonify({'error': 'Please provide a movie name'}), 400

        # Check if movie exists
        movie_row = df_result[df_result['title'] == movie_name]
        if movie_row.empty:
            return jsonify({'error': 'Movie not found in our database'}), 404

        # Fetch recommendations
        recommendations = {
            'first': movie_row['FirstMovieRecommendation'].values[0],
            'second': movie_row['SecondMovieRecommendation'].values[0],
            'third': movie_row['ThirdMovieRecommendation'].values[0],
            'fourth': movie_row['FourthMovieRecommendation'].values[0],
        }

        return jsonify(recommendations)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500 

if __name__ == '__main__': 
    app.run(debug=True)