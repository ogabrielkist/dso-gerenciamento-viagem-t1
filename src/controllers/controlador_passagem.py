import FreeSimpleGUI as sg
from models.passagem import Passagem
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException, ListaVaziaException
from views.tela_passagem_gui import TelaPassagemGUI
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_passagem import DAOPassagem


class ControladorPassagem(ControladorEntidadeBase):
    def __init__(self, controlador_principal, controlador_pessoa, controlador_trecho):
        super().__init__(controlador_principal)
        self._controlador_pessoa = controlador_pessoa
        self._controlador_trecho = controlador_trecho
        self._tela = TelaPassagemGUI()
        self._dao = DAOPassagem()
        self._entidades = self._dao.carregar()

    def _criar_entidade(self, dados):
        for passagem in self._entidades:
            if (
                passagem.passageiro.id == dados["passageiro"].id
                and passagem.trecho.id == dados["trecho"].id
            ):
                raise EntidadeJaExisteException("Passagem para esse passageiro nesse trecho já cadastrada.")

        return Passagem(
            dados["passageiro"],
            dados["trecho"],
            dados["responsavel_compra"],
        )

    def _atualizar_entidade(self, passagem, dados):
        for p in self._entidades:
            if (
                p != passagem
                and p.passageiro.id == dados["passageiro"].id
                and p.trecho.id == dados["trecho"].id
            ):
                raise EntidadeJaExisteException("Passagem para esse passageiro nesse trecho já cadastrada.")

        passagem.passageiro = dados["passageiro"]
        passagem.trecho = dados["trecho"]
        passagem.responsavel_compra = dados["responsavel_compra"]

    def _entidade_para_dict(self, passagem):
        return {
            "id": passagem.id,
            "compra_efetuada": passagem.compra_efetuada,
            "passageiro": passagem.passageiro,
            "trecho": passagem.trecho,
            "responsavel_compra": passagem.responsavel_compra,
        }

    def abre_tela(self):
        while True:
            event = self._tela.le_opcao() 
            
            if event == '-INCLUIR-':
                self.incluir()
            elif event == '-LISTAR-':
                self.listar()
            elif event == '-EDITAR-':
                self.editar()
            elif event == '-EXCLUIR-':
                self.excluir()
            elif event == '-CONFIRMAR_COMPRA-':
                self.confirmar_compra()
            elif event == '-VOLTAR-' or event == sg.WIN_CLOSED:
                break

    def incluir(self):
        try:
            lista_pessoas = self._controlador_pessoa.get_entidades()
            lista_trechos = self._controlador_trecho.get_entidades()
            
            dados = self._tela.pega_dados_entidade(lista_pessoas, lista_trechos) 

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
                raise ListaVaziaException("Nenhuma passagem cadastrada.")

            dados_lista = [self._entidade_para_dict(e) for e in self._entidades] 
            id_selecionado = self._tela.seleciona_entidade(dados_lista, "Editar Passagem")

            if id_selecionado:
                entidade_encontrada = self._buscar_entidade(id_selecionado)
                if not entidade_encontrada:
                    raise EntidadeNaoEncontradaException("Passagem não encontrada.")

                lista_pessoas = self._controlador_pessoa.get_entidades()
                lista_trechos = self._controlador_trecho.get_entidades()
                dados_atuais = self._entidade_para_dict(entidade_encontrada)
                
                novos_dados = self._tela.pega_dados_entidade(lista_pessoas, lista_trechos, dados_atuais)

                if novos_dados:
                    self._atualizar_entidade(entidade_encontrada, novos_dados)
                    self._dao.salvar(self._entidades)
                    self._tela.mostra_sucesso("Entidade editada com sucesso!")

        except (ListaVaziaException, EntidadeNaoEncontradaException, ValueError) as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao editar: {str(e)}")

    def confirmar_compra(self):
        try:
            if not self._entidades:
                raise ListaVaziaException("Nenhuma passagem cadastrada.")
                
            dados_lista = [self._entidade_para_dict(e) for e in self._entidades]
            id_passagem = self._tela.seleciona_entidade(dados_lista, "Confirmar Compra de Passagem")

            if not id_passagem:
                return # Usuário cancelou

            passagem_encontrada = self._buscar_entidade(id_passagem)

            if not passagem_encontrada:
                raise EntidadeNaoEncontradaException("Passagem não encontrada.")

            if passagem_encontrada.compra_efetuada:
                self._tela.mostra_erro("Passagem já foi comprada.")
                return

            passagem_encontrada.compra_efetuada = True
            self._dao.salvar(self._entidades)
            self._tela.mostra_sucesso("Compra da passagem confirmada!")

        except (EntidadeNaoEncontradaException, ListaVaziaException) as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao confirmar compra: {str(e)}")
