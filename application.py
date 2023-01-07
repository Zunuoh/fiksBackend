# # import gevent
# from gevent import monkey
# monkey.patch_all()

# from app.tasks.pending_task_processor import process_pending_feepay_transactions
# import os
# import datetime
# from apscheduler.schedulers.background import BackgroundScheduler

# from flask import Flask
# import click
# from flask_mongoengine import MongoEngine
# from flask_socketio import SocketIO
# from flask_cors import CORS
# from flask_mail import Mail
# from flask import session

# # Project dependencies
# from app.libs.logger import Logger

# scheduler = BackgroundScheduler()
# #scheduler.add_job(process_pending_feepay_transactions, 'cron', year='*', month='*', day='*', week='*', day_of_week='*', hour=8, minute=0, second=0)
# #scheduler.add_job(process_pending_feepay_transactions, 'cron', year='*', month='*', day='*', week='*', day_of_week='*', hour=11, minute=30, second=0)
# #scheduler.start()

# app = Flask(__name__, static_url_path="/static")
# # app = Flask(__name__, static_url_path="/static")

# # Set `FLASK_CONFIG` env to 'Production' or 'Development' to set Config
# flask_config = os.environ.get('FLASK_CONFIG', 'Development')
# app.config.from_object('app.config.{}'.format(flask_config))

# # Web Socket instance
# socketio = SocketIO(app)
# CORS(app)
# # db = MongoEngine(app)
# db = MongoEngine(app)

# mail = Mail()
# mail.init_app(app)

# from app.client import client_bp
# from app.controllers import api

# @app.before_request
# def make_session_permanent():
#     session.permanent = True
#     app.permanent_session_lifetime = datetime.timedelta(minutes=60)


# # Register API Endpoints Blueprints
# app.register_blueprint(api)

# # Register Client Portal Blueprint
# app.register_blueprint(client_bp)

# from . import config
# Logger.log(__name__, "start_up", "EVENT", "", "SERVER STARTED")
