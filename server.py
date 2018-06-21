from __future__ import unicode_literals
import json
from gender import compute_bias, compute_similar, upload_text, load_files, delete_file
from flask import Flask, make_response, render_template, request, abort, redirect, url_for
from kmeans import load_model

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """
    Action to render home page.
    """
    return render_template('index.html')


@app.route('/info', methods=['GET'])
def info():
    """
    Action to render home page.
    """
    return render_template('info.html')


@app.route('/database', methods=['GET'])
def database():
    """
    Action to render the database page.
    """
    files = load_files()
    clusterized = load_model()

    data = {file: { 'content': content, 'cluster': clusterized.get(file) } for file, content in files.items()}
    # { 'pippo.txt': { 'content': 'pippo', 'cluster': 4 } }

    return render_template('database.html', data = data )

@app.route('/database/<string:name>', methods=['GET'])
def content(name):
    """
    Action to render the database page.
    """
    files = load_files()
    clusterized = load_model()

    try:
        lines = files[name].split("\n")
        cluster = clusterized.get(name)
        return render_template('content.html', lines = lines, name = name, cluster = cluster )
    except KeyError:
        abort(404)

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    This action accepts user-provided text and returns a JSON payload of
    computed bias.
    """
    text = request.form['text']
    bias = compute_bias(text)

    app.logger.debug('Input: %s', text)
    app.logger.debug('Computed bias: %s', bias)

    res = make_response(json.dumps(bias), 200)
    res.headers['Content-Type'] = 'application/json'

    return res

@app.route('/similar', methods=['POST'])
def similar():
    """
    Action to find similar word to the one pressed
    """
    word = request.form['word']
    heOrShe = request.form['heOrShe']
    similarWords = compute_similar(word, heOrShe)

    app.logger.debug('Finding similar word for %s (%s)', word, heOrShe)
    app.logger.debug('Found words: %s', ', '.join([word for word, _ in similarWords]))

    res = make_response(json.dumps(similarWords), 200)
    res.headers['Content-Type'] = 'application/json'

    return res


@app.route('/upload', methods=['POST'])
def upload():
    """
    Action to append and save user-provided text to a json file
    """
    text = request.form['text']
    uploadjson = upload_text(text)

    app.logger.debug('uploading %s ', text)

    res = make_response(json.dumps(text), 200)
    res.headers['Content-Type'] = 'application/json'

    return res

@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['name']
    delete_file(name)

    return redirect(url_for('database'))
