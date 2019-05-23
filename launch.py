import requests
import os
import socket
import src.generators as generators
import src.services as services
from json import dumps
from flask import Flask
from flask import request
from kafka import KafkaProducer


#pour creer service REST
app = Flask(__name__)

#pour recupere variable d'env du yml
housthon_port=os.environ['HOUSTHON_PORT']
colissithon_url_port="http://"+str(os.environ['COLISSITHON_IP'])+":"+str(os.environ['COLISSITHON_PORT'])
kafka_endpoint = str(os.environ["KAFKA_IP"]) + ":" + str(os.environ["KAFKA_PORT"])
#pour tester sur poste de dev
#housthon_port=8090
#colissithon_url_port="http://192.168.0.13:9876"
#kafka_endpoint =  "192.168.0.13:8092"

#url des services REST de collissithon
createbio_url=colissithon_url_port+"/create_bio"
createminibio_url=colissithon_url_port+"/create_minibio"
bindbio_url=colissithon_url_port+"/bind_bio"

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
    nom_famille_pere= habilitation_json['94A']['Pere']['nom']
    prenom_pere=habilitation_json['94A']['Pere']['prenom'][0]
    nom_famille_mere= habilitation_json['94A']['Mere']['nom']
    prenom_mere=habilitation_json['94A']['Mere']['prenom'][0]
    nom_famille_conjoint=habilitation_json['94A']['Conjoint']['nom de famille']
    prenom_conjoint=habilitation_json['94A']['Conjoint']['prenom'][0]
    nom_famille_pere_conjoint=habilitation_json['94A']['Conjoint']['Pere']['nom']
    prenom_pere_conjoint=habilitation_json['94A']['Conjoint']['Pere']['prenom'][0]
    nom_famille_mere_conjoint=habilitation_json['94A']['Conjoint']['Mere']['nom']
    prenom_mere_conjoint=habilitation_json['94A']['Conjoint']['Mere']['prenom'][0]

    #creation des json pour create bio
    bio = {
        "biographicsFirstName": prenom,
        "biographicsName": nomfamille,
        "biographicsImageContentType": typeimage,
        "biographicsImage": image
    }

    bio_pere = {
        "biographicsFirstName": prenom_pere,
        "biographicsName": nom_famille_pere
    }

    bio_mere = {
        "biographicsFirstName": prenom_mere,
        "biographicsName": nom_famille_mere
    }

    bio_conjoint = {
        "biographicsFirstName": prenom_conjoint,
        "biographicsName": nom_famille_conjoint,
    }

    bio_pere_conjoint = {
        "biographicsFirstName": prenom_pere_conjoint,
        "biographicsName": nom_famille_pere_conjoint,
    }

    bio_mere_conjoint = {
        "biographicsFirstName": prenom_mere_conjoint,
        "biographicsName": nom_famille_mere_conjoint,
    }

    idbio=services.create_bio_colissithon(bio, createbio_url)
    idbio_pere=services.create_bio_colissithon(bio_pere,createminibio_url)
    #relation entre les deux id
    services.bind_bio_colissithon(idbio,idbio_pere, bindbio_url)

    idbio_mere=services.create_bio_colissithon(bio_mere,createminibio_url)
    services.bind_bio_colissithon(idbio,idbio_mere, bindbio_url)

    idbio_conjoint=services.create_bio_colissithon(bio_conjoint,createminibio_url)
    services.bind_bio_colissithon(idbio,idbio_conjoint, bindbio_url)

    idbio_pere_conjoint=services.create_bio_colissithon(bio_pere_conjoint,createminibio_url)
    services.bind_bio_colissithon(idbio,idbio_pere_conjoint, bindbio_url)

    idbio_mere_conjoint=services.create_bio_colissithon(bio_mere_conjoint,createminibio_url)
    services.bind_bio_colissithon(idbio,idbio_mere_conjoint, bindbio_url)

    #generators.raw_data_generator(tweet_directory, idbio, producer)
    #generators.pictures_generator(pictures_directory, idbio, producer)
    return idbio


if __name__ == '__main__':
    app.run(host=ip, port=housthon_port)