'use strict';

angular.module('myApp.view1', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/expression', {
            templateUrl: 'expression/expression.html',
            controller: 'View1Ctrl'
        });
    }])

    .controller('View1Ctrl', ["$scope", "$http", "$log", function ($scope, $http, $log) {
        $scope.typeChanged = function () {
            $log.info("adapting chart");

            $scope.chartoptions.chart.type = $scope.selectedType;
            $scope.chart = new Highcharts.Chart($scope.chartoptions);
            drawSeries();
        };

        $scope.setMeanWarn = function () {
            $scope.meanWarn
        }

        $http.get("http://127.0.0.1:5000/genes/charts").then(function (payload) {
            $scope.charts = payload.data.types;
            $scope.selectedType = $scope.charts[0].value;
        });

        $http.get("http://127.0.0.1:5000/genes").then(function (payload) {
            $scope.chartype = $scope.selectedType == null ? 'column' : $scope.selectedType
            $scope.dataset = payload.data.content.dataset;
            $scope.genes = payload.data.content.genes;
            $scope.samples = payload.data.samples;

            drawSeries();
        });

        var drawSeries = function () {
            var serieData = [];
            var catNames = [];
            for (var i = 0; i < $scope.genes.length; ++i) {
                $log.info($scope.genes[i]["mean"]);
                serieData[i] = $scope.genes[i]["mean"];
                catNames[i] = $scope.genes[i]["name"];
            }
            $log.info(serieData);
            $scope.chart.addSeries({"name": "all samples", "data": serieData});
            $scope.chart.xAxis[0].setCategories(catNames);
        }

        var removeAllSeries = function (chart) {
            while (chart.series.length > 0)
                chart.series[0].remove(true);
        };

        var changeToPlot = function (chart) {
            chart.type = "line";
        };

        $scope.chartoptions = {
            chart: {
                renderTo: "genchart",
                type: $scope.chartype
            },
            credits: false,
            title: {
                text: 'Demo data 11 12',
                x: -20 //center
            },
            subtitle: {
                text: 'Overview of interaction with charts and data',
                x: -20
            },
            xAxis: {},
            yAxis: {
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: ' mean counts'
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            }
        };
    }])
    .directive('myChart', function () {
        function link(scope, element, attrs) {
            scope.chart = new Highcharts.Chart(scope.chartoptions);
        };

        return {
            link: link
        };
    })
;