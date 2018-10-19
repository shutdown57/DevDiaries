from flask import render_template

from .server import app


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


#  if __name__ == '__main__':
    #  app.run(debug=False)
