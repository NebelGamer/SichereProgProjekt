from flask import Flask, render_template, request
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd
import json

app = Flask(__name__)

# Intentionally hardcoded API key for demonstration (a vulnerability)
API_KEY = '2761f756-fd93-4129-9bdb-321fdf7d11b8'

@app.route('/')
def index():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,  # Using the hardcoded API key (a vulnerability)
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        normalized_data = pd.json_normalize(data['data'])

        html_table = normalized_data.to_html()

        # Vulnerability: Renders HTML without proper sanitization, making it susceptible to XSS attacks(HTML injection)
        return render_template('index.html', table=html_table)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return f"Error: {e}"

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('query')

        # Accepts user input without validation, exposing it to injection attacks
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?symbol={search_query}'
        parameters = {
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)

            # Handle the retrieved data accordingly (omitted for brevity)

            # Vulnerability: Rendering data directly without proper validation
            return render_template('search_result.html', result=data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return f"Error: {e}"

#@app.errorhandler(500)
#def server_error(e):
#   return render_template('error.html'), 500

# Vulnerability: Lacks proper error handling, potentially exposing sensitive information in error messages.
if __name__ == '__main__':
    app.run(debug=True)
