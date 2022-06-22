from app import app
import os

port = int(os.environ.get("PORT", 15000))
app.run(host='0.0.0.0', port=port)
#app.run(host='127.0.0.1', port=17000)