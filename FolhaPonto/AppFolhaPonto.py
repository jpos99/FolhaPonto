from flask import Flask, render_template

app = Flask(__name__)

@app.route('/inicio')
def inicio():
    return render_template('FrontPage.html')

app.run(host='127.0.0.1', port=15000)