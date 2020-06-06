from flask import session
from flask_socketio import SocketIO
import time
from website import create_app
from website.database import DataBase
import config


app = create_app()
socketio = SocketIO(app) #for user Communication

#FUNCTIONS

@socketio.on('event')
def handle_event(json, methods = ['GET', 'POST']):
    data = dict(json)
    if "name" in data:
        db = DataBase()
        db.save_messages(data["name"], data["messages"])

    socketio.emit("message response", json)

#MAIN FUNCTION
if __name__ == "__main__":
    socketio.run(app, debug=True, host=str(config.Config.SERVER))