"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import os

import flask


system = flask.Blueprint('system', __name__)


@system.route('/node_modules/angular/<path:path>')
def serve_angular(path):
    """Serve AngularJS."""
    return flask.send_from_directory(
        os.path.join('..', 'static', 'node_modules', 'angular'),
        path
    )


@system.route('/js/<path:path>')
def serve_javascript(path):
    """Serve javascript."""
    return flask.send_from_directory(
        os.path.join('..', 'static', 'js'),
        path
    )
