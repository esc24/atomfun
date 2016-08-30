"""
Flask web app that exposes endpoints with an atom feed for notifications.

"""
import datetime
import mimetypes
import os
import os.path
import urlparse

from feedgen.feed import FeedGenerator
from flask import Flask, request, send_from_directory
from flask_cors import cross_origin
import tzlocal

app = Flask(__name__)
app.config['DATA_DIR'] = 'data'


# Controllers API
@app.route("/")
def hello_world():
    return 'Hello, World!'


@app.route("/ping")
@cross_origin(headers=['Content-Type', 'Authorization'])
def ping():
    return "All good. You don't need to be authenticated to call this."


@app.route('/data/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['DATA_DIR'],
                               filename, as_attachment=False)


# Atom feed
@app.route('/atom.xml')
def atom_feed():
    fg = FeedGenerator()
    fg.id(request.url)
    fg.title('Test Atom feed')
    fg.author({'name': 'Ed', 'email': 'ed@email.com'})
    fg.link(href=request.url, rel='self')
    fg.language('en')
    # Check data store
    data_dir = app.config['DATA_DIR']
    if not os.path.isdir(data_dir):
        raise IOError('Data directory {!r} not found'.format(data_dir))
    filenames = (os.path.join(data_dir, f) for f in os.listdir(data_dir) if
                 os.path.isfile(os.path.join(data_dir, f)))
    for filename in filenames:
        fe = fg.add_entry()
        key = os.path.basename(filename)
        fe.id(key)
        fe.title(key)
        tz = tzlocal.get_localzone()
        ctime = datetime.datetime.fromtimestamp(os.path.getctime(filename))
        fe.published(tz.localize(ctime))
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        fe.updated(tz.localize(mtime))
        filesize = str(os.path.getsize(filename))
        mimetype, _ = mimetypes.guess_type(filename)
        # Construct link to resource (must be a better way to use flask route)
        # note that the training slash is needed due to urljoin behaviour
        data_url = urlparse.urljoin(request.url_root, 'data/')
        link = urlparse.urljoin(data_url, key)
        print data_url, link
        fe.link(href=link)
        fe.enclosure(link, filesize, mimetype)
    return fg.atom_str(pretty=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3001)))
