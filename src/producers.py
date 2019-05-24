def fill_googlethon_kafka(prenom, nomfamille, idBio, topic, producer):
    json_minibio = {
        "prenom": prenom,
        "nom": nomfamille,
        "idBio" : idBio
    }
    producer.send(topic, value=(json_minibio))

def fill_travelthon_kafka(destination, idBio, topic, producer):
    json_togo = {
        "destination": destination,
        "idBio" : idBio
    }
    producer.send(topic, value=(json_togo))

def fill_kafka(json, bio_id, producer, topic):

    producer.send(topic, value=(json, bio_id))
