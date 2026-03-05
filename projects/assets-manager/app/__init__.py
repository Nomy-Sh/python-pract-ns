from flask import Flask, url_for, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def index_page():
    return f'<b>Hello, World!</b>, {url_for('dashboard', username='noman')}'

@app.route('/dashboard/<username>')
def dashboard(username):
    return f'This is a dashboard for {escape(username)}'


@app.get('/product/list/<int:id>')
def product_list(id):
    return render_template('index.html')


# with app.test_request_context():
#     print(url_for('index_page'))
#     print(url_for('dashboard', username='noman'))
#     print(url_for('product_list', id=100))
#url_for('static', filename='css/style.css')

if __name__ == '__main__':
    app.run()
