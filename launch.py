import requests
import os
import socket
import src.services as services
import src.producers as producers
from json import dumps
from flask import Flask
from flask import request
from kafka import KafkaProducer
import base64
from ftplib import FTP
import logging

# pour creer service REST
app = Flask(__name__)

# pour recupere variable d'env du yml
# housthon_port = os.environ['HOUSTHON_PORT']
# colissithon_url_port = "http://" + str(os.environ['COLISSITHON_IP']) + ":" + str(os.environ['COLISSITHON_PORT'])
# kafka_endpoint = str(os.environ['KAFKA_IP']) + ":" + str(os.environ['KAFKA_PORT'])
# tweethon_in = str(os.environ['TOPIC_TWITTHON'])
# googlethon_in = os.environ['TOPIC_GOOGLETHON']
# travelthon_in = os.environ['TOPIC_TRAVELTHON']
# tweet_directory = os.environ['PATH_TWEET']
# pictures_directory = os.environ['PATH_PICTURES']
# topic_housTOcompara = os.environ['TOPIC_COMPARATHON']

# pour tester sur poste de dev
housthon_port=8090
colissithon_url_port="http://192.168.0.4:9876"
kafka_endpoint =  "192.168.0.4:8092"
topic_housTOcompara="housToCompara"
tweethon_in="housToTwit"
googlethon_in="housToGoogle"
travelthon_in="housToTravel"
topic_housTOcompara ="housToCompara"
tweet_directory = "samples/tweets"
pictures_directory = "samples/pictures"

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

producer = KafkaProducer(bootstrap_servers=[kafka_endpoint], value_serializer=lambda x: dumps(x).encode('utf-8'))

print("housthon_port " + str(housthon_port))
print("colissithon_url_port " + colissithon_url_port)
print("ip container " + str(ip))
print("Tweet Path: " + str(tweet_directory))
print("Tweet Pictures: " + str(pictures_directory))




