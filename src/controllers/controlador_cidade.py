from models.cidade import Cidade
from models.exceptions import (
    EntidadeJaExisteException,
    EntidadeNaoEncontradaException,
    ListaVaziaException,
)
from views.tela_cidade_gui import TelaCidadeGUI
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_cidade import DAOCidade


class ControladorCidade(ControladorEntidadeBase):
    def __init__(self, controlador_principal, controlador_pais):
        super().__init__(controlador_principal)
        self._controlador_pais = controlador_pais
        self._tela = TelaCidadeGUI("Destinos")
        self._dao = DAOCidade()
        self._entidades = self._dao.carregar()

    def _criar_entidade(self, dados):
        for cidade in self._entidades:
            if (
                cidade.nome.lower() == dados["nome"].lower()
                and cidade.pais.id == dados["pais"].id
            ):
                raise EntidadeJaExisteException(
                    "Cidade com esse nome já cadastrada neste país."
                )

        return Cidade(dados["nome"], dados["pais"])

    def _atualizar_entidade(self, cidade, dados):
        for c in self._entidades:
            if (
                c.id != cidade.id
                and c.nome.lower() == dados["nome"].lower()
                and c.pais.id == dados["pais"].id
            ):
                raise EntidadeJaExisteException(
                    "Cidade com esse nome já cadastrada neste país."
                )

        cidade.nome = dados["nome"]
        cidade.pais = dados["pais"]

    def _entidade_para_dict(self, cidade):
        return {
            "id": cidade.id,
            "nome": cidade.nome,
            "pais": cidade.pais,
        }

    def incluir(self):
        try:
            lista_paises = self._controlador_pais.get_entidades()
            dados = self._tela.pega_dados_entidade(lista_paises)

            if dados:
                entidade = self._criar_entidade(dados)
                self._entidades.append(entidade)
                self._dao.salvar(self._entidades)
                self._tela.mostra_sucesso("Entidade incluída com sucesso!")

        except (EntidadeJaExisteException, ValueError) as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro inesperado ao incluir: {str(e)}")

    def editar(self):
        try:
            if not self._entidades:
                raise ListaVaziaException("Nenhuma cidade cadastrada.")

            dados_lista = [self._entidade_para_dict(e) for e in self._entidades]
            id_selecionado = self._tela.seleciona_entidade(dados_lista, "Editar Cidade")

            if id_selecionado:
                entidade_encontrada = self._buscar_entidade(id_selecionado)
                if not entidade_encontrada:
                    raise EntidadeNaoEncontradaException("Entidade não encontrada.")

                lista_paises = self._controlador_pais.get_entidades()
                dados_atuais = self._entidade_para_dict(entidade_encontrada)
                novos_dados = self._tela.pega_dados_entidade(lista_paises, dados_atuais)

                if novos_dados:
                    self._atualizar_entidade(entidade_encontrada, novos_dados)
                    self._dao.salvar(self._entidades)
                    self._tela.mostra_sucesso("Entidade editada com sucesso!")

        except (ListaVaziaException, EntidadeNaoEncontradaException, ValueError) as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao editar: {str(e)}")
