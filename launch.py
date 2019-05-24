import requests
import os
import socket
import src.generators as generators
import src.services as services
import src.producers as producers
from json import dumps
from flask import Flask
from flask import request
from kafka import KafkaProducer

#pour creer service REST
app = Flask(__name__)

#pour recupere variable d'env du yml
housthon_port=os.environ['HOUSTHON_PORT']
colissithon_url_port="http://"+str(os.environ['COLISSITHON_IP'])+":"+str(os.environ['COLISSITHON_PORT'])
kafka_endpoint = str(os.environ['KAFKA_IP']) + ":" + str(os.environ['KAFKA_PORT'])
topictures=str(os.environ['TOPIC_PICTURE'])
tweetopic=str(os.environ['TOPIC_TWITTER'])
topicgooglethon=os.environ['TOPIC_GOOGLETHON']

#pour tester sur poste de dev
#housthon_port=8090
#colissithon_url_port="http://192.168.0.13:9876"
#kafka_endpoint =  "192.168.0.13:8092"
#topictures="topictures"
#tweetopic="tweetopic"
#topicgooglethon="topicgoogle"

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

producer = KafkaProducer(bootstrap_servers=[kafka_endpoint], value_serializer=lambda x: dumps(x).encode('utf-8'))
tweet_directory = "samples/tweets"
pictures_directory = "samples/pictures"


print("housthon_port "+str(housthon_port))
print("colissithon_url_port "+colissithon_url_port)
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


    #creation du candidat
    idbio=services.create_bio_minibio(prenom, nomfamille, image, typeimage, colissithon_url_port)
    producers.fill_googlethon_kafka(nomfamille,prenom, idbio,topicgooglethon,producer)
    #creation du pere
    idbio_pere=services.create_bio_minibio(prenom_pere, nom_famille_pere, None, None,  colissithon_url_port)
    #relation entre les deux id
    services.bind_bio_colissithon(idbio,idbio_pere, colissithon_url_port)
    #creation de la mere
    idbio_mere=services.create_bio_minibio(prenom_mere, nom_famille_mere, None, None,  colissithon_url_port)
    services.bind_bio_colissithon(idbio,idbio_mere, colissithon_url_port)
    #creation du conjoint
    idbio_conjoint=services.create_bio_minibio(prenom_conjoint, nom_famille_conjoint, None, None,  colissithon_url_port)
    services.bind_bio_colissithon(idbio,idbio_conjoint, colissithon_url_port)
    #creation du pere du conjoint
    idbio_pere_conjoint=services.create_bio_minibio(prenom_pere_conjoint, nom_famille_pere_conjoint, None, None,  colissithon_url_port)
    services.bind_bio_colissithon(idbio,idbio_pere_conjoint, colissithon_url_port)
    #creation de la mere du conjoint
    idbio_mere_conjoint=services.create_bio_minibio(prenom_mere_conjoint, nom_famille_mere_conjoint, None, None,  colissithon_url_port)
    services.bind_bio_colissithon(idbio,idbio_mere_conjoint, colissithon_url_port)

    generators.raw_data_generator(tweet_directory, idbio, producer, tweetopic)
    generators.pictures_generator(pictures_directory, idbio, producer, topictures)
    return idbio


if __name__ == '__main__':
    app.run(host=ip, port=housthon_port)