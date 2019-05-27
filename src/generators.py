import base64
import json
import os
import time
import src.producers as producers

resolved_locations = {}

def raw_data_generator(path_to_tweets_dir, bio_id, producer, topic):
    index = 0
    for file in os.listdir(path_to_tweets_dir):
        index += 1
        fname, fext = os.path.splitext(file)
        print(fname)
        try:
            with open(os.path.join(path_to_tweets_dir, file), encoding='utf-8') as json_file:
                json_tweet = json.load(json_file)
            if index < 10:
                producers.fill_kafka(json_tweet, bio_id, producer, topic)
            else:
                break
        except:
            raise ValueError("Problem before sending tweet to Kafka")


def pictures_generator(path_to_pictures, bio_id, producer, topic):
    # TODO génère des pictures pour remplir la file Kafka, et return data + topic
    index = 0
    for file in os.listdir(path_to_pictures):
        index += 1
        try:
            if index < 10:
             fname, fext = os.path.splitext(file)
             print(fname)
             file_type_point = "image/" + str(fext).replace(".", "")

             image = picture_evolution(path_to_pictures + "/" + file)
             picture = {
                'name': fname,
                'extension': file_type_point,
                'image': image
                }
             producers.fill_kafka(picture, bio_id, producer, topic)
             time.sleep(5)
            else:
                break
        except:
            raise ValueError("Problem before sending picture to Kafka")  # bytifie la picture


def picture_evolution(picture_path):
    with open(picture_path, "rb") as image:
        f = image.read()
    b = bytearray(f)
    bytified_picture = base64.b64encode(b).decode('UTF-8')
    return bytified_picture
