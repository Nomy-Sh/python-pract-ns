from flask import Flask, url_for, render_template, request


# This is going to be about page
@app.route('/')
@app.route('/about/')
def index():
    return '<b>Hello, World!</b>'


@app.post('/login')
@app.get('/login')
def login():
    if request.method == 'POST':
        print('You are IN')
        return 'You are IN'
    elif request.method == 'GET':
        print('Fill the form to log-in')
        return render_template('login.html')
    

@app.get('/register')
def register():
    return render_template('register.html')

@app.get('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.get('/physical')
def physical():
    return  render_template('physical_assets_list.html')


@app.get('/digital')
def digital():
    return  render_template('digital_assets_list.html')


@app.get('/debts')
def debts():
    return  render_template('debts_list.html')


@app.get('/settings')
def settings():
    return  render_template('settings.html')




