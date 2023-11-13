from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
import re

app = Flask(__name__)
csrf = CSRFProtect(app)  # You can directly pass the app instance here
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/submit', methods=['POST'])
def submit():
    html_file = './index.html'
    try:
        user_input = request.form['Input']
        if check_requirement(user_input):
            if not check_if_is_list(user_input):
                return f'Input accepted: {user_input}'
            else:
                app.logger.error('An error occurred: In List')
        else:
            app.logger.error('An error occurred: No requirement')
        return render_template(html_file, error="Invalid.")
    except Exception as e:
        app.logger.error(f'An error occurred: {e}')
        return render_template(html_file, error="An internal error occurred."), 500

def check_if_is_list(data):
    with open('list.txt', 'r') as file:
        password_set = set(file.read().splitlines())
    return data in password_set

def check_requirement( user_input):
    pattern = r'^[a-zA-Z0-9 ]{8,64}$'
    return re.match(pattern, user_input)

if __name__ == '__main__':
    app.run(debug=True, port=8001, host="0.0.0.0")

