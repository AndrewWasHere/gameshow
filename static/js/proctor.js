(function() {
    var app = angular.module('proctorApp', []);
    app.controller('ProctorController', ['$http', '$interval', '$scope',
        function($http, $interval, $scope) {
            this.increaseScore = function(name) {
                this.changeScore(name, '+1');
            };

            this.decreaseScore = function(name) {
                this.changeScore(name, '-1');
            };

            this.resetScores = function() {
                $http.post('proctor/zeroscores').then(function(response) {});
            };

            this.changeScore = function(name, val) {
                var uri_name = name.replace(/ /g, '_');
                var data = {value: val};
                $http.post('players/' + uri_name + '/score', data).then(
                    function(response) {}
                );
            };

            this.requestPlayers = function() {
                $http.get('players').then(function(response) {
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

            this.resetBuzzers = function() {
                $http.post('proctor/resetbuzzers').then(function(response) {});
            };

            this.changeState = function() {
                $http.post('proctor/gamestate').then(this.updateState);
            };

            this.updateState = function(response) {
                var currentState = response.data['state'];
                var nextState = (currentState === 'register') ? 'play': 'register';

                $scope.currentState = currentState;
                $scope.nextState = nextState;
            };

            $scope.players = [];
            $scope.currentState = null;
            $scope.nextState = null;
            $http.get('proctor/gamestate').then(this.updateState);
            $interval(this.requestPlayers, 677);
    }]);
})();