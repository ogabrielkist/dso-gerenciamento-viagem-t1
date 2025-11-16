from models.viagem import Viagem
from models.exceptions import (
    EntidadeJaExisteException, 
    EntidadeNaoEncontradaException,
    ListaVaziaException
)
from views.tela_viagem import TelaViagem
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_viagem import DAOViagem


class ControladorViagem(ControladorEntidadeBase):
    def __init__(self, controlador_principal, controlador_itinerario):
        super().__init__(controlador_principal)
        self._tela = TelaViagem()
        self._tela.set_controlador_itinerario(controlador_itinerario)
        self._dao = DAOViagem()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes = {
            1: self.incluir,
            2: self.listar,
            3: self.excluir,
            4: self.editar,
            5: self.gerenciar_itinerarios,
        }

    def _criar_entidade(self, dados):
        for viagem in self._entidades:
            if viagem.data_inicio == dados["data_inicio"]:
                raise EntidadeJaExisteException(
                    "Viagem com essa data de início já cadastrada."
                )

        if dados["data_fim"] <= dados["data_inicio"]:
            raise ValueError("Data de fim deve ser posterior à data de início.")

        if dados["valor_total_pacote"] < 0:
            raise ValueError("Valor total do pacote não pode ser negativo.")

        return Viagem(
            dados["data_inicio"],
            dados["data_fim"],
            dados["valor_total_pacote"],
        )

    def _atualizar_entidade(self, viagem, dados):
        for v in self._entidades:
            if v != viagem and v.data_inicio == dados["data_inicio"]:
                raise EntidadeJaExisteException(
                    "Viagem com essa data de início já cadastrada."
                )

        if dados["data_fim"] <= dados["data_inicio"]:
            raise ValueError("Data de fim deve ser posterior à data de início.")

        if dados["valor_total_pacote"] < 0:
            raise ValueError("Valor total do pacote não pode ser negativo.")

        viagem.data_inicio = dados["data_inicio"]
        viagem.data_fim = dados["data_fim"]
        viagem.valor_total_pacote = dados["valor_total_pacote"]

    def _entidade_para_dict(self, viagem):
        return {
            "id": viagem.id,
            "data_inicio": viagem.data_inicio,
            "data_fim": viagem.data_fim,
            "valor_total_pacote": viagem.valor_total_pacote,
            "participantes": viagem.participantes,
            "destinos_visitados": viagem.destinos_visitados,
        }

    def incluir(self):
        try:
            super().incluir()
        except Exception as e:
            self._tela.mostra_erro(str(e))

    def excluir(self):
        try:
            super().excluir()
        except Exception as e:
            self._tela.mostra_erro(str(e))

    def editar(self):
        try:
            super().editar()
        except Exception as e:
            self._tela.mostra_erro(str(e))

    def gerenciar_itinerarios(self):
        """
        Delega a lógica de gerenciamento de itinerários para a Tela.
        """
        try:
            self.listar()
            if not self._entidades:
                return

            id_viagem = self._tela.seleciona_entidade()
            
            viagem_encontrada = self._buscar_entidade(id_viagem) 

            if not viagem_encontrada:
                raise EntidadeNaoEncontradaException("Viagem não encontrada.")

            self._tela.gerenciar_itinerarios(viagem_encontrada)
            
            self._dao.salvar(self._entidades)

        except (EntidadeNaoEncontradaException, ListaVaziaException) as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao gerenciar itinerários: {str(e)}")
