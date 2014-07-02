app.controller("transacoesController", function($scope, ngTableParams, $http) {

    $scope.contas = [];
    $scope.categorias = [];
    $scope.transacoes =[];
    $scope.pessoas = [];

    $scope.transacaoEmEdicao;
    $scope.radioVisualizaTransacao = "todas";
    $scope.mes = new Date();

    $scope.inicializaDados = function(){

        // Carrega Categorias
        $http.get('/service/categoriaServ/listar').success(function (categorias){
            $scope.categorias = categorias;
        });

        $http.get('/service/contaServ/listar').success(function (contas){
            $scope.contas = contas;
        });

         $http.get('/service/pessoaServ/listar').success(function (pessoas){
            $scope.pessoas = pessoas;
        });

        $http.get('/service/transacao_serv/listar').success(function (transacoes){
            $scope.transacoes  = transacoes;
        });
    };

    $scope.incrementaMesFiltro = function() {
        if ($scope.mes) {
            $scope.mes.setMonth($scope.mes.getMonth() + 1);
        };
    };

    $scope.decrementaMesFiltro = function() {
        if ($scope.mes) {
            $scope.mes.setMonth($scope.mes.getMonth() - 1);
        };
    };


    $scope.dateFiltroOptions = {
        datepickerMode:"'month'",
        minMode:"month",
        dateFormat:"MMMM/yyyy"
    };


    $scope.tableParams = new ngTableParams({
        page: 1, // show first page
        count: 10           // count per page
    }, {
        counts: [], // hide page counts control
        total: 1,  // value less than count hide pagination
        //  total: $scope.transacoes.length, // length of data
        getData: function($defer, params) {
            $defer.resolve($scope.transacoes.slice((params.page() - 1) * params.count(), params.page() * params.count()));
            // $defer.resolve($scope.transacoes);
        }
    });

    $scope.setTransacaoEdicao = function(transacao) {
        $scope.transacaoEmEdicao = angular.copy(transacao);
    };

    $scope.adicionarTransacao = function() {
        $scope.transacaoEmEdicao = {};
    };

    $scope.salvarTransacao = function(transacao) {

        console.log($scope.transacaoEmEdicao);

        $scope.transacaoEmEdicao = {complemento:'Teste'};

        $http.post('/service/transacao_serv/salvar', $scope.transacaoEmEdicao).success(function(transacaoSalva){
            if ($scope.transacaoEmEdicao.id) {
                transacao = transacaoSalva;
            } else {
                $scope.transacoes.push(transacaoSalva);
            };
        });
    };

    $scope.cancelarEdicaoTransacao = function() {
        $scope.transacaoEmEdicao = null;
    };

    $scope.incluirCategoria = function () {
        categoria = {descricao:'Nova categoria', tipo:'Despesa'};
        $http.post('/model/service/categoriaServ/salvar', categoria).success(function(data){
            $scope.carregarCategorias();
        });

    };
});
