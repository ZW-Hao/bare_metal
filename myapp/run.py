from app import app
from flask_cors import CORS

CORS(app, resources={r"/api/*": {"origins": "*"}})

app.run(host="0.0.0.0", port=8080, debug=True)
