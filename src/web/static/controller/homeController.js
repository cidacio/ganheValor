app.controller("homeController", function($scope, ngTableParams, $http, $location, $window) {

    $scope.searchText = "";
    $scope.data = {};
    $scope.data.productData = [{
        "id": "6000", "Name": "All Categories",  "iconright": "hide", "iconleft": "show", "confirm": false,
        Children: [{
            "id": "6100", "Name": "Juice",  "iconright": "hide", "iconleft": "show", "confirm": false,
            Children: [{
                "id": "6200", "Name": "Mom's Brands",  "iconright": "hide", "iconleft": "show", "confirm": false,
                Children: [{ "id": "6454", "Name": "Mom's Apple Jug",  "iconright": "hide", "iconleft": "show", "confirm": false },
                    { "id": "6456", "Name": "Mom's Apple Juice",  "iconright": "hide", "iconleft": "show", "confirm": false },
                    { "id": "6458", "Name": "Mom's Grape Juice",  "iconright": "hide", "iconleft": "show", "confirm": false },
                    { "id": "6462", "Name": "Mom's Apple Grape Jug",  "iconright": "hide", "iconleft": "show", "confirm": false },
                    { "id": "6463", "Name": "Mom's Pear Blend",  "iconright": "hide", "iconleft": "show", "confirm": false },
                    { "id": "6465", "Name": "ABC Pear Blend",  "iconright": "hide", "iconleft": "show", "confirm": false },
                    { "id": "6464", "Name": "Mom's Juice Cocktail Lite",  "iconright": "hide", "iconleft": "show", "confirm": false }]
            },
                {
                    "id": "6300", "Name": "Sparkle Brands",  "iconright": "hide", "iconleft": "show", "confirm": false,
                    Children: [{ "id": "6392", "Name": "Sparkle Pear Juice",  "iconright": "hide", "iconleft": "show", "confirm": false },
                        { "id": "6393", "Name": "Sparkle Grape Juice Light",  "iconright": "hide", "iconleft": "show", "confirm": false },
                        { "id": "6394", "Name": "Sparkle Apple Juice",  "iconright": "hide", "iconleft": "show", "confirm": false }]
                },
                {
                    "id": "6400", "Name": "Natural Choice",  "iconright": "hide", "iconleft": "show", "confirm": false,
                    Children: [{ "id": "6472", "Name": "Natural Choice Apple Juice",  "iconright": "hide", "iconleft": "show", "confirm": false },
                        { "id": "6474", "Name": "Natural Choice mGrape Juice",  "iconright": "hide", "iconleft": "show", "confirm": false },
                        { "id": "6475", "Name": "Natural Choice Pear Juice",  "iconright": "hide", "iconleft": "show", "confirm": false },
                        { "id": "6476", "Name": "Natural Choice Grape Juice Light",  "iconright": "hide", "iconleft": "show", "confirm": false }]
                },
            ]
        }]
    }];

    $scope.usuario = null;
    $scope.logout_url = null;
    $scope.login_url = null;
    $scope.baseUrl = null;

    $scope.carrega_dados = function(){

        url = '/service/usuario_serv/login';

        $http.get(url).success(function (dados) {
            $scope.usuario = dados.usuario;
            $scope.logout_url = $location.absUrl() + dados.logout_url;
            $scope.login_url = $location.absUrl() + dados.login_url;

        });

    };

    $scope.login = function() {

       // $location.path($scope.login_url);
       // $scope.baseUrl = $location.absUrl();

        $window.location.href = $scope.login_url;
        $window.location.reload();
    };

    $scope.retData = function () {
        return $scope.productData;
    }
    $scope.attr = "Name";
    //$scope.gettreeSel = function () {

    //              //};
    $scope.getSelection = function () {
        var selectedData = $scope.gettreeSel();
    };

});