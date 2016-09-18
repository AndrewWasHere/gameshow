(function() {
    var app = angular.module('proctorApp', []);
    app.controller('ProctorController', ['$http', '$interval', '$scope',
        function($http, $interval, $scope) {
            var update_interval = 1000;  // milliseconds.

            $scope.players = [];

            this.increaseScore = function(name) {
                this.changeScore(name, '+1');
            };

            this.decreaseScore = function(name) {
                this.changeScore(name, '-1');
            };

            this.resetScores = function() {
                var parent = this;
                $scope.players.forEach(function(p) {
                    parent.changeScore(p.name, '0');
                });
            };

            this.changeScore = function(name, val) {
                var uri_name = name.replace(/ /g, '_');
                var data = {value: val};
                var httpRequest = $http.post(
                    'players/' + uri_name + '/score',
                    data
                ).then(function(response) {})
            };

            this.requestPlayers = function() {
                var httpRequest = $http.get(
                    'players'
                ).then(function(response) {
                    var newPlayers = response.data;
                    try {
                        newPlayers.forEach(function(p) {
                            p.name = p.name.replace(/_/g, ' ');
                        });
                    } catch (e) {
                        newPlayers = [];
                    }
                    $scope.players = newPlayers;
                });
            };

            this.refresh = $interval(this.requestPlayers, update_interval);
    }]);
})();