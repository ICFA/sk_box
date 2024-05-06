import logging.config

from flask import Flask, request

from logger_config import dict_config

app = Flask(__name__)

logging.config.dictConfig(dict_config)
server_logger = logging.getLogger("server")


@app.route('/log', methods=['POST'])
def log_post():
    msg = (request.form['levelname'] + " | " +
           request.form['name'] + " | " +
           request.form['asctime'] + " | " +
           request.form['lineno'] + " | " +
           request.form['message'])

    print(msg)
    return 'OK', 200


@app.route('/log', methods=['GET'])
def log_get():
    with open(f'calc.log', 'r') as file:
        result = file.read()
        result = result.replace('/n', '<br>')
    return result


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(port=5555, debug=True)
