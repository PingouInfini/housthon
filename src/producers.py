def fill_tweets_kafka(json_tweet, bio_id, producer):

    producer.send("tweetopic", value=(json_tweet, bio_id))


def fill_pictures_kafka(picture, bio_id, producer):

    producer.send("topictures", value=(picture, bio_id))
