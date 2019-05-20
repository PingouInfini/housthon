import sys
import threading
from flask import Flask
from flask import request

custom_port = 8090
app = Flask(__name__)

@app.route('/start_process94A', methods=['POST'])
def process_94A():
    habilitation_json = request.get_json()
    nomfamille = habilitation_json['94A']['nom de famille']
    prenom = habilitation_json['94A']['prenom'][1]
    return prenom

def start_REST_server(port):
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=custom_port)