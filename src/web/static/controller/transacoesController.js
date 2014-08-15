app.controller("transacoesController", function ($scope, ngTableParams, $http) {

    $scope.contas = [];
    $scope.categorias = [];
    $scope.transacoes = [];
    $scope.pessoas = [];
    $scope.saldo_anterior = {};

    $scope.transacaoEmEdicao;
    $scope.radioVisualizaTransacao = "todas";
    $scope.mes = new Date();

    $scope.inicializaDados = function () {

        // Carrega Categorias
        $http.get('/rest/categoria/listar').success(function (categorias) {
            $scope.categorias = categorias;

            if ($scope.categorias.length === 0) {

                dadosEnvio = {descricao: 'Despesas', tipo: 'D'};
                $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                    var categoria_pai = categoriaSalva.id;
                    $scope.categorias.push(categoriaSalva)

                    dadosEnvio = {descricao: 'Transporte', categoria_pai_id: categoria_pai, tipo: 'D'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Alimentação', categoria_pai_id: categoria_pai, tipo: 'D'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Habitação', categoria_pai_id: categoria_pai, tipo: 'D'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Saúde', categoria_pai_id: categoria_pai, tipo: 'D'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Vestuário', categoria_pai_id: categoria_pai, tipo: 'D'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Presentes', categoria_pai_id: categoria_pai, tipo: 'D'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Lazer', categoria_pai_id: categoria_pai, tipo: 'D'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Impostos/Taxas', categoria_pai_id: categoria_pai, tipo: 'D'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Educação', categoria_pai_id: categoria_pai, tipo: 'D'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Veículo', categoria_pai_id: categoria_pai, tipo: 'D'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Juros/Multa', categoria_pai_id: categoria_pai, tipo: 'D'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });
                });

                dadosEnvio = {descricao: 'Receitas', tipo: 'R'};
                $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                    var categoria_pai = categoriaSalva.id;
                    $scope.categorias.push(categoriaSalva)

                    dadosEnvio = {descricao: 'Salário', categoria_pai_id: categoria_pai, tipo: 'R'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Empréstimo', categoria_pai_id: categoria_pai, tipo: 'R'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                    dadosEnvio = {descricao: 'Vendas', categoria_pai_id: categoria_pai, tipo: 'R'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });
                });

                dadosEnvio = {descricao: 'Transferência', tipo: 'T'};
                $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                    var categoria_pai = categoriaSalva.id;
                    $scope.categorias.push(categoriaSalva)

                    dadosEnvio = {descricao: 'Transferências', categoria_pai_id: categoria_pai, tipo: 'T'};

                    $http.post('/rest/categoria/salvar', dadosEnvio).success(function (categoriaSalva) {
                        $scope.categorias.push(categoriaSalva)
                    });

                });

            }
            ;
        });


        $http.get('/rest/conta/listar').success(function (contas) {
            $scope.contas = contas;

            if ($scope.contas.length === 0) {

                dadosEnvio = {nome: 'CC BB'};
                $http.post('/rest/conta/salvar', dadosEnvio).success(function (contaSalva) {
                    $scope.contas.push(contaSalva)
                });

                dadosEnvio = {nome: 'CA BB'};
                $http.post('/rest/conta/salvar', dadosEnvio).success(function (contaSalva) {
                    $scope.contas.push(contaSalva)
                });

                dadosEnvio = {nome: 'CC CEF'};
                $http.post('/rest/conta/salvar', dadosEnvio).success(function (contaSalva) {
                    $scope.contas.push(contaSalva)
                });

            }
            ;

            $scope.carregarTransacoes();

        });

        $http.get('/rest/pessoa/listar').success(function (pessoas) {
            $scope.pessoas = pessoas;
        });
    };

    $scope.carregarTransacoes = function () {
        mes_pesquisar = ($scope.mes.getMonth() + 1) + '/' + $scope.mes.getFullYear();

        url = '/rest/transacao/listar?mes=' + mes_pesquisar + '&confirmada=' + $scope.radioVisualizaTransacao;

        var filtro_contas = $scope.contasSelecionadas();

        url = url + "&contas=" + filtro_contas;

        $http.get(url).success(function (dados) {
            $scope.transacoes = dados.transacoes;
            $scope.saldo_anterior = dados.saldo_anterior;

            transacao = {id: -1};
            $scope.transacoes.push(transacao);
        });
    };

    $scope.selecionouFiltroConfirmadas = function (opcao) {
        $scope.radioVisualizaTransacao = opcao;
        $scope.carregarTransacoes();
    };

    $scope.incrementaMesFiltro = function () {
        if ($scope.mes) {
            $scope.mes = new Date($scope.mes.getFullYear(), $scope.mes.getMonth() + 1, 1);
            $scope.carregarTransacoes();
        }
        ;
    };

    $scope.decrementaMesFiltro = function () {
        if ($scope.mes) {
            $scope.mes = new Date($scope.mes.getFullYear(), $scope.mes.getMonth() - 1, 1);
            $scope.carregarTransacoes();
        }
        ;
    };

    $scope.dateFiltroOptions = {
        datepickerMode: "'month'",
        minMode: "month",
        dateFormat: "MMMM/yyyy"
    };

    $scope.tableParams = new ngTableParams({
        page: 1, // show first page
        count: 10           // count per page
    }, {
        counts: [], // hide page counts control
        total: 1,  // value less than count hide pagination
        //  total: $scope.transacoes.length, // length of data
        getData: function ($defer, params) {
            $defer.resolve($scope.transacoes.slice((params.page() - 1) * params.count(), params.page() * params.count()));
            // $defer.resolve($scope.transacoes);
        }
    });

    $scope.setTransacaoEdicao = function (transacao) {
        $scope.transacaoEmEdicao = angular.copy(transacao);
    };

    $scope.adicionarTransacao = function () {
        $scope.transacaoEmEdicao = {id: -1, confirmada: false, tipo_parcelamento: "S", parcelamento: {tipo_parcelamento: "S"}};
    };

    $scope.salvarTransacao = function (transacao, index) {


        transacao.data = new Date(transacao.data);
        dataSelecionada = transacao.data.toISOString();
        qtParcelas = 0;
        confirmacaoAutomatica = false;
        if (transacao.parcelamento) {
            qtParcelas = transacao.parcelamento.qt_parcelas;
            confirmacaoAutomatica = transacao.parcelamento.confirmacao_automatica;
        }
        ;

        dadosEnvio =

        {
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

        if (transacao.id === -1) {
            $http.post('/rest/transacao/salvar', dadosEnvio).success(function (transacaoSalva) {

                if ($scope.atendeFiltro(transacaoSalva)) {
                    $scope.transacoes.push(transacaoSalva);
                }
                ;

                $scope.transacaoEmEdicao = null;
            });

        } else {

            dadosEnvio.transacao_id = transacao.id;
            dadosEnvio.atualiza_parcelamento = false;

            if ((dadosEnvio.tipo_parcelamento != 'S') && confirm("Deseja atualizar as demais parcelas do parcelamento?")) {
                dadosEnvio.atualiza_parcelamento = true;
            }
            ;

            $http.post('/rest/transacao/atualizar', dadosEnvio).success(function (transacaoSalva) {
                if ($scope.atendeFiltro(transacaoSalva)) {
                    $scope.transacoes[index] = transacaoSalva;
                } else {
                    $scope.transacoes.splice(index, 1);
                }
                ;
                $scope.transacaoEmEdicao = null;
            });
        }
        ;
    };

    $scope.cancelarEdicaoTransacao = function () {
        $scope.transacaoEmEdicao = null;
    };

    $scope.openMesFiltro = function ($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.openedMesFiltro = true;
    };

    $scope.openData = function ($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.transacaoEmEdicao.dataAberta = true;
    };

    $scope.alterarConfirmacao = function (transacao, confirmada, index) {

        dadosEnvio = {transacao_id: transacao.id, confirmada: confirmada};

        $http.post('/rest/transacao/atualizar', dadosEnvio).success(function (transacaoSalva) {
            if ($scope.atendeFiltro(transacaoSalva)) {
                transacao.confirmada = confirmada;
            } else {
                $scope.transacoes.splice(index, 1);
            }
            ;
        });
    };

    $scope.atendeFiltro = function (transacao) {

        var mesFiltro = ($scope.mes.getMonth() + 1) + '/' + $scope.mes.getFullYear();

        var mesTransacao = new Date(transacao.data);

        mesTransacao = (mesTransacao.getMonth() + 1) + '/' + mesTransacao.getFullYear();

        var naoAtende = ($scope.radioVisualizaTransacao === 'pendentes' && transacao.confirmada);

        naoAtende = naoAtende || ($scope.radioVisualizaTransacao === 'confirmadas' && !transacao.confirmada);

        naoAtende = naoAtende || (mesFiltro !== mesTransacao);

        naoAtende = naoAtende || ($scope.contasSelecionadas().indexOf(transacao.conta.id) < 0);

        return !naoAtende;
    };

    $scope.contasSelecionadas = function () {
        var selecionadas = "";

        for (var key in $scope.contas) {
            if ($scope.contas[key].selecionado) {
                if (selecionadas != "") {
                    selecionadas += ",";
                }
                ;
                selecionadas += $scope.contas[key].id;
            }
            ;
        }
        ;

        return selecionadas;
    };

    $scope.selecionouCategoria = function () {

        var categoria = $($scope.categorias).filter(function () {
            return this.id == $scope.transacaoEmEdicao.categoria.id;
        }).first()[0];

        $scope.transacaoEmEdicao.categoria.tipo = categoria.tipo;
    };

    $scope.excluir = function (transacao, index) {
        if (confirm("Deseja excluir esta transação ?")) {
            $http.get('/rest/transacao/apagar?transacao_id=' + transacao.id).success(function (s) {
                $scope.transacoes.splice(index, 1);
            });
        }
    };

    $scope.recalculaSaldo = function (conta_id) {

        data = new Date($scope.mes);
        data = data.toISOString();

        $http.get('/rest/transacao/recalcula_saldo?conta_id=' + conta_id + '&data=' + data).success(function (s) {

        });
    };

    $scope.selecionarTodasContas = function () {

        for (var key in $scope.contas) {
            $scope.contas[key].selecionado = true;
        }
        ;
    };

});
