from flask import Flask, url_for, render_template, request
from markupsafe import escape
from routes import *

app = Flask(__name__)



# login
# register
# dashboard -> quickcount, search, add-new, links
# physical assets
# digital assets
# debts
# settings
# about -> /about and /












if __name__ == '__main__':
     app.run()
    #       host = '0.0.0.0',
    #       port = 5001
    #   )

# with app.test_request_context():
#     print(url_for('index_page'))
#     print(url_for('dashboard', username='noman'))
#     print(url_for('product_list', id=100))
#url_for('static', filename='css/style.css')
