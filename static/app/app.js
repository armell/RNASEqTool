'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
    'angularFileUpload',
    'ngRoute',
    'myApp.expression',
    'myApp.view2',
    'myApp.version',
    'ui.grid',
    'ui.grid.pagination',
    'ui.grid.selection',
    'ui.grid.exporter',
    'ngTouch',
    'ngMaterial',
    'ngAnimate',
    'ngAria',
    'ngMessages'
]).
    config(['$routeProvider', '$locationProvider', '$mdThemingProvider', function ($routeProvider, $locationProvider, $mdThemingProvider) {
        $routeProvider.otherwise({redirectTo: '/expression'});
        $mdThemingProvider.theme('default')
            .primaryPalette('deep-purple')
            .accentPalette('indigo');
        //$locationProvider.html5Mode(true);
    }]).controller('MainController', ["$scope", "$mdSidenav", function ($scope, $mdSidenav) {
        $scope.openLeftMenu = function () {
            $mdSidenav('left').toggle();
        };
    }]);
