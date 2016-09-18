(function() {
    var app = angular.module('scoreboardApp', []);
    app.controller(
        'ScoreboardController',
        [
            '$http', '$interval', '$scope',
            function($http, $interval, $scope) {
                var update_interval = 1000;  // milliseconds.
                $scope.players = [];
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
            }
        ]
    );
})();
