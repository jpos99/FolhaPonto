from app import app

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
#app.run(host='127.0.0.1', port=17000)