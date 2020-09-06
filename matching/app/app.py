"""Core Appliction.
This module houses the core Flask application.
"""

import os
import json
import logging
import watchtower
from boto3.session import Session
from flask import Flask, g, request
from datetime import datetime
from flask_restful import Api

from matching.api import ComputeMatch
from matching.config import ConfigurationFactory
from matching.database import Session

app = Flask(__name__)
config = ConfigurationFactory.from_env()
app.config.from_object(config)

api = Api(app)
api.add_resource(ComputeMatch, '/compute-match')

# logger configuration
formatter = logging.Formatter(
    fmt='[%(asctime)s] [%(levelname)s] %(message)s', datefmt="%a, %d %b %Y %H:%M:%S")

try:
    logging.getLogger().setLevel(logging.INFO)
    boto3_session = Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION_NAME')
    )
    logger = logging.getLogger(config.AWS_LOGGER_NAME)
    handler = watchtower.CloudWatchLogHandler(
        boto3_session=boto3_session, log_group=os.getenv('AWS_LOG_GROUP'), stream_name=os.getenv('AWS_LOG_STREAM'))
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] %(message)s', datefmt="%a, %d %b %Y %H:%M:%S")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
except Exception as e:
    logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.warning(
        f'Failed to configure CloudWatch due to the following error: {str(e)}')


@app.after_request
def after_request(response):
    info = {
        'remote_addr': request.remote_addr,
        'request_time': str(datetime.utcnow()),
        'method': request.method,
        'path': request.path,
        'scheme': request.scheme.upper(),
        'status_code': response.status_code,
        'status': response.status,
        'content_length': response.content_length,
        'user_agent': str(request.user_agent),
        'payload': {
            'last_name': request.json['last_name'] if 'last_name' in request.json else '',
            'gender_id': request.json['gender_id'] if 'gender_id' in request.json else ''
        }
    }
    if info['status_code'] >= 200 and info['status_code'] < 300:
        logger.info(info)
    else:
        logger.error(info)
    return response


@app.teardown_appcontext
def cleanup(resp_or_exc):
    '''
    A session establishes all conversations with the database. 
    Mainly, it requests a connection with the database. 

    A session can have a lifespan across many *short* transactions. For web applications, 
        the scope of a session should align with the scope of a request. 
        In other words: tear down the session at the end of a request.

        This decorator function ensures that Sessions are removed at the end of a request.

        References:
        - https://docs.sqlalchemy.org/en/13/orm/contextual.html#using-thread-local-scope-with-web-applications
        - https://dev.to/nestedsoftware/flask-and-sqlalchemy-without-the-flask-sqlalchemy-extension-3cf8
    '''
    Session.remove()
