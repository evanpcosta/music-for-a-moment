import os
from . import db_config

db = db_config.firebase.database()

# gets songs in specific corpus
def fetch_db(corpus_name='corpus_1'):
    return db.child('/' + corpus_name + '/').get().val()


def fetch_specific(path):  # for specific song
    return db.child(path).get().val()


def delete(filepath, songname, corpus_name='corpus_1'):
    os.remove('./downloadedsongs/' + filepath)
    return db.child(corpus_name + '/' + songname + '/').set({})


def write(songs, corpus_name='corpus_1'):
    for i, song in enumerate(songs):
        obj = {
            song[0]: {
                "artist": song[1],
                "title": song[0],
                "lyrics": song[2],
                "watson": song[3],
                "file_name": song[4]
            }
        }
        db.child(corpus_name + '/').update(obj)
