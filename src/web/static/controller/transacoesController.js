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
        $http.get('/service/categoria_serv/listar').success(function (categorias){
            $scope.categorias = categorias;

            if ($scope.categorias.length === 0) {

                dadosEnvio = {descricao:'Alimentação'};
                $http.post('/service/categoria_serv/salvar', dadosEnvio).success(function(categoriaSalva){
                    $scope.categorias.push(categoriaSalva)
                });

                dadosEnvio = {descricao:'Transferência'};
                $http.post('/service/categoria_serv/salvar', dadosEnvio).success(function(categoriaSalva){
                    $scope.categorias.push(categoriaSalva)
                });

                dadosEnvio = {descricao:'Salário'};
                $http.post('/service/categoria_serv/salvar', dadosEnvio).success(function(categoriaSalva){
                    $scope.categorias.push(categoriaSalva)
                });

            };
        });



        $http.get('/service/conta_serv/listar').success(function (contas){
            $scope.contas = contas;

            if ($scope.contas.length === 0) {

                dadosEnvio = {nome:'CC BB'};
                $http.post('/service/conta_serv/salvar', dadosEnvio).success(function(contaSalva){
                    $scope.contas.push(contaSalva)
                });

                dadosEnvio = {nome:'CA BB'};
                $http.post('/service/conta_serv/salvar', dadosEnvio).success(function(contaSalva){
                    $scope.contas.push(contaSalva)
                });

                dadosEnvio = {nome:'CC CEF'};
                $http.post('/service/conta_serv/salvar', dadosEnvio).success(function(contaSalva){
                    $scope.contas.push(contaSalva)
                });

            };
        });

        $http.get('/service/pessoa_serv/listar').success(function (pessoas){
            $scope.pessoas = pessoas;
        });

        $scope.carregarTransacoes();
    };

    $scope.carregarTransacoes = function() {
        mes_pesquisar = ($scope.mes.getMonth()+1)+'/'+$scope.mes.getFullYear();

        url = '/service/transacao_serv/listar?mes='+mes_pesquisar+'&confirmada='+$scope.radioVisualizaTransacao;

        $http.get(url).success(function (transacoes){
            $scope.transacoes  = transacoes;
        });
    };

    $scope.selecionouFiltroConfirmadas = function(opcao) {
        $scope.radioVisualizaTransacao = opcao;
        $scope.carregarTransacoes();
    };

    $scope.incrementaMesFiltro = function() {
        if ($scope.mes) {
            $scope.mes = new Date($scope.mes.getFullYear(), $scope.mes.getMonth()+1, 1);
            $scope.carregarTransacoes();
        };
    };

    $scope.decrementaMesFiltro = function() {
        if ($scope.mes) {
            $scope.mes = new Date($scope.mes.getFullYear(), $scope.mes.getMonth()-1, 1);
            $scope.carregarTransacoes();
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
        $scope.transacaoEmEdicao = {confirmada:false, tipo_parcelamento:"S", parcelamento:{tipo_parcelamento:"S"}};
    };

    $scope.salvarTransacao = function(transacao, index) {


        dataSelecionada = transacao.data.getDate()+'/'+(transacao.data.getMonth()+1)+'/'+transacao.data.getFullYear();
        qtParcelas = 0;
        confirmacaoAutomatica = false;
        if (transacao.parcelamento) {
            qtParcelas = transacao.parcelamento.qt_parcelas;
            confirmacaoAutomatica = transacao.parcelamento.confirmacao_automatica;
        }

        dadosEnvio =

        {
            transacao_id: transacao.id,
            complemento: transacao.complemento,
            conta_id: transacao.conta.id,
            categoria_id: transacao.categoria.id,
            valor: transacao.valor,
            confirmada: transacao.confirmada,
            pessoa_id: transacao.pessoa.id,
            pessoa_nome: transacao.pessoa,
            tipo_parcelamento: transacao.tipo_parcelamento,
            nu_parcela: transacao.nu_parcela,
            qt_parcelas: qtParcelas,
            confirmacao_automatica: confirmacaoAutomatica,
            data: dataSelecionada
        };

        if (transacao.id == null) {
            $http.post('/service/transacao_serv/salvar', dadosEnvio).success(function(transacaoSalva){
                $scope.transacoes.push(transacaoSalva);
                $scope.transacaoEmEdicao = null;
            });

        } else {

            $http.post('/service/transacao_serv/atualizar', dadosEnvio).success(function(transacaoSalva){
                $scope.transacoes[index] = transacaoSalva;
                $scope.transacaoEmEdicao = null;
            });

        };
    };

    $scope.cancelarEdicaoTransacao = function() {
        $scope.transacaoEmEdicao = null;
    };

    $scope.openMesFiltro = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.openedMesFiltro = true;
    };

    $scope.openData = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.transacaoEmEdicao.dataAberta = true;
    };
});
