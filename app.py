from flask import Flask, render_template, request
import requests
import os
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    error = None

    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            headers = {
                "User-Agent": "DarkWebCheckerApp"
            }
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            try:
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    results = res.json()
                elif res.status_code == 404:
                    results = []  # No breach
                else:
                    error = f"Napaka pri iskanju: {res.status_code}"
            except Exception as e:
                error = f"Napaka: {str(e)}"

    return render_template('index.html', results=results, error=error)

if __name__ == '__main__':
    app.run(debug=True)
