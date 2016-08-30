atomfun
=======

GET request to http://0.0.0.0:3001/ping


local install
-------------

With conda:

    conda install flask flask-cors

Just pip:

    pip install -r requirements.txt


Run:

With flask 0.11 and later use:

    export FLASK_APP=server.py
    export FLASK_DEBUG=1 (optional)
    flask run

With earlier version just do:

    python server.py

docker
------

Build:

    docker build -t username/jwttut:latest .

Run:

    docker run -p 3001:3001 --env-file .env username/jwttut

