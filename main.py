from flask import *
from flask_socketio import SocketIO

# Create flask app, SocketIO object
app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('gyroperfect.html')

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port = 9000, debug=True)
