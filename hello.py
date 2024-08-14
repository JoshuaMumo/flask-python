from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

# Define a user-agent list to simulate requests from different browsers
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/53.0',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12'
]


def get_page_content(url):
    headers = {'User-Agent': random.choice(USER_AGENTS)}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Error connecting: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:
        return f"Timeout error: {timeout_err}"
    except requests.exceptions.RequestException as req_err:
        return f"An error occurred: {req_err}"

    return None


def parse_html(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        return soup
    except Exception as e:
        return f"An error occurred while parsing HTML: {e}"


def extract_info(soup):
    try:
        tables = soup.find_all('table')
        table_data = ""
        for idx, table in enumerate(tables):
            table_data += f"<h3>Table {idx + 1}:</h3>"
            rows = table.find_all('tr')
            table_data += "<table border='1'>"
            for row in rows:
                table_data += "<tr>"
                cols = row.find_all(['td', 'th'])
                cols = [f"<td>{ele.text.strip()}</td>" for ele in cols]
                table_data += ''.join(cols)
                table_data += "</tr>"
            table_data += "</table><br>"
        return table_data

    except Exception as e:
        return f"An error occurred while extracting information: {e}"


@app.route('/')
def home():
    url = request.args.get('url', 'https://www.unido.org/get-involved-procurement/procurement-opportunities')
    content = get_page_content(url)
    if isinstance(content, str) and content.startswith('Error'):
        return content

    soup = parse_html(content)
    if isinstance(soup, str) and soup.startswith('An error occurred'):
        return soup

    table_data = extract_info(soup)
    return render_template_string("""
    <h1>Web Scraping Result</h1>
    <form method="get">
        <label for="url">Enter URL:</label>
        <input type="text" id="url" name="url" value="{{ url }}">
        <input type="submit" value="Scrape">
    </form>
    <div>{{ table_data|safe }}</div>
    """, url=url, table_data=table_data)


if __name__ == "__main__":
    app.run(debug=True)
