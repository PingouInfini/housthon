import requests

#pour creer bioGraphics dans insight via collissithon
def create_bio_colissithon(bio_json, createbio_url):
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

#pour creer relation entre deux id  dans insight via collissithon
def bind_bio_colissithon(id_bio_candidat, id_bio_tobind, url):
    session = requests.Session()
    #json avec les deux id a lier
    twoBioIdsJson= {
        "candidateBioId": id_bio_candidat,
        "relationBioId": id_bio_tobind
    }
    current_header = {'Accept': 'application/json',
                      'Content-type': 'application/json'}
    post_response = session.post(url = url, json = twoBioIdsJson, headers = current_header)
    if post_response.status_code == 200:
        print("SUCCESSFUL REQUEST :  " + str(post_response))