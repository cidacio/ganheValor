var app = angular.module("ganheValor", ['ngRoute', 'ui.treeview', 'ui.bootstrap', 'ngTable', 'ui.select2', 'googlechart']);

app.config(function ($routeProvider) {
    $routeProvider
        .when('/home', {templateUrl: '/static/view/home.html', controller: 'homeController'})
        .when('/orcamento', {templateUrl: '/static/view/orcamento.html', controller: 'orcamentoController'})
        .when('/transacoes', {templateUrl: '/static/view/transacoes/transacoes.html', controller: 'transacoesController'})
        .otherwise({redirectTo: 'home'});
});

app.config(function (datepickerConfig, datepickerPopupConfig) {
    datepickerPopupConfig.currentText = 'Hoje';
    datepickerPopupConfig.clearText = "Limpar";
    datepickerPopupConfig.closeText = "Fechar";
    datepickerConfig.formatYear = "yyyy";
    //uiSelectConfig.theme = 'bootstrap';
});

app.value('googleChartApiConfig', {
    version: '1',
    optionalSettings: {
        packages: ['corechart'],
        language: 'pt'
    }
});
