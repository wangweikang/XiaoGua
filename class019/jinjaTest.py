from flask import Flask
import flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///complicated.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


@app.route('/')
def index_view():
    return flask.render_template('index.html')


@app.route('/blogs')
def blog_view():
    return flask.render_template('blog.html')


if __name__ == '__main__':
    app.run(debug=True)
