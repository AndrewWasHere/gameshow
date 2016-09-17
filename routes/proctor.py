"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import flask


proctor = flask.Blueprint('proctor', __name__)


@proctor.route('/proctor')
def control_panel():
    """Proctor control panel."""
    return flask.current_app.send_static_file('proctor.html')
