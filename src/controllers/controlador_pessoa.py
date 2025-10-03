from models import Pessoa
from views import TelaPessoa


class ControladorPessoa:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__tela_pessoa = TelaPessoa()
        self.__participantes = []

    def incluir_pessoa(self):
        dados_pessoa = self.__tela_pessoa.pega_dados_pessoa()
        
        for participante in self.__participantes:
            if participante.identificacao() == dados_pessoa["identificacao"]:
                self.__tela_pessoa.mostra_mensagem("ERRO: Pessoa com essa identificação já cadastrada.")
                return

        pessoa = Pessoa(dados_pessoa["nome"], dados_pessoa["celular"], dados_pessoa["identificacao"], dados_pessoa["idade"])
    
        self.__participantes.append(pessoa)
        self.__tela_pessoa.mostra_mensagem("Pessoa incluída com sucesso!")

    def listar_pessoas(self):
        if not self.__participantes:
            self.__tela_pessoa.mostra_mensagem("Nenhuma pessoa cadastrada.")
            return
        
        print(f'PARTICIPANTES ----> {self.__participantes}')
        for pessoa in self.__participantes:
            print(f'PESSOA ----> {pessoa}')
            dados_pessoa = {
                "nome": pessoa.nome,
                "celular": pessoa.celular,
                "identificacao": pessoa.identificacao,
                "idade": pessoa.idade,
            }
    
            self.__tela_pessoa.mostra_pessoa(dados_pessoa)
            
    def excluir_pessoa(self):
        self.listar_pessoas()
        if not self.__participantes:
            return

        identificacao = self.__tela_pessoa.seleciona_pessoa()
        
        pessoa_encontrada = None
        for pessoa in self.__participantes:
            if pessoa.identificacao == identificacao:
                pessoa_encontrada = pessoa
                break
        
        if pessoa_encontrada:
            self.__participantes.remove(pessoa_encontrada)
            self.__tela_pessoa.mostra_mensagem("Pessoa removida com sucesso!")
        else:
            self.__tela_pessoa.mostra_mensagem("ERRO: Pessoa não encontrada.")

    def retornar(self):
        self.__controlador_principal.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            1: self.incluir_pessoa,
            2: self.listar_pessoas,
            3: self.excluir_pessoa,
            0: self.retornar
        }

        while True:
            opcao_escolhida = self.__tela_pessoa.tela_opcoes()

            funcao_escolhida = lista_opcoes.get(opcao_escolhida)
            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__tela_pessoa.mostra_mensagem("Opção inválida!")
