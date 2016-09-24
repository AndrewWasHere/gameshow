# Gameshow

A webapp for hosting [GameShowBuzzers](https://github.com/AndrewWasHere/GameShowBuzzer),
and scoring games.

## Dependencies

Python dependencies are listed in requirements.txt, and can be installed
using pip:

    pip install -r requirements.txt
    
AngularJS 1.5.8 must be installed from the static/ directory via npm.

    cd static
    npm install angular@1.5.8

## Endpoints

* / - Scorecard (GET)
* /players - Get current players and scores (GET)
* /players/<id> - Buzzer endpoint (POST)
* /players/<id>/score - Update player score (POST)
* /proctor - Proctor control panel (GET)


## License

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
