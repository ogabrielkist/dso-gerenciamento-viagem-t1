from datetime import date
from models.pagamento import Pagamento, PagamentoDinheiro, PagamentoPix, PagamentoCartao
from models.exceptions import (
    CPFInvalidoException,
    DadosInvalidosException,
    EntidadeJaExisteException,
    EntidadeNaoEncontradaException,
    PagamentoForaPrazoException,
)
from models.utils.validadores import normaliza_cpf
from views.tela_pagamento_gui import TelaPagamentoGUI
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_pagamento import DAOPagamento


class ControladorPagamento(ControladorEntidadeBase):
    def __init__(self, controlador_principal, controlador_pessoa, controlador_viagem):
        super().__init__(controlador_principal)
        self._tela = TelaPagamentoGUI()
        self._tela.set_controlador_pessoa(controlador_pessoa)
        self._tela.set_controlador_viagem(controlador_viagem)
        self._dao = DAOPagamento()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes.update(
            {
                1: self.incluir,
                2: self.listar,
                3: self.excluir,
                4: self.editar,
            }
        )

    def _criar_entidade(self, dados):
        if dados["data"] > dados["viagem"].data_inicio:
            raise PagamentoForaPrazoException(
                "Pagamento não pode ser feito após a data de início da viagem."
            )

        if dados["tipo"] == 1:
            return PagamentoDinheiro(
                dados["data"],
                dados["valor_pago"],
                dados["pagador"],
                dados["viagem"],
            )
        elif dados["tipo"] == 2:
            try:
                cpf = normaliza_cpf(dados["cpf_pagador"])
            except ValueError as err:
                raise CPFInvalidoException(str(err))
            return PagamentoPix(
                dados["data"],
                dados["valor_pago"],
                dados["pagador"],
                dados["viagem"],
                cpf,
            )
        elif dados["tipo"] == 3:
            return PagamentoCartao(
                dados["data"],
                dados["valor_pago"],
                dados["pagador"],
                dados["viagem"],
                dados["numero_cartao"],
                dados["bandeira"],
            )
        else:
            raise DadosInvalidosException("Tipo de pagamento inválido.")

    # TODO: Fix
    def _atualizar_entidade(self, pagamento, dados):
        if dados["data"] > dados["viagem"].data_inicio:
            raise PagamentoForaPrazoException(
                "Pagamento não pode ser feito após a data de início da viagem."
            )

        pagamento.data = dados["data"]
        pagamento.valor_pago = dados["valor_pago"]
        pagamento.pagador = dados["pagador"]
        pagamento.viagem = dados["viagem"]

        if isinstance(pagamento, PagamentoPix) and "cpf_pagador" in dados:
            try:
                pagamento.cpf_pagador = normaliza_cpf(dados["cpf_pagador"])
            except ValueError as err:
                raise CPFInvalidoException(str(err))
        elif isinstance(pagamento, PagamentoCartao):
            if "numero_cartao" in dados:
                pagamento.numero_cartao = dados["numero_cartao"]
            if "bandeira" in dados:
                pagamento.bandeira = dados["bandeira"]

    def _entidade_para_dict(self, pagamento):
        dados = {
            "id": pagamento.id,
            "data": pagamento.data,
            "valor_pago": pagamento.valor_pago,
            "pagador": pagamento.pagador,
            "viagem": pagamento.viagem,
            "tipo": pagamento.__class__.__name__,
        }

        if isinstance(pagamento, PagamentoPix):
            dados["cpf_pagador"] = pagamento.cpf_pagador
        elif isinstance(pagamento, PagamentoCartao):
            dados["numero_cartao"] = pagamento.numero_cartao
            dados["bandeira"] = pagamento.bandeira

        return dados

    def incluir(self):
        try:
            super().incluir()
            self._dao.salvar(self._entidades)
        except Exception as e:
            self._tela.mostra_erro(str(e))

    def excluir(self):
        try:
            super().excluir()
            self._dao.salvar(self._entidades)
        except Exception as e:
            self._tela.mostra_erro(str(e))

    def editar(self):
        try:
            super().editar()
            self._dao.salvar(self._entidades)
        except Exception as e:
            self._tela.mostra_erro(str(e))