@app.route('/start_process94A', methods=['POST'])
def process_94A():
    habilitation_json = request.get_json()

    # recuperation des champs du json
    nomfamille = habilitation_json['94A']['nom de famille']
    try:
        comptetwitter=habilitation_json['94A']['compte twitter']
    except Exception as e:
        comptetwitter=None

    prenom = habilitation_json['94A']['prenom'][0]
    image = habilitation_json['94A']['photo']
    typeimage = "image/jpeg"
    extension = "jpeg"
    nom_famille_pere = habilitation_json['94A']['Pere']['nom']
    prenom_pere = habilitation_json['94A']['Pere']['prenom'][0]
    nom_famille_mere = habilitation_json['94A']['Mere']['nom']
    prenom_mere = habilitation_json['94A']['Mere']['prenom'][0]
    nom_famille_conjoint = habilitation_json['94A']['Conjoint']['nom de famille']
    prenom_conjoint = habilitation_json['94A']['Conjoint']['prenom'][0]
    nom_famille_pere_conjoint = habilitation_json['94A']['Conjoint']['Pere']['nom']
    prenom_pere_conjoint = habilitation_json['94A']['Conjoint']['Pere']['prenom'][0]
    nom_famille_mere_conjoint = habilitation_json['94A']['Conjoint']['Mere']['nom']
    prenom_mere_conjoint = habilitation_json['94A']['Conjoint']['Mere']['prenom'][0]

    # recuperation des voyages
    voyage_json = habilitation_json['94A']['Voyages depuis 5 ans']
    voyage_conjoint_json = habilitation_json['94A']['Conjoint']['Voyages depuis 5 ans']

    # creation du candidat
    idbio = services.create_bio_minibio(prenom, nomfamille, image, typeimage, colissithon_url_port)
    # idbio="1234567890"
    # creation du pere
    idbio_pere = services.create_bio_minibio(prenom_pere, nom_famille_pere, None, None, colissithon_url_port)
    # relation entre les deux id
    services.bind_bio_colissithon(idbio, idbio_pere, colissithon_url_port)
    # creation de la mere
    idbio_mere = services.create_bio_minibio(prenom_mere, nom_famille_mere, None, None, colissithon_url_port)
    services.bind_bio_colissithon(idbio, idbio_mere, colissithon_url_port)
    # creation du conjoint
    idbio_conjoint = services.create_bio_minibio(prenom_conjoint, nom_famille_conjoint, None, None,
                                                 colissithon_url_port)
    # idbio_conjoint="0987654321"
    services.bind_bio_colissithon(idbio, idbio_conjoint, colissithon_url_port)
    # creation du pere du conjoint
    idbio_pere_conjoint = services.create_bio_minibio(prenom_pere_conjoint, nom_famille_pere_conjoint, None, None,
                                                      colissithon_url_port)
    services.bind_bio_colissithon(idbio, idbio_pere_conjoint, colissithon_url_port)
    # creation de la mere du conjoint
    idbio_mere_conjoint = services.create_bio_minibio(prenom_mere_conjoint, nom_famille_mere_conjoint, None, None,
                                                      colissithon_url_port)
    services.bind_bio_colissithon(idbio, idbio_mere_conjoint, colissithon_url_port)

    # parcours des destinations pour les envoyer dans file kafka travelthon
    voyages_in_travelthon(voyage_json, idbio, travelthon_in, producer)
    voyages_in_travelthon(voyage_conjoint_json, idbio_conjoint, travelthon_in, producer)

    # envoi de la bio dans googlethon
    producers.fill_mini_bio_extension_kafka(nomfamille, prenom, idbio, extension, googlethon_in, producer)

    # envoi de la bio dans twitthon
    if comptetwitter is not None:
        producers.fill_mini_bio_kafka("",comptetwitter, idbio, tweethon_in, producer)
    else:
        producers.fill_mini_bio_kafka(nomfamille, prenom, idbio, tweethon_in, producer)

    producers.fill_mini_bio_kafka(nom_famille_pere, prenom_pere, idbio_pere, tweethon_in, producer)
    producers.fill_mini_bio_kafka(nom_famille_mere, prenom_mere, idbio_mere, tweethon_in, producer)
    producers.fill_mini_bio_kafka(nom_famille_conjoint, prenom_conjoint, idbio_conjoint, tweethon_in, producer)
    producers.fill_mini_bio_kafka(nom_famille_pere_conjoint, prenom_pere_conjoint, idbio_pere_conjoint, tweethon_in, producer)
    producers.fill_mini_bio_kafka(nom_famille_mere_conjoint, prenom_mere_conjoint, idbio_mere_conjoint, tweethon_in, producer)

    # envoi dans housTOcompara pour récupération des images
    producers.fill_housTOcompara(nomfamille, prenom, image, extension, idbio, producer, topic_housTOcompara)

    ### FTP

    ftp = FTP("192.168.0.4")
    ftp.login("test", "test")
    type = ".*\.jpg$"
    crawled_dir = ftp.pwd()
    crdir("processedData", ftp)
    coucou = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isdir(coucou+"/img_94A"):
        os.mkdir(coucou+"/img_94A")
    os.chdir(coucou+"/img_94A")

    base64toFTP(ftp, image, idbio, extension)

    return idbio


def voyages_in_travelthon(voyage_json, idbio, travelthon_in, producer):
    # parcour des destinations pour les envoyer dans file kafka travelthon
    for i in range(len(voyage_json)):
        destination = voyage_json[i]['pays']
        producers.fill_travelthon_kafka(destination, idbio, travelthon_in, producer)

def base64toFTP(ftp, img_data, idBio, extension):
    img_name = idBio+"."+extension
    with open(img_name, "wb") as fh:
        fh.write(base64.b64decode(img_data))
        logging.info("Sauvegarde de l'image de référence du candidat dans le filesystem ")
    file = open(img_name,'rb')
    ftp.storbinary('STOR '+img_name, file)
    file.close()



"""
Tests if the source directory doesn't contain a json or an image (except processedData directory)
"""
def isSourceDirectoryEmpty(ftp):
    filelist = []
    ftp.retrlines('LIST', filelist.append)
    return len(filelist) == 1

"""
Tests if the given directory exists 
"""
def directory_exists(directory, ftp):
    filelist = []
    ftp.retrlines('LIST', filelist.append)
    for f in filelist:
        if f.split()[-1] == directory and f.upper().startswith('D'):
            return True
    return False

"""
Create a given directory
"""
def crdir(dir, ftp):
    if len(dir.rsplit("/", 1)) == 2:
        ftp.cwd(dir.rsplit("/", 1)[0])
        dir = dir.rsplit("/", 1)[1]
    if directory_exists(dir, ftp) is False:  # (or negate, whatever you prefer for readability)
        ftp.mkd(dir)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=housthon_port)
