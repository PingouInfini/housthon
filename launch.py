import requests
import os
import socket
import src.generators as generators
from json import dumps
from flask import Flask
from flask import request
from kafka import KafkaProducer


#pour creer service REST
app = Flask(__name__)

#pour recupere variable d'env du yml
housthon_port=os.environ['HOUSTHON_PORT']
createbio_url="http://"+str(os.environ['COLISSITHON_IP'])+":"+str(os.environ['COLISSITHON_PORT'])+"/create_bio"
kafka_endpoint = str(os.environ["KAFKA_IP"]) + ":" + str(os.environ["KAFKA_PORT"])
#housthon_port=8090
#createbio_url="http://192.168.0.13:9876/create_bio"
#kafka_endpoint =  "192.168.0.13:8092"

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

producer = KafkaProducer(bootstrap_servers=[kafka_endpoint], value_serializer=lambda x: dumps(x).encode('utf-8'))
tweet_directory = "samples/tweets"
pictures_directory = "samples/pictures"

print("housthon_port "+str(housthon_port))
print("createbio_url "+createbio_url)
print("ip container "+str(ip))

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
    generators.raw_data_generator(tweet_directory, idbio, producer)
    generators.pictures_generator(pictures_directory, idbio, producer)
    return idbio

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
    app.run(host=ip, port=housthon_port)