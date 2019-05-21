import requests
from flask import Flask
from flask import request
from src.variables import createbio_url

custom_port = 8090
app = Flask(__name__)

@app.route('/start_process94A', methods=['POST'])
def process_94A():
    habilitation_json = request.get_json()
    #recuperation des champs du json
    nomfamille = habilitation_json['94A']['nom de famille']
    prenom = habilitation_json['94A']['prenom'][0]
    image =habilitation_json['94A']['photo']
    typeimage="image/jpeg"

    #creation du json pour colissithon
    bio = {
        "biographicsFirstName": prenom,
        "biographicsName": nomfamille,
        "biographicsImageContentType": typeimage,
        "biographicsImage": image
    }
    idbio=create_bio_colissithon(bio)
    return idbio

def start_REST_server(port):
    app.run(host='0.0.0.0', port=port)

def create_bio_colissithon(bio_json):
    #appel au service rest de collissithon pour creer biographics
    session = requests.Session()
    current_header = {'Accept': 'application/json',
                      'Content-type': 'application/json'}
    post_response = session.post(url = createbio_url, json = bio_json, headers = current_header)
    if post_response.status_code == 200:
        #recupereation de l'id de l'objet crée
        target_id = str(post_response.content, "utf-8")
        print("SUCCESSFUL REQUEST :  " + str(post_response))
        print("RETURNED TARGET ID OF BIOGRAPHICS IS :" + str(target_id))
        return target_id

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=custom_port)