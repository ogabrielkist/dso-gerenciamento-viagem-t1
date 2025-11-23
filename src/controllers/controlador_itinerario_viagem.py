from datetime import date
from models.itinerario_viagem import ItinerarioViagem
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException
from views.tela_itinerario_viagem import TelaItinerarioViagem
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_itinerario_viagem import DAOItinerarioViagem


class ControladorItinerarioViagem(ControladorEntidadeBase):
    def __init__(self, controlador_principal, controlador_passeio):
        super().__init__(controlador_principal)
        self._tela = TelaItinerarioViagem()
        self._tela.set_controlador_passeio(controlador_passeio)
        self._dao = DAOItinerarioViagem()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes.update(
            {
                5: self.gerenciar_passeios,
                "-PASSEIOS-": self.gerenciar_passeios,
            }
        )

    def _criar_entidade(self, dados):
        for itinerario in self._entidades:
            if itinerario.data == dados["data"]:
                raise EntidadeJaExisteException(
                    "Itinerário para essa data já cadastrado."
                )

        return ItinerarioViagem(dados["data"])

    def _atualizar_entidade(self, itinerario, dados):
        for i in self._entidades:
            if i != itinerario and i.data == dados["data"]:
                raise EntidadeJaExisteException(
                    "Itinerário para essa data já cadastrado."
                )

        itinerario.data = dados["data"]

    def _entidade_para_dict(self, itinerario):
        return {
            "id": itinerario.id,
            "data": itinerario.data,
            "passeios": itinerario.passeios,
        }

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

    def gerenciar_passeios(self):
        try:
            self.listar()
            if not self._entidades:
                return

            dados_lista = [self._entidade_para_dict(e) for e in self._entidades]
            id_itinerario = self._tela.seleciona_entidade(
                dados_lista, "Selecionar Itinerário"
            )
            if not id_itinerario:
                return
            itinerario_encontrado = None
            for itinerario in self._entidades:
                if itinerario.id == id_itinerario:
                    itinerario_encontrado = itinerario
                    break

            if not itinerario_encontrado:
                raise EntidadeNaoEncontradaException("Itinerário não encontrado.")

            self._tela.gerenciar_passeios(itinerario_encontrado)
            self._dao.salvar(self._entidades)

        except EntidadeNaoEncontradaException as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(str(e))
