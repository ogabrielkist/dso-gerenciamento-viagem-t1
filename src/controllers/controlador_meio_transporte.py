from models.meio_transporte import MeioTransporte, TipoTransporte
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException, ListaVaziaException
from views.tela_meio_transporte_gui import TelaMeioTransporteGUI
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_meio_transporte import DAOMeioTransporte


class ControladorMeioTransporte(ControladorEntidadeBase):
    def __init__(self, controlador_principal, controlador_empresa):
        super().__init__(controlador_principal)
        self._controlador_empresa = controlador_empresa
        self._tela = TelaMeioTransporteGUI()
        self._dao = DAOMeioTransporte()
        self._entidades = self._dao.carregar()

    def _get_tipo_obj_from_str(self, tipo_str: str) -> TipoTransporte:
        for tipo in TipoTransporte:
            if tipo.value == tipo_str:
                return tipo
        raise ValueError(f"Tipo de transporte desconhecido: {tipo_str}")

    def _criar_entidade(self, dados):
        tipo_obj = self._get_tipo_obj_from_str(dados["tipo"])

        for meio in self._entidades:
            if (
                meio.tipo == tipo_obj
                and meio.empresa.cnpj == dados["empresa"].cnpj
            ):
                raise EntidadeJaExisteException("Meio de transporte com esse tipo e empresa já cadastrado.")

        return MeioTransporte(tipo_obj, dados["empresa"])

    def _atualizar_entidade(self, meio_transporte, dados):
        tipo_obj = self._get_tipo_obj_from_str(dados["tipo"])

        for m in self._entidades:
            if (
                m != meio_transporte
                and m.tipo == tipo_obj
                and m.empresa.cnpj == dados["empresa"].cnpj
            ):
                raise EntidadeJaExisteException("Meio de transporte com esse tipo e empresa já cadastrado.")

        meio_transporte.tipo = tipo_obj
        meio_transporte.empresa = dados["empresa"]

    def _entidade_para_dict(self, meio_transporte):
        return {
            "id": meio_transporte.id,
            "tipo": meio_transporte.tipo.value,
            "empresa": meio_transporte.empresa,
        }

    def incluir(self):
        try:
            lista_empresas = self._controlador_empresa.get_entidades()
            dados = self._tela.pega_dados_entidade(lista_empresas) 

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
                raise ListaVaziaException("Nenhum meio de transporte cadastrado.")

            dados_lista = [self._entidade_para_dict(e) for e in self._entidades] 
            id_selecionado = self._tela.seleciona_entidade(dados_lista, "Editar Meio de Transporte")

            if id_selecionado:
                entidade_encontrada = self._buscar_entidade(id_selecionado)
                if not entidade_encontrada:
                    raise EntidadeNaoEncontradaException("Entidade não encontrada.")

                lista_empresas = self._controlador_empresa.get_entidades()
                dados_atuais = self._entidade_para_dict(entidade_encontrada)
                novos_dados = self._tela.pega_dados_entidade(lista_empresas, dados_atuais)

                if novos_dados:
                    self._atualizar_entidade(entidade_encontrada, novos_dados)
                    self._dao.salvar(self._entidades)
                    self._tela.mostra_sucesso("Entidade editada com sucesso!")

        except (ListaVaziaException, EntidadeNaoEncontradaException, ValueError) as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao editar: {str(e)}")
