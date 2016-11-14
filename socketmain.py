from flask import *
from flask_socketio import SocketIO

# Create flask app, SocketIO object
app = Flask(__name__)
socketio = SocketIO(app)
count = 0

@app.route("/")
def index():
    return render_template('gyrosocket.html')

@socketio.on('drive')
def get_drive(driveleft,driveright):
    global count
    count+=1
    print("socket {0}:   {1}    |    {2} ".format(count,driveleft,driveright))

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port = 9000, debug=True)
