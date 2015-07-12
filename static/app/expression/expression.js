'use strict';

angular.module('myApp.expression', ['ngRoute'])

    .config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
        $routeProvider.when('/expression', {
            templateUrl: 'expression/expression.html',
            controller: 'ExpressionCtrl'
        }).when('/expression/mine', {
            templateUrl: 'expression/expression_mining.html',
            controller: 'ExpressionCtrl'
        }).when('/expression/visualization', {
            templateUrl: 'expression/expression_visualization.html',
            controller: 'ExpressionCtrl'
        }).otherwise({redirectTo: '/expression'});

        //$locationProvider.html5Mode(true)
    }])
    .controller('ExpressionCtrl', ["$scope", "$http", "$log", "$sce", "$mdToast", "$animate", "uiGridConstants", "mainStorage", "visualizationStorage",
        function ($scope, $http, $log, $sce, $mdToast, $animate, uiGridConstants, mainStorage, visualizationStorage) {

            var build_ids = function (selectedGenes) {
                var gene_ids = [];

                for (var i = 0; i < selectedGenes.length; ++i) {
                    gene_ids.push(selectedGenes[i].identifier);
                }

                return gene_ids;
            };

            //var base_path = "http://vps117390.ovh.net:8888/api";
            //var base_path = "http://127.0.0.1:5000/api";
            var base_path = "http://wgs11.op.umcutrecht.nl/RNASeqTool/api";
            $scope.currentExpIdentifier = null;
            $scope.selectedDataSet = null;
            $scope.availableExperiments = null;
            $scope.existingMiningTask = null;
            $scope.maxSamples = 10;
            $scope.distance = 0.7;
            $scope.fullEda = false;
            $scope.goMine = false;
            $scope.exploreBusy = false;
            //$scope.selectedMineChart = undefined;
            //$scope.selectedChartType = null;
            //$scope.selectedGenes = [];

            //colums for visualization grid
            $scope.columns = [
                {name: 'id', field: 'identifier'},
                {name: 'name', field: 'name'},
                {name: 'type', field: 'type'},
                /*                {
                 name: 'distribution',
                 cellTemplate: '<button class="btn btn-default" ng-click="grid.appScope.showMe()">Sample distribution</button>'
                 }*/
            ];

            //colums for EDA grid
            $scope.edaColumns = [
                {name: 'id', field: 'identifier'},
                {name: 'mean'},
                {name: 'sd'},
                {name: 'max'}
            ];

            $scope.edaColumns2 = [
                {name: 'id'},
            ];
            // temp chart options

            //plots for visualization page
            $scope.chartTypes = [
                {id: "heat", name: "Heatmap"},
                //{id:"violin", name:"Violin plot"},
                //{id: "box", name: "Boxplot"},
                {id: "scatter", name: "Scatter plot"}
            ];

            //plots for eda panel
            $scope.plotsForEda = [
                {id: "boxplot", name: "Boxplot"},
                {id: "scatter", name: "Scatter plot"}
            ];

            $scope.techForEda = [
                {id: "limma_mds", name: "Limma MDS"}
            ];

            //$scope.selectedChartType = $scope.chartTypes[0]

            // options for visualization grid
            $scope.gridOptions = {
                columnDefs: $scope.columns,
                enableRowSelection: true,
                enableSelectAll: true,
                paginationPageSizes: [25, 50, 75],
                paginationPageSize: 25,
                enableSorting: true,
                enableFiltering: true,
                enableGridMenu: true,
                exporterCsvLinkElement: angular.element(document.querySelectorAll(".custom-csv-link-location"))
            };

            // options for eda grid
            $scope.edaOptions = {
                columnDefs: $scope.edaColumns,
                enableRowSelection: true,
                enableSelectAll: false,
                multiSelect:false,
                paginationPageSizes: [25, 50, 75],
                paginationPageSize: 25,
                enableSorting: true,
                enableFiltering: true,
                enableGridMenu: true,
                exporterCsvLinkElement: angular.element(document.querySelectorAll(".custom-csv-link-location"))
            };

            $scope.edaOptions2 = {
                columnDefs: $scope.edaColumns2,
                enableRowSelection: true,
                enableSelectAll: true,
                paginationPageSizes: [25, 50, 75],
                paginationPageSize: 25,
                enableSorting: true,
                enableFiltering: true,
                enableGridMenu: true,
                exporterCsvLinkElement: angular.element(document.querySelectorAll(".custom-csv-link-location"))
            };

            $scope.gridOptions.onRegisterApi = function (gridApi) {
                //set gridApi on scope
                $scope.gridApi = gridApi;
                visualizationStorage.grid_api = $scope.gridApi;
                gridApi.selection.on.rowSelectionChanged($scope, function (row) {
                    $scope.selectedGenesFromTable = $scope.gridApi.selection.getSelectedRows();
                    $scope.selected_features = $scope.selectedGenesFromTable;
                    //display selected rows in console
                    $log.log($scope.gridApi.selection.getSelectedRows());
                });
            };

            $scope.edaOptions.onRegisterApi = function (gridApi) {
                //set gridApi on scope
                $scope.edaGridApi = gridApi;
                //visualizationStorage.grid_api = $scope.gridApi;
                gridApi.selection.on.rowSelectionChanged($scope, function (row) {
                    $scope.selectedGenesFromEdaTable = $scope.edaGridApi.selection.getSelectedRows();
                    $scope.numberSelectedGenes = $scope.selectedGenesFromEdaTable.length;
                    $log.log($scope.gridApi.selection.getSelectedRows());
                });
            };

            $scope.edaOptions2.onRegisterApi = function (gridApi) {
                //set gridApi on scope
                $scope.eda2GridApi = gridApi;
                //visualizationStorage.grid_api = $scope.gridApi;
                gridApi.selection.on.rowSelectionChanged($scope, function (row) {
                    $scope.selectedSamplesFromEdaTable = $scope.eda2GridApi.selection.getSelectedRows();
                    $scope.numberSelectedSamples = $scope.selectedSamplesFromEdaTable.length;
                    $log.log($scope.gridApi.selection.getSelectedRows());
                });
            };


            // load default experiment
            $scope.$watch('experimentSelection', function (newValue, oldValue) {
                if ($scope.experimentSelection != null)
                    init_experiment(newValue.data.public_identifier);
            });

            //tracks if the mining task selected has changed an sets the selected dataset
            $scope.$watch('existingMiningTask', function (newValue, oldValue) {
                $log.log('changed mining task');
                $log.log($scope.existingMiningTask);
                if ($scope.existingMiningTask != null) {
                    $scope.selectedDataSet = $scope.existingMiningTask.data.dataset;
                    $scope.apply();
                }
            });

            //loads the page with the selected experiment
            var init_experiment = function (identifier) {
                if (mainStorage.last_experiment == null || mainStorage.last_experiment.public_identifier != identifier) {
                    $http.get(base_path + "/expression/experiment/" + identifier, {headers: {"Accept": "application/json"}}).then(function (payload) {
                        $scope.selectedGenesFromTable = [];
                        $scope.currentExperiment = payload.data;
                        $log.log($scope.currentExperiment);
                        $scope.datasets = $scope.currentExperiment.datasets;
                        $scope.selectedDataSet = $scope.datasets[0];
                        $scope.currentExpIdentifier = $scope.currentExperiment.experiment;
                        $scope.selectedMineChart = $scope.chartTypes[0]
                        $http.get(base_path + '/expression/tasks', {headers: {"Accept": "application/json"}}).success(function (data) {
                            $scope.existingMiningTasks = data;
                        });

                        mainStorage.last_experiment = $scope.currentExperiment;
                        visualizationStorage.last_grid = $scope.gridOptions;
                        visualizationStorage.selected_features = $scope.selectedGenesFromTable;
                        visualizationStorage.last_columns = $scope.columns;

                        $log.log("experiment loaded");
                        $log.log($scope.datasets);
                        $log.log($scope.selectedDataSet);
                        $log.log(payload);
                    });
/*
                    $http.get(base_path + "/expression/methods/", {headers: {"Accept": "application/json"}})
                        .success(function (payload) {
                            $scope.selectedGenesFromTable = [];
                            $scope.currentExperiment = payload.data;
                            $log.log($scope.currentExperiment);
                            $scope.datasets = $scope.currentExperiment.datasets;
                            $scope.selectedDataSet = $scope.datasets[0];
                            mainStorage.last_experiment = $scope.currentExperiment;
                            visualizationStorage.last_grid = $scope.gridOptions;
                            visualizationStorage.selected_features = $scope.selectedGenesFromTable;

                            $log.log("experiment loaded");
                            $log.log($scope.datasets);
                            $log.log($scope.selectedDataSet);
                            $log.log(payload);
                        }).error(function () {

                        });*/
                }
                else {
                    /*
                     here the page has been loaded again so we retrieve old information
                     from the storage variables (main and visualization) so the user
                     finds the page in the same state (almost, some stuff is missing)
                     */
                    $log.log("reset");
                    loadExperimentsList();
                    $log.log(mainStorage.last_experiment);
                    $scope.currentExperiment = mainStorage.last_experiment;
                    $scope.currentExpIdentifier = $scope.currentExperiment.experiment;
                    $scope.datasets = $scope.currentExperiment.datasets;
                    $scope.selectedDataSet = $scope.datasets[0];
                    $scope.gridOptions = visualizationStorage.last_grid;
                    $scope.currentChart = visualizationStorage.last_chart;

                    //$scope.gridApi = visualizationStorage.grid_api;
                    if (visualizationStorage.selected_features != null)
                        $scope.selectedGenesFromTable = visualizationStorage.selected_features;
                }
            };

            $scope.compareEdaDatasets = function () {

                var datasets = [];
                var selectedGenes = build_ids($scope.selectedGenesFromEdaTable);
                var chart_type = $scope.edaPlots.id;

                for (var i = 0; i < $scope.currentExperiment.datasets.length; i++) {
                    if ($scope.currentExperiment.datasets[i].selected == true) {
                        var public_identifier = $scope.currentExperiment.datasets[i].data.public_identifier;
                        datasets.push(public_identifier);
                    }
                }

                var message = {
                    "compare_datasets":datasets,
                    "features":selectedGenes,
                    "chart_type":chart_type,
                    "local":true
                };

                $http.post(base_path + '/expression/tasks', message, {
                    headers: {
                        "Accept": "text/html", //get plot as html
                        "X-Testing": "testing"
                    }
                }).success(function (data) {
                    $scope.edaChart = $sce.trustAsHtml(data);
                    $scope.exploreBusy = false;
                }).error(function () {
                    $scope.exploreBusy = false;
                });
            };

            $scope.loadEdaDatasets = function () {
                $log.log($scope.selectedEdaData);
                $scope.exploreBusy = true;
                $scope.edaOptions.data = null;
                $scope.edaOptions2.data = null;
                for (var i = 0; i < $scope.currentExperiment.datasets.length; i++) {
                    if ($scope.currentExperiment.datasets[i].selected == true) {
                        var public_identifier = $scope.currentExperiment.datasets[i].data.public_identifier;

                        $http.get(base_path + '/expression/dataset/' + public_identifier + '/desc', {headers: {"Accept": "application/json"}}).success(function (data) {
                            $scope.edaOptions.data = data.descriptive;
                            $scope.edaOptions2.data = data.samples;
                            $scope.edaMeta = data.meta;
                            $scope.exploreBusy = false;
                        }).error(function () {
                            $scope.exploreBusy = false;
                        });

                        break;
                    }
                }
            };

            if (mainStorage.last_experiment != null)
                init_experiment(null);
            else {
                loadExperimentsList();
            }

            //gets a list of available experiments
            function loadExperimentsList() {
                $http.get(base_path + '/expression/experiments', {headers: {"Accept": "application/json"}}).success(function (data) {
                    $scope.availableExperiments = data.items;
                })
            }

            $scope.sampleSelected = function () {
                $log.log($scope.selectedDataSet.href);
                $scope.processingInProgress = true;
                $http.get($scope.selectedDataSet.href + '/genes', {headers: {"Accept": "application/json"}}).success(function (data) {
                    $log.log(data);
                    $scope.gridOptions.data = data;
                    $scope.processingInProgress = false;
                }).error(function (data) {
                    $scope.processingInProgress = false;
                });
            };

            $scope.selectedDataset = function (dataset) {
                $scope.selectedDataSet = dataset;
            };

            $scope.selectNormalizationMethod = function (method) {
                $log.log("selected methods " + method.data.public_identifier);
                $scope.selectedNormalizationMethod = method.data.public_identifier;
                $scope.selectedNormalizationMethodName = method.data.name;
            };

            $scope.selectMiningMethod = function (method) {
                $log.log(method);
                $scope.mine = method;
            };


            var getInformationAboutNormMethod = function (method_identifier) {
                $http.get(base_path + '/expression/method/' + method_identifier + '/all', {headers: {"Accept": "application/json"}}).success(function (data) {
                    $log.log(data);

                    $scope.infoMethods = data;
                }).error(function (data) {

                });
            };

            var getInformationAboutMineMethod = function (method_identifier) {
                $http.get(base_path + '/expression/method/' + method_identifier + '/all', {headers: {"Accept": "application/json"}}).success(function (data) {
                    $log.log(data);

                    $scope.infoMethodsMine = data;
                }).error(function (data) {

                });
            };

            $scope.getInfo = function () {
                $log.log("info normalization");
                getInformationAboutNormMethod($scope.normalizationMethod);
            };

            $scope.getInfoMine = function () {
                $log.log("info mine");
                getInformationAboutMineMethod($scope.mine);
            };


            $scope.compareGeneDistribution = function (header, type_of_chart) {
                //$("#charts").empty();
                //$scope.$apply();
                $scope.processingInProgress = true;
                var selectedGenes = $scope.selected_features;
                $log.log("selected genes");
                $log.log(selectedGenes);

                var gene_ids = build_ids(selectedGenes);
                var message = {
                    gene_set: gene_ids,
                    chart_type: type_of_chart.id,
                    experiment_identifier: $scope.currentExperiment.experiment,
                    dataset_identifier: $scope.selectedDataSet.data.public_identifier
                };

                $log.log(message);

                var accept_header = (header == "pdf" ? "application/pdf" : "text/html");

                $http.post(base_path + "/expression/charts",
                    message
                    , {
                        headers: {
                            "Accept": accept_header, //get plot as html
                            "X-Testing": "testing"
                        }
                    }).success(function (data, status, headers, config) {

                        if (header == "html") {
                            $scope.currentChart = $sce.trustAsHtml(data);
                            visualizationStorage.last_chart = $scope.currentChart;
                            $log.log("chart loaded");
                        }
                        else {
                            $log.log(data)
                            //window.open("data:application/pdf, " + );
                            //var content = window.btoa(data);
                            var url_to_file = data;
                            window.open(data);
                        }
                        $scope.processingInProgress = false;

                    }).error(function (data, status, headers, config) {
                        $log.log("BOOOM" + data);
                        $scope.processingInProgress = false;
                    });
            };

            //$scope.exploreData();

            $scope.preprocess = function () {
                $log.log("called preprocess");
                $log.log($scope.selectedDataSet.data.public_identifier);
                $log.log($scope.normalizationMethod);
                $log.log($scope.selectedNormalizationMethod);


                if ($scope.normalizationMethod != null) {
                    $scope.selectNormalizationMethod = false;
                    $scope.processingInProgress = true;

                    $http.post(base_path + "/expression/datasets", {
                        dataset_identifier: $scope.selectedDataSet.data.public_identifier,
                        preprocessing_method_identifier: $scope.selectedNormalizationMethod,
                        experiment_identifier: $scope.currentExperiment.experiment
                    }, {
                        headers: {"Accept": "application/json"}
                    }).success(function (data, status, headers, config) {
                        //$scope.datasets.push(data);
                        $mdToast.show(
                            $mdToast.simple()
                                .content('Preprocessing successfuly executed!')
                                .position($scope.getToastPosition())
                                .hideDelay(3000)
                        );
                        $scope.datasets.push(data);
                        $scope.processingInProgress = false;
                    }).error(function (data, status, headers, config) {
                        $log.log("BOOOM" + status);
                        $log.log(data);
                        $scope.processingInProgress = false;
                    });
                }
                else {
                    $scope.selectNormalizationMethod = true;
                }
            };
            var add = function () {
                visualizationStorage.last_columns.push({
                    field: 'samples', type: 'number', filters: [
                        {
                            condition: uiGridConstants.filter.GREATER_THAN,
                            placeholder: 'greater than'
                        },
                        {
                            condition: uiGridConstants.filter.LESS_THAN,
                            placeholder: 'less than'
                        }
                    ]
                });
                visualizationStorage.last_columns.push({
                    field: 'distance', type: 'number', filters: [
                        {
                            condition: uiGridConstants.filter.GREATER_THAN,
                            placeholder: 'greater than'
                        },
                        {
                            condition: uiGridConstants.filter.LESS_THAN,
                            placeholder: 'less than'
                        }
                    ]
                });
                visualizationStorage.last_columns.push({
                    field: 'range', type: 'number', filters: [
                        {
                            condition: uiGridConstants.filter.GREATER_THAN,
                            placeholder: 'greater than'
                        },
                        {
                            condition: uiGridConstants.filter.LESS_THAN,
                            placeholder: 'less than'
                        }
                    ]
                });
            };

            $scope.executeJob = function (selectedJob) {
                var new_data = [];
                visualizationStorage.last_grid.data = [];
                $scope.$apply();
                $scope.miningInProgress = true;
                add();
                oboe({
                    url: selectedJob,
                    headers: {"Accept": "application/json"},
                    cached: false
                }).path('outliers.*', function () {
                    $log.log("got something here");
                }).node('outliers.*', function (outlier) {
                    //new_data.push(outlier)
                    visualizationStorage.last_grid.data.push(outlier);
                    $scope.$apply();
                    //$log.log('Go check this ' + outlier.identifier);
                }).done(function (things) {
                    $log.log(things.length);
                    $scope.miningInProgress = false;
                    $mdToast.show(
                        $mdToast.simple()
                            .content('Everything is loaded!')
                            .position($scope.getToastPosition())
                            .hideDelay(3000)
                    );
                }).fail(function (things) {
                    $scope.miningInProgress = false;
                    $mdToast.show(
                        $mdToast.simple()
                            .content('Sorry, something went wrong !')
                            .position($scope.getToastPosition())
                            .hideDelay(3000)
                    );
                });
            };

            $scope.scheduleJob = function () {
                $log.log($scope.mine.public_identifier)
                if ($scope.mine.data.public_identifier == "cluster_umc_kloosterman_01") {
                    $log.log("kmeans mining");
                    $log.log($scope.currentExperiment);
                    var message = {
                        method_identifier: "kmeans_outliers",
                        dataset_identifier: $scope.selectedDataSet.data.public_identifier,
                        min_samples: $scope.maxSamples,
                        min_distance: $scope.distance,
                        experiment_identifier: $scope.currentExperiment.experiment
                    };

                    $http.post(base_path + '/expression/tasks', message, {
                        headers: {"Accept": "application/json"}
                    }).success(function (data) {
                        $scope.scheduled = true;
                        $mdToast.show(
                            $mdToast.simple()
                                .content('Job ' + data.data.public_identifier + ' is configured')
                                .position($scope.getToastPosition())
                                .hideDelay(3000)
                        );
                    }).error(function (data) {
                        $mdToast.show(
                            $mdToast.simple()
                                .content('Sorry, something went wrong !')
                                .position($scope.getToastPosition())
                                .hideDelay(3000)
                        );
                    });

                }
                else if ($scope.mine.mad) {
                    $log.log("mad mining");

                }
            }

            $scope.toastPosition = {
                bottom: true,
                top: false,
                left: false,
                right: true
            };

            $scope.getToastPosition = function () {
                return Object.keys($scope.toastPosition)
                    .filter(function (pos) {
                        return $scope.toastPosition[pos];
                    })
                    .join(' ');
            };


        }
    ]).factory('mainStorage', [function () {
        var serviceInstance = {
            last_experiment: null
        };

        return serviceInstance;
    }]).factory('visualizationStorage', [function () {
        var serviceInstance = {
            last_grid: null,
            grid_api: null,
            selected_features: null,
            last_chart: null,
            job_url: null,
            last_columns: null
        };

        return serviceInstance;
    }]);

