#!/usr/bin/env python
from flask import Flask
from os import listdir
from os.path import isdir, join

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/<measurement_series>/<cart_id>/<img_type>')
def hello(measurement_series, cart_id, img_type):
    ms_directory = "/Users/george/Documents/Exemplar_Datasets/TPA_LemnaTec/0059"
    snapshots = load(ms_directory)

    to_return = '<link rel="stylesheet" type="text/css" \
    href="/static/album.css"/>'
    to_return += '<div class="gallery">'

    for ss in snapshots:
        if ss.measurement_series == measurement_series and ss.cart_id == cart_id and (img_type in ss.images):
            to_return += '<a tabindex="1"><img src="http://localhost:8080/img/' + ss.images[img_type] + '"></a>\n'

    to_return += '<span class="closed">+</span>\n'
    to_return += '<span class="closed-layer"></span>'
    to_return += '</div>'
    return to_return


class Snapshot:
    def __init__(self, measurement_series, cart_id, date):
        self.measurement_series = measurement_series
        self.cart_id = cart_id
        self.date = date
        self.images = dict()

    def add_image(self, img_type, img_path):
        self.images[img_type] = img_path


def load(ms_directory):
    snapshot_directories = [f for f in listdir(ms_directory) if isdir(join(ms_directory, f))]
    snapshots = []

    for snapshot_dir in snapshot_directories:

        tokens = snapshot_dir.split('_')
        snapshot = Snapshot(tokens[0] + ' ' + tokens[1], tokens[2], tokens[3] + "-" + tokens[4])
        image_directories = [f for f in listdir(join(ms_directory, snapshot_dir)) if
                             isdir(join(join(ms_directory, snapshot_dir), f))]
        for image_dir in image_directories:
            snapshot.add_image(image_dir, snapshot_dir + '/' + image_dir + '/' + '0_0.png')

        snapshots.append(snapshot)

    return snapshots


if __name__ == '__main__':
    app.run(debug=True)
