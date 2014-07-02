var app = angular.module("ganheValor", ['ngRoute', 'ui.treeview', 'ui.bootstrap', 'ngTable', 'ui.select2']);

app.config(function($routeProvider) {
    $routeProvider
            .when('/home', {templateUrl: '/static/view/home.html', controller: 'homeController'})
            .when('/transacoes', {templateUrl: '/static/view/transacoes/transacoes.html', controller: 'transacoesController'})
            .otherwise({redirectTo: 'home'});
});

app.config(function(datepickerConfig, datepickerPopupConfig) {
    datepickerPopupConfig.currentText = 'Hoje';
    datepickerPopupConfig.clearText = "Limpar";
    datepickerPopupConfig.closeText = "Fechar";
    datepickerConfig.formatYear= "yyyy";
    //uiSelectConfig.theme = 'bootstrap';
});
