from flask import Flask, render_template
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd
import json

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '2761f756-fd93-4129-9bdb-321fdf7d11b8',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        # Normalize the 'data' part of the JSON response
        normalized_data = pd.json_normalize(data['data'])

        # Convert DataFrame to HTML table
        html_table = normalized_data.to_html()

        return render_template('index.html', table=html_table)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
