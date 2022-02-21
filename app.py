from apis import api
from flask import Flask

app = Flask(__name__)
api.init_app(app)

app.run(debug=True)
