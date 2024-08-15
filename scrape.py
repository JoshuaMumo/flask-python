from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd
import os

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def google_search(query):
    return search(query, num_results=10)

def extract_links_with_extensions(urls, extensions):
    valid_links = []
    for url in urls:
        if any(url.lower().endswith(ext) for ext in extensions):
            valid_links.append(url)
    return valid_links

def fetch_url_content(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_links():
    # Get the text input from the form
    search_text = request.form.get('search_text', '')

    # Automatically locate the CSV file in the same directory as the .py file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, 'base_urls.csv')

    # Check if the file exists
    if not os.path.exists(csv_file):
        return render_template('error.html', message="CSV file not found.")

    # Read the CSV file
    df = pd.read_csv(csv_file)
    results = []

    for base_url in df['Website URL']:
        # Include the search_text in the query
        query = f"{base_url} {search_text}"
        search_results = google_search(query)
        results.append({
            'Website URL': base_url,
            'links': search_results
        })

    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
