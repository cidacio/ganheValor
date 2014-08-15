app.controller("orcamentoController", function ($scope, $http) {

    $scope.carregar_dados_grafico = function () {

        mes = new Date();

        mes_pesquisar = mes.getFullYear() + '-' + (mes.getMonth() + 1) + '-' + mes.getDate()

        url = '/rest/orcamento/consultar_orcamento_grafico?mes_inicial=' + mes_pesquisar;

        $http.get(url).success(function (dados) {
            $scope.chartObject.data.rows = dados;
        });
    };


    $scope.chartObject = {
        "type": "LineChart",
        "displayed": false,
        "data": {
            "cols": [
                {
                    "id": "month",
                    "label": "Month",
                    "type": "string",
                    "p": {}
                },
                {
                    "id": "saldo-acumulado",
                    "label": "Saldo acumulado",
                    "type": "number",
                    "p": {}
                },
                {
                    "id": "saldo-mes",
                    "label": "Saldo mensal",
                    "type": "number",
                    "p": {}
                }
            ],
            "rows": []
        },
        "options": {
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": true,
            "vAxis": {
                "title": "Montante",
                "gridlines": {
                    "count": 10
                }
            }
        },
        "formatters": {},
        "view": {}
    }
});