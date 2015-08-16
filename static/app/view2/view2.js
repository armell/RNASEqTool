'use strict';

angular.module('myApp.view2', ['ngRoute', 'ngMaterial', 'ngTouch'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/view2', {
            templateUrl: 'view2/view2.html',
            controller: 'View2Ctrl'
        }).when('/view2/experiment', {
            templateUrl: 'view2/new_experiment.html',
            controller: 'View2Ctrl'
        }).when('/view2/help', {
            templateUrl: 'view2/help.html',
            controller: 'View2Ctrl'
        });
    }])

    .controller('View2Ctrl', ["$scope", "$http", "$log", "$sce", "$upload", "$mdDialog", "$mdToast", function ($scope, $http, $log, $sce, $upload, $mdDialog, $mdToast) {
        //var base_url = "http://vps117390.ovh.net:8888/api";
        //var base_url = 'http://127.0.0.1:5000/api';
        var base_url = "http://wgs11.op.umcutrecht.nl/RNASeqTool/api";
        $scope.displayFiles = [];
        var load_page = function () {

            load_datasets();

            $http.get(base_url + '/expression/experiments', {headers: {"Accept": "application/json"}}).success(function (data, status) {
                $scope.displayExperiments = data.items;
                $log.log(data.items);
            }).error(function (data, status) {
                $log.log("")
            });
        };

        function load_datasets() {
            $http.get(base_url + '/expression/datasets', {headers: {"Accept": "application/json"}}).success(function (data, status) {
                $scope.displayFiles = data;
            }).error(function (data, status) {
                $log.log("")
            });
        }

        // $scope.message = "hello from controller !";
        $scope.file_types = ["raw gene counts", "genes normalized dataset"];
        $scope.filesMonitoring = [];
        $scope.savedFiles = [];
        $scope.selectedUploadedFile = null;

        load_page();

        $scope.createNewExperiment = function () {

            $http.post(base_url + "/expression/experiments", $scope.newExperiment, {headers: {"Accept": "application/json"}}).success(function (data, status) {
                showToastie("Experiment created");
                $scope.expJustCreated = data;
            }).error(function (data, status) {
                showToastie("Could not create the experiment");
                $scope.errorMessageNewExperiment = data;
                $scope.expJustCreated = false;
            });
        }

        $scope.updatedMetadata = function (identifier) {
            $log.log("updated file " + identifier);
            var element = null;
            for (var i = 0; i < $scope.savedFiles.length; i++) {
                if ($scope.savedFiles[i].intern_identifier == identifier)
                    element = $scope.savedFiles[i]
            }
            ;

            $log.log(element);
            var data = {
                "dataset_identifier": element.filename
            };
            //$log.log($scope.savedFiles)
            $http.put(base_url + "/expression/dataset/" + identifier + '/genes', data, {headers: {"Accept": "application/json"}}).success(function (data, status) {
                $log.log("updated");

                //reload dataset table
                load_page();
            }).error(function (data, status) {
                $log.log(" could not update meta data")
            });
        };

        $scope.$watch('files', function () {
            $scope.upload($scope.files);
        });

        $scope.showConfirm = function (ev) {
            // Appending dialog to document.body to cover sidenav in docs app
            var message = "Link resources ";
            var data_identifiers = [];
            var count = 0;
            for (var i = 0; i < $scope.displayFiles.length; i++) {
                if ($scope.displayFiles[i].active == true) {

                    if (count > 0)
                        message += " and ";

                    message += $scope.displayFiles[i].data.public_identifier;
                    data_identifiers.push($scope.displayFiles[i].data.public_identifier);
                    count++;
                    //$scope.showConfirm($event);
                }
            }

            message += " to " + $scope.selectedExperiment.data.public_identifier;

            $log.log("creating dialog");
            if (message != null) {
                $log.log(angular.element(document.body));
                var confirm = $mdDialog.confirm()
                    //.parent(angular.element(document.body))
                    .title('Would you like to link the selected dataset(s)?')
                    .content(message)
                    .ariaLabel('Confirmation')
                    .ok('Yup!')
                    .cancel('Nope!!')
                    .targetEvent(ev);
                $log.log("show dialog");
                $mdDialog.show(confirm).then(function () {
                    var experiment_id = $scope.selectedExperiment.data.public_identifier;
                    $log.log("linking data")
                    $http.put(base_url + '/expression/experiment/' + experiment_id, {'linked_datasets': data_identifiers}, {headers: {"Accept": "application/json"}}).success(function (data) {
                        load_datasets();
                        showToastie("Data sets are linked");
                    }).error(function (data) {

                    });
                }, function () {
                    showToastie("Could not proceed with your request dear user");
                });
            }
        };

        function showToastie(sayNoMore) {
            $mdToast.show(
                $mdToast.simple()
                    .content(sayNoMore)
                    .position($scope.getToastPosition())
                    .hideDelay(3000)
            );
        }

        $scope.upload = function (files) {

            if (files && files.length) {
                for (var i = 0; i < files.length; i++) {
                    var file = files[i];
                    $scope.filesMonitoring.push({filename: file.name, progress: 0});
                    $upload.upload({
                        url: base_url + '/expression/datasets',
                        fields: {'name': 'new_file'},
                        file: file,
                        headers: {"Accept": "application/json"}
                    }).progress(function (evt) {
                        var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                        $scope.filesMonitoring[files.indexOf(evt.config.file)].progress = progressPercentage;

                        //console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
                    }).success(function (data, status, headers, config) {
                        //console.log('file ' + config.file.name + 'uploaded. Response: ' + data);

                        $scope.savedFiles.push(data);
                    }).error(function (data, satus, headers, config) {
                        showToastie("could not process this file")
                        $scope.savedFiles = [];
                    });
                }
            }
        };

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

    }]).factory('simpleAdminStorage', [function () {

    }]);