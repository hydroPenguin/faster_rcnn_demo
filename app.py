from flask import Flask, render_template, request
from werkzeug import secure_filename
import logging
import os

app = Flask(__name__, static_url_path='', static_folder='')
app.config.from_object('config.Config')
resource_path = os.path.join(app.root_path, 'tmp')

@app.route('/')
def hello():
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    import inference
    file = request.files['file']

    filename = secure_filename(file.filename)
    file.save(os.path.join(resource_path, filename))

    path = resource_path+'/'+filename
    # app.logger.info(path)
    inference.process(path, app.config['PATH_TO_FROZEN_GRAPH'], app.config['PATH_TO_LABELS'], filename)

    # app.logger.info(resource_path)

    return render_template('result.html', filename=filename)

if __name__ == '__main__':
    app.run()
