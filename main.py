from flask import Flask, render_template, request, redirect, url_for, session,jsonify

import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'



# Define the folder containing CSV chunks
CSV_CHUNKS_FOLDER = 'output_chunks/'

# Function to load quotes from a specific CSV chunk
def load_quotes(chunk_number):
    csv_path = os.path.join(CSV_CHUNKS_FOLDER, f'output_chunk_{chunk_number}.csv')
    quotes_df = pd.read_csv(csv_path)
    return quotes_df

# API endpoint to get all quotes or filter by category/author
@app.route('/quotes', methods=['GET'])
def get_quotes():
    try:
        # Extract chunk number from the request parameters
        chunk_number = int(request.args.get('chunk_number'))
        if chunk_number <= 0:
            raise ValueError("Invalid chunk number")

        # Load quotes from the specified CSV chunk
        quotes_df = load_quotes(chunk_number)

        # Filter quotes by category or author if provided
        category = request.args.get('category')
        author = request.args.get('author')

        if category:
            quotes_df = quotes_df[quotes_df['category'].str.lower() == category.lower()]

        if author:
            quotes_df = quotes_df[quotes_df['author'].str.lower() == author.lower()]

        # Convert the filtered quotes to a dictionary and return as JSON
        return jsonify(quotes_df.to_dict(orient='records'))

    except ValueError as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
