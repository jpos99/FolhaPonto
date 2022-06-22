from app import app
import os

port = int(os.environ.get("PORT", 15000))
app.run(port=port)
#app.run(host='127.0.0.1', port=17000)