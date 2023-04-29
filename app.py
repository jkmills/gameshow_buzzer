from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO

app = Flask(__name__)
socketio = SocketIO(app)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
button_pins = [2, 3, 4, 17, 27]
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

@app.route('/')
def main_menu():
    return render_template('main_menu.html')

@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        # Process the submitted game data and set up the game
        return jsonify({"success": True})
    return render_template('new_game.html')

@app.route('/reboot', methods=['POST'])
def reboot():
    os.system('sudo reboot now')
    return '', 204

@app.route('/diagnostics')
def diagnostics():
    return render_template('diagnostics.html')

@app.route('/button_status')
def button_status():
    return jsonify([not GPIO.input(pin) for pin in button_pins])

@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)

@socketio.on('player_buzz')
def handle_player_buzz(player_number):
    # Broadcast the buzzed player to all clients
    emit('player_buzz', player_number, broadcast=True)

@socketio.on('host_reset')
def handle_host_reset():
    # Broadcast the reset signal to all clients
    emit('reset', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
