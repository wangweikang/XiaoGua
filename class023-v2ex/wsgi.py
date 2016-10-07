import app as bbs

app = bbs.configured_app()

# gunicorn appcorn:app
# nohup gunicorn -b '0.0.0.0:80' appcorn:app &

# wsgi
