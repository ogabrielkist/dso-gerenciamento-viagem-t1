from models.viagem import Viagem
from models.exceptions import (
    EntidadeJaExisteException,
    EntidadeNaoEncontradaException,
    ListaVaziaException,
    DadosInvalidosException,
)
from views.tela_viagem import TelaViagem
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_viagem import DAOViagem


class ControladorViagem(ControladorEntidadeBase):
    def __init__(self, controlador_principal, controlador_itinerario, controlador_pessoa):
        super().__init__(controlador_principal)
        self._tela = TelaViagem()
        self._tela.set_controlador_itinerario(controlador_itinerario)
        self._controlador_pessoa = controlador_pessoa
        self._dao = DAOViagem()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes.update(
            {
                5: self.gerenciar_itinerarios,
                6: self.gerenciar_participantes,
                "-ITINERARIOS-": self.gerenciar_itinerarios,
                "-PARTICIPANTES-": self.gerenciar_participantes,
            }
        )

    def _criar_entidade(self, dados):
        for viagem in self._entidades:
            if viagem.data_inicio == dados["data_inicio"]:
                raise EntidadeJaExisteException(
                    "Viagem com essa data de início já cadastrada."
                )

        if dados["data_fim"] <= dados["data_inicio"]:
            raise DadosInvalidosException(
                "Data de fim deve ser posterior à data de início."
            )

        if dados["valor_total_pacote"] < 0:
            raise DadosInvalidosException(
                "Valor total do pacote não pode ser negativo."
            )

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
            raise DadosInvalidosException(
                "Data de fim deve ser posterior à data de início."
            )

        if dados["valor_total_pacote"] < 0:
            raise DadosInvalidosException(
                "Valor total do pacote não pode ser negativo."
            )

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
            if not self._entidades:
                raise ListaVaziaException("Nenhuma viagem cadastrada.")

            dados_lista = [self._entidade_para_dict(e) for e in self._entidades]
            id_viagem = self._tela.seleciona_entidade(
                dados_lista, "Selecionar Viagem para Itinerários"
            )
            if not id_viagem:
                return
            
            viagem_encontrada = self._buscar_entidade(id_viagem) 

            if not viagem_encontrada:
                raise EntidadeNaoEncontradaException("Viagem não encontrada.")

            self._tela.gerenciar_itinerarios(viagem_encontrada)
            
            self._dao.salvar(self._entidades)

        except (EntidadeNaoEncontradaException, ListaVaziaException) as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao gerenciar itinerários: {str(e)}")

    def gerenciar_participantes(self):
        try:
            if not self._entidades:
                raise ListaVaziaException("Nenhuma viagem cadastrada.")

            pessoas = self._controlador_pessoa.get_entidades()
            if not pessoas:
                raise ListaVaziaException(
                    "Cadastre pessoas antes de gerenciar participantes."
                )

            dados_lista = [self._entidade_para_dict(e) for e in self._entidades]
            id_viagem = self._tela.seleciona_entidade(
                dados_lista, "Selecionar Viagem para Participantes"
            )
            if not id_viagem:
                return

            viagem_encontrada = self._buscar_entidade(id_viagem)

            if not viagem_encontrada:
                raise EntidadeNaoEncontradaException("Viagem não encontrada.")

            self._tela.gerenciar_participantes(viagem_encontrada, pessoas)

            self._dao.salvar(self._entidades)

        except (EntidadeNaoEncontradaException, ListaVaziaException) as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao gerenciar participantes: {str(e)}")
