import requests
import json
from flask import Flask
from flask import request
from src.variables import createbio_url

custom_port = 8090
app = Flask(__name__)

@app.route('/start_process94A', methods=['POST'])
def process_94A():
    habilitation_json = request.get_json()
    nomfamille = habilitation_json['94A']['nom de famille']
    prenom = habilitation_json['94A']['prenom'][0]
    image = habilitation_json['94A']['photo']
    typeimage="bio-img"

    bio = {
        "biographicsFirstname": prenom,
        "biographicsName": nomfamille,
        "biographicsImageContentType": typeimage,
        "biographicsImage": image
    }
    idbio=create_bio_colissithon(bio)
    return idbio

def start_REST_server(port):
    app.run(host='0.0.0.0', port=port)


def create_bio_colissithon(bio_json):
    session = requests.Session()
    current_header = {'Accept': 'application/json, text/plain, */*',
                      'Accept-Encoding': 'gzip, deflate, br',
                      'Content-type': 'application/json'}
    post_response = session.post(url = createbio_url, json = bio_json, headers = current_header)
    if post_response.status_code == 201:
        data = json.loads(post_response.content)
        target_ID = data["externalId"]
        print("SUCCESSFUL REQUEST :  " + str(post_response))
        print("RETURNED TARGET ID OF BIOGRAPHICS IS :" + str(target_ID))
        return target_ID

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=custom_port)