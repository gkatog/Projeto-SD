import threading
from concurrent import futures
import grpc
import sys
import json

import PortalAdministrativo_pb2
import PortalAdministrativo_pb2_grpc
import pub_sub


class PortalAdministrativoServidor(PortalAdministrativo_pb2_grpc.PortalAdministrativoServicer):
    def __init__(self):
        self.alunos = dict()
        self.professores = dict()
        self.disciplinas = dict()

    def NovoAluno(self, request, context):
        existe = 0
        nome = request.nome
        matricula = request.matricula

        if len(nome) <= 4 or len(matricula) <= 4:
            return PortalAdministrativo_pb2.Status(status=1, msg="Nome ou matricula do aluno é invalido")

        if matricula in self.alunos:
            existe = 2
        else:
            self.alunos[matricula] = nome
            pub_sub.pub_novo_aluno(matricula, nome)

        try:
            return PortalAdministrativo_pb2.Status(status=existe, msg="")
        except grpc.RpcError:
            raise grpc.RpcError

    def EditaAluno(self, request, context):
        nome = request.nome
        matricula = request.matricula

        if len(nome) <= 4 or len(matricula) <= 4:
            return PortalAdministrativo_pb2.Status(status=1, msg="Nome ou matricula do aluno é invalido")

        try:
            if matricula in self.alunos:
                del self.alunos[matricula]
                self.alunos[matricula] = nome

                pub_sub.pub_edita_aluno(matricula, nome)

                return PortalAdministrativo_pb2.Status(status=0, msg="")
            else:
                return PortalAdministrativo_pb2.Status(status=1, msg="Esse aluno não existe")
        except grpc.RpcError:
            raise grpc.RpcError

    def RemoveAluno(self, request, context):
        matricula = request.id

        try:
            if matricula in self.alunos:
                del self.alunos[matricula]
                pub_sub.pub_remove_aluno(matricula)

                return PortalAdministrativo_pb2.Status(status=0, msg="")
            else:
                return PortalAdministrativo_pb2.Status(status=1, msg="Esse aluno não existe")
        except grpc.RpcError:
            raise grpc.RpcError

    def ObtemAluno(self, request, context):
        matricula = request.id

        try:
            if matricula in self.alunos:
                return PortalAdministrativo_pb2.Aluno(
                    matricula=matricula,
                    nome=self.alunos[matricula]
                )
            else:
                return PortalAdministrativo_pb2.Aluno(
                    matricula='',
                    nome=''
                )
        except grpc.RpcError:
            raise grpc.RpcError

    def ObtemTodosAlunos(self, request, context):
        try:
            for chave, valor in self.alunos.items():
                yield PortalAdministrativo_pb2.Aluno(matricula=chave, nome=valor)
        except grpc.RpcError:
            raise grpc.RpcError

    def NovoProfessor(self, request, context):
        siape = request.siape
        nome = request.nome
        existe = 0

        if len(nome) <= 4 or len(siape) <= 4:
            return PortalAdministrativo_pb2.Status(status=1, msg="Nome ou Siape do professor é invalido")

        if siape in self.professores:
            existe = 2
        else:
            self.professores[siape] = nome
            pub_sub.pub_novo_professor(siape, nome)

        try:
            return PortalAdministrativo_pb2.Status(status=existe, msg="")
        except grpc.RpcError:
            raise grpc.RpcError

    def EditaProfessor(self, request, context):
        siape = request.siape
        nome = request.nome

        if len(nome) <= 4 and len(siape) <= 4:
            return PortalAdministrativo_pb2.Status(status=1, msg="Nome ou siape do professor é invalido")

        try:
            if siape in self.professores:
                del self.professores[siape]
                self.professores[siape] = nome

                pub_sub.pub_edita_professor(siape, nome)

                return PortalAdministrativo_pb2.Status(status=0, msg="")
            else:
                return PortalAdministrativo_pb2.Status(status=1, msg="Esse professor não existe")
        except grpc.RpcError:
            raise grpc.RpcError

    def RemoveProfessor(self, request, context):
        siape = request.id

        try:
            if siape in self.professores:
                del self.professores[siape]
                pub_sub.pub_remove_professor(siape)

                return PortalAdministrativo_pb2.Status(status=0, msg="")
            else:
                return PortalAdministrativo_pb2.Status(status=1, msg="Esse professor não existe")
        except grpc.RpcError:
            raise grpc.RpcError

    def ObtemProfessor(self, request, context):
        siape = request.id

        try:
            if siape in self.professores:
                return PortalAdministrativo_pb2.Professor(
                    siape=siape,
                    nome=self.professores[siape]
                )
            else:
                return PortalAdministrativo_pb2.Professor(
                    siape='',
                    nome=''
                )
        except grpc.RpcError:
            raise grpc.RpcError

    def ObtemTodosProfessores(self, request, context):
        try:
            for chave, valor in self.professores.items():
                yield PortalAdministrativo_pb2.Professor(siape=chave, nome=valor)
        except grpc.RpcError:
            raise grpc.RpcError

    def NovaDisciplina(self, request, context):
        existe = 0
        sigla = request.sigla
        nome = request.nome
        vagas = request.vagas

        if len(sigla) <= 4 or len(nome) <= 4 or vagas <= 0:
            return PortalAdministrativo_pb2.Status(status=1, msg="Nome, sigla ou vagas com valor invalido")

        if sigla in self.disciplinas:
            existe = 2
        else:
            self.disciplinas[sigla] = (nome, vagas)
            pub_sub.pub_nova_disciplina(sigla, nome, vagas)

        try:
            return PortalAdministrativo_pb2.Status(status=existe, msg="")
        except grpc.RpcError:
            raise grpc.RpcError

    def EditaDisciplina(self, request, context):
        sigla = request.sigla
        nome = request.nome
        vagas = request.vagas

        if len(sigla) <= 4 or len(nome) <= 4 or vagas <= 0:
            return PortalAdministrativo_pb2.Status(status=1, msg="Nome, sigla ou vagas com valor invalido")

        try:
            if sigla in self.disciplinas:
                del self.disciplinas[sigla]
                self.disciplinas[sigla] = (nome, vagas)

                pub_sub.pub_edita_disciplina(sigla, nome, vagas)

                return PortalAdministrativo_pb2.Status(status=0, msg="")
            else:
                return PortalAdministrativo_pb2.Status(status=1, msg="Essa disciplina não existe")
        except grpc.RpcError:
            raise grpc.RpcError

    def RemoveDisciplina(self, request, context):
        sigla = request.id

        try:
            if sigla in self.disciplinas:
                del self.disciplinas[sigla]

                pub_sub.pub_remove_disciplina(sigla)

                return PortalAdministrativo_pb2.Status(status=0, msg="")
            else:
                return PortalAdministrativo_pb2.Status(status=1, msg="Essa disciplina não existe")
        except grpc.RpcError:
            raise grpc.RpcError

    def ObtemDisciplina(self, request, context):
        sigla = request.id

        try:
            if sigla in self.disciplinas:
                return PortalAdministrativo_pb2.Disciplina(
                    sigla=sigla,
                    nome=self.disciplinas[sigla][0],
                    vagas=self.disciplinas[sigla][1]
                )
            else:
                return PortalAdministrativo_pb2.Disciplina(
                    sigla='',
                    nome='',
                    vagas=-1
                )
        except grpc.RpcError:
            raise grpc.RpcError

    def ObtemTodasDisciplinas(self, request, context):
        try:
            for chave, valor in self.disciplinas.items():
                yield PortalAdministrativo_pb2.Disciplina(
                    sigla=chave,
                    nome=valor[0],
                    vagas=valor[1]
                )
        except grpc.RpcError:
            raise grpc.RpcError


def sincroniza_pub_sub(class_work: PortalAdministrativoServidor) -> None:
    while True:
        fila_msgs = pub_sub.get_queue()

        while not fila_msgs.empty():
            msg = fila_msgs.get()

            try:
                if not msg:
                    continue

                partes = msg.split(',')
                topico = partes[0].strip()

                if topico == pub_sub.MQTT_TOPIC + '/addAluno':
                    payload = partes[1] + "," + partes[2]
                    dados = json.loads(payload)

                    matricula = dados.get("matricula")
                    nome = dados.get("nome")

                    if matricula not in class_work.alunos:
                        class_work.alunos[matricula] = nome
                elif topico == pub_sub.MQTT_TOPIC + '/editaAluno':
                    payload = partes[1] + "," + partes[2]
                    dados = json.loads(payload)

                    matricula = dados.get("matricula")
                    nome = dados.get("nome")

                    if matricula in class_work.alunos:
                        del class_work.alunos[matricula]
                        class_work.alunos[matricula] = nome
                elif topico == pub_sub.MQTT_TOPIC + '/removeAluno':
                    payload = partes[1]
                    dados = json.loads(payload)

                    matricula = dados.get("matricula")

                    if matricula in class_work.alunos:
                        del class_work.alunos[matricula]
                elif topico == pub_sub.MQTT_TOPIC + '/addProfessor':
                    payload = partes[1] + "," + partes[2]
                    dados = json.loads(payload)

                    siape = dados.get("siape")
                    nome = dados.get("nome")

                    if siape not in class_work.professores:
                        class_work.professores[siape] = nome
                elif topico == pub_sub.MQTT_TOPIC + '/editaProfessor':
                    payload = partes[1] + "," + partes[2]
                    dados = json.loads(payload)

                    siape = dados.get("siape")
                    nome = dados.get("nome")

                    if siape in class_work.professores:
                        del class_work.professores[siape]
                        class_work.professores[siape] = nome
                elif topico == pub_sub.MQTT_TOPIC + '/removeProfessor':
                    payload = partes[1]
                    dados = json.loads(payload)

                    siape = dados.get("siape")

                    if siape in class_work.professores:
                        del class_work.professores[siape]
                elif topico == pub_sub.MQTT_TOPIC + '/addDisciplina':
                    payload = partes[1] + "," + partes[2] + "," + partes[3]
                    dados = json.loads(payload)

                    sigla = dados.get("sigla")
                    nome = dados.get("nome")
                    vagas = dados.get("vagas")

                    if sigla not in class_work.disciplinas:
                        class_work.disciplinas[sigla] = (nome, vagas)
                elif topico == pub_sub.MQTT_TOPIC + '/editaDisciplina':
                    payload = partes[1] + "," + partes[2] + "," + partes[3]
                    dados = json.loads(payload)

                    sigla = dados.get("sigla")
                    nome = dados.get("nome")
                    vagas = dados.get("vagas")

                    if sigla in class_work.disciplinas:
                        del class_work.disciplinas[sigla]
                        class_work.disciplinas[sigla] = (nome, vagas)
                elif topico == pub_sub.MQTT_TOPIC + '/removeDisciplina':
                    payload = partes[1]
                    dados = json.loads(payload)

                    sigla = dados.get("sigla")

                    if sigla in class_work.disciplinas:
                        del class_work.disciplinas[sigla]
            except Exception as e:
                print(f'Erro no MQTT: {e}')


def run_server(porta: int) -> None:
    class_work = PortalAdministrativoServidor()

    server = None

    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        PortalAdministrativo_pb2_grpc.add_PortalAdministrativoServicer_to_server(class_work, server)
        server.add_insecure_port(f'localhost:{porta}')
    except grpc.RpcError as e:
        print(f'Error during gRPC startup: {e}')

    server.start()

    print('Server listening on port ' + str(porta) + '...')

    mqttc = pub_sub.mqttClient()

    thread_mqtt = threading.Thread(target=sincroniza_pub_sub, args=(class_work,))
    thread_mqtt.start()

    rc = mqttc.run()
    print(f'rc: {rc}')

    thread_mqtt.join()
    server.wait_for_termination()


if __name__ == '__main__':
    try:
        porta = int(sys.argv[1])
    except Exception:
        porta = 60061

    run_server(porta)
