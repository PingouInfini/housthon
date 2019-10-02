import logging

import requests


def create_bio_minibio(prenom, nomfamille, image, typeimage, url_collissithon):
    # creation des json pour create bio
    if image is not None:
        bio = {
            "biographicsFirstName": prenom,
            "biographicsName": nomfamille,
            "biographicsImageContentType": typeimage,
            "biographicsImage": image
        }
        createbio_url = url_collissithon + "/create_bio"
    else:
        bio = {
            "biographicsFirstName": prenom,
            "biographicsName": nomfamille
        }
        createbio_url = url_collissithon + "/create_minibio"
    target_id = create_bio_colissithon(bio, createbio_url)
    return target_id


# pour creer bioGraphics dans insight via collissithon
def create_bio_colissithon(bio_json, url):
    # appel au service rest de collissithon pour creer biographics
    session = requests.Session()
    current_header = {'Accept': 'application/json',
                      'Content-type': 'application/json'}
    post_response = session.post(url=url, json=bio_json, headers=current_header)
    if post_response.status_code == 200:
        # recuperation de l'id de l'objet créé
        target_id = str(post_response.content, "utf-8")
        logging.info("SUCCESSFUL REQUEST :  " + str(post_response))
        logging.info("RETURNED TARGET ID OF BIOGRAPHICS IS :" + str(target_id))

        return target_id


# pour creer relation entre deux id  dans insight via collissithon
def bind_bio_colissithon(id_bio_candidat, id_bio_tobind, colissithon_url_port):
    session = requests.Session()
    # json avec les deux id a lier
    twoBioIdsJson = {
        "candidateBioId": id_bio_candidat,
        "relationBioId": id_bio_tobind
    }
    url = colissithon_url_port + "/bind_bio"
    current_header = {'Accept': 'application/json',
                      'Content-type': 'application/json'}
    post_response = session.post(url=url, json=twoBioIdsJson, headers=current_header)
    if post_response.status_code == 200:
        logging.info("SUCCESSFUL REQUEST :  " + str(post_response))
