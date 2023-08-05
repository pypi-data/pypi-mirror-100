# Init application
import asyncio
import glob
import os
import sys
import threading

from flask import Flask, render_template, jsonify

from crypto_bot.bots import create_bot
from crypto_bot.config import load_config, init_logger
from crypto_bot.connector import ApiConnector
from crypto_bot.error import ApiError
from crypto_bot.resources import get_resource

try:
    cfg = sys.argv[1]
except:
    cfg = None

bots = []
config = load_config(cfg)
logger = init_logger(config['log_level'])
logger.info("Config loaded")
connector = ApiConnector(config['api_url'])
logger.info("Start Bots")
loop = asyncio.get_event_loop()
for i, b in enumerate(config['bots']):
    chat_id = str(i + 1) if i + 1 > 9 else "0{}".format(i + 1)
    bot = create_bot(b['coin'], chat_id, config['command_roles'], connector)
    loop.create_task(bot.start(b['token']))
    bots.append(bot)
threading.Thread(target=loop.run_forever).start()

application = Flask(__name__,
                    template_folder=get_resource('templates'),
                    static_folder=get_resource('static'))


@application.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@application.route('/logs', methods=['GET'])
def get_server_logs():
    files = glob.glob(os.path.join('logs', "*.log"))
    return jsonify([f.split(os.sep)[-1] for f in files])


@application.route('/bots', methods=['GET'])
def get_bots():
    return jsonify({b.user.name: b.describe() for b in bots})


@application.route('/logs/<filename>', methods=['GET'])
def get_local_log(filename):
    try:
        short_name = filename.split(os.sep)[-1]
        data = ["Log data for: " + short_name, "---------------------------------"]
        with open(os.path.join('logs', filename), 'r') as log:
            data.extend([l.rstrip('\n') for l in log.readlines()])
        return jsonify(data)
    except Exception as e:
        raise ApiError("Error, no logs for '"
                       + filename + "' could be found!", e, status_code=404)


@application.errorhandler(ApiError)
def handle_error(error):
    response = jsonify(error.serialize())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    application.run(
        host='0.0.0.0',
        port=8033,
        debug=False,
        use_reloader=False
    )
