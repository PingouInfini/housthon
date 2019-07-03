def fill_mini_bio_kafka(nomfamille, prenom, idBio, topic, producer):
    json_minibio = {
        "idBio": idBio,
        "nom": nomfamille,
        "prenom": prenom
    }
    producer.send(topic, value=(json_minibio))

def fill_mini_bio_extension_kafka(nomfamille, prenom, idBio, extension, topic, producer):
    json_minibio = {
        "idBio": idBio,
        "nom": nomfamille,
        "prenom": prenom,
        "extension": extension
    }
    producer.send(topic, value=(json_minibio))

def fill_travelthon_kafka(destination, idBio, topic, producer):
    json_togo = {
        "destination": destination,
        "idBio": idBio
    }
    producer.send(topic, value=(json_togo))


def fill_housTOcompara(nom, prenom, bytified_picture, picture_extension, bio_id, producer, topic):
    producer.send(topic, value=(nom, prenom, bytified_picture, picture_extension, bio_id))
