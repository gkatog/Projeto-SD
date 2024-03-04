from concurrent import futures
import grpc
import threading
import json
import sys

import PortalDeMatricula_pb2_grpc
import PortalDeMatricula_pb2
import pub_sub


class PortalMatriculaServidor(PortalDeMatricula_pb2_grpc.PortalMatriculaServicer):
    def __init__(self):
        self.professores = dict()
        self.alunos = dict()
        self.disciplinas = dict()
        self.turmas = dict()

    def AdicionaProfessor(self, request, context):
        sigla_disciplina = request.disciplina
        siape_professor = request.idPessoa

        try:
            if sigla_disciplina in self.disciplinas and siape_professor in self.professores:
                if sigla_disciplina in self.turmas:
                    if self.turmas[sigla_disciplina]["professor"] is not None:
                        return PortalDeMatricula_pb2.Status(status=1, msg="Essa disciplina já professor cadastrado")
                    else:
                        self.turmas[sigla_disciplina]["professor"] = siape_professor
                        return PortalDeMatricula_pb2.Status(status=0, msg="")
                else:
                    self.turmas[sigla_disciplina] = {
                        "professor": siape_professor,
                        "alunos": [],
                        "vagas_usadas": 0
                    }
                    return PortalDeMatricula_pb2.Status(status=0, msg="")
            else:
                return PortalDeMatricula_pb2.Status(status=1, msg="Disciplina ou professor não existe")
        except grpc.RpcError:
            raise grpc.RpcError

    def RemoveProfessor(self, request, context):
        sigla_disciplina = request.disciplina
        siape_professor = request.idPessoa

        try:
            if sigla_disciplina in self.disciplinas and siape_professor in self.professores:
                if sigla_disciplina in self.turmas and "professor" in self.turmas[sigla_disciplina]:
                    if siape_professor == self.turmas[sigla_disciplina]["professor"]:
                        self.turmas[sigla_disciplina]["professor"] = None

                        return PortalDeMatricula_pb2.Status(status=0, msg="")
                    else:
                        return PortalDeMatricula_pb2.Status(status=1, msg="Professor não está vinculado a disciplina")
                else:
                    return PortalDeMatricula_pb2.Status(status=1, msg="Não há professores vinculados a está disciplina")
            else:
                return PortalDeMatricula_pb2.Status(status=1, msg="Disciplina ou professor não existe")
        except grpc.RpcError:
            raise grpc.RpcError

    def AdicionaAluno(self, request, context):
        sigla_disciplina = request.disciplina
        matricula_aluno = request.idPessoa

        if sigla_disciplina in self.disciplinas and matricula_aluno in self.alunos:
            if sigla_disciplina in self.turmas:
                if self.turmas[sigla_disciplina]["vagas_usadas"] < self.disciplinas[sigla_disciplina][1]:
                    if matricula_aluno not in self.turmas[sigla_disciplina]["alunos"]:
                        self.turmas[sigla_disciplina]["alunos"].append(matricula_aluno)
                        self.turmas[sigla_disciplina]["vagas_usadas"] += 1

                        return PortalDeMatricula_pb2.Status(status=0, msg="")
                    else:
                        return PortalDeMatricula_pb2.Status(status=1, msg="Aluno já cadastrado")
                else:
                    return PortalDeMatricula_pb2.Status(status=1, msg="Limite de vagas excedido")
            else:
                self.turmas[sigla_disciplina] = {
                    "professor": None,
                    "alunos": [matricula_aluno],
                    "vagas_usadas": 1
                }

                return PortalDeMatricula_pb2.Status(status=0, msg="")
        else:
            return PortalDeMatricula_pb2.Status(status=1, msg="Disciplina ou aluno não existe")

    def RemoveAluno(self, request, context):
        sigla_disciplina = request.disciplina
        matricula_aluno = request.idPessoa

        try:
            if sigla_disciplina in self.disciplinas and matricula_aluno in self.alunos:
                turma = self.turmas.get(sigla_disciplina)

                if turma and "alunos" in self.turmas[sigla_disciplina]:
                    if "alunos" in self.turmas[sigla_disciplina]:
                        if matricula_aluno in self.turmas[sigla_disciplina]["alunos"]:
                            self.turmas[sigla_disciplina]["alunos"].remove(matricula_aluno)
                            self.turmas[sigla_disciplina]["vagas_usadas"] -= 1

                            return PortalDeMatricula_pb2.Status(status=0, msg="")
                        else:
                            return PortalDeMatricula_pb2.Status(status=1,
                                                                msg="Esse aluno não está matriculado nessa disciplina")
                    else:
                        return PortalDeMatricula_pb2.Status(status=1, msg="Matricule algum aluno primeiro")
                else:
                    return PortalDeMatricula_pb2.Status(status=1, msg="Não há alunos vinculados a está disciplina ou a "
                                                                      "turma não existe")
            else:
                return PortalDeMatricula_pb2.Status(status=1, msg="Disciplina ou aluno não existe")
        except grpc.RpcError:
            raise grpc.RpcError

    def DetalhaDisciplina(self, request, context):
        sigla_disciplina = request.id

        try:
            if sigla_disciplina in self.disciplinas and sigla_disciplina in self.turmas:
                disciplina_info = PortalDeMatricula_pb2.Disciplina(
                    sigla=sigla_disciplina,
                    nome=self.disciplinas[sigla_disciplina][0],
                    vagas=self.disciplinas[sigla_disciplina][1]
                )

                if "professor" in self.turmas[sigla_disciplina] and (self.turmas[sigla_disciplina]
                                                                     ["professor"] is not None):
                    siape_professor = self.turmas[sigla_disciplina]["professor"]
                    nome_professor = self.professores[siape_professor]

                    professor_info = PortalDeMatricula_pb2.Professor(
                        siape=siape_professor,
                        nome=nome_professor
                    )
                else:
                    professor_info = PortalDeMatricula_pb2.Professor(
                        siape='',
                        nome=''
                    )

                alunos_info = []

                if "alunos" in self.turmas[sigla_disciplina]:
                    for matricula in self.turmas[sigla_disciplina]["alunos"]:
                        alunos_info.append(
                            PortalDeMatricula_pb2.Aluno(
                                matricula=matricula,
                                nome=self.alunos[matricula]
                            )
                        )
                else:
                    alunos_info.append(
                        PortalDeMatricula_pb2.Aluno(
                            matricula='',
                            nome=''
                        )
                    )

                return PortalDeMatricula_pb2.RelatorioDisciplina(
                    disciplina=disciplina_info,
                    professor=professor_info,
                    alunos=alunos_info
                )
            else:
                return PortalDeMatricula_pb2.RelatorioDisciplina()
        except grpc.RpcError:
            raise grpc.RpcError

    def ObtemDisciplinasProfessor(self, request, context):
        siape_professor = request.id

        try:
            if siape_professor in self.professores:
                professor_info = PortalDeMatricula_pb2.Professor(
                    siape=siape_professor,
                    nome=self.professores[siape_professor]
                )

                for turma_id, dados_turma in self.turmas.items():
                    if dados_turma["professor"] == siape_professor:
                        disciplina_info = PortalDeMatricula_pb2.Disciplina(
                            sigla=turma_id,
                            nome=self.disciplinas[turma_id][0],
                            vagas=self.disciplinas[turma_id][1]
                        )

                        alunos_final = []

                        for aluno in dados_turma["alunos"]:
                            alunos_final.append(
                                PortalDeMatricula_pb2.Aluno(
                                    matricula=aluno,
                                    nome=self.alunos[aluno]
                                )
                            )

                        yield PortalDeMatricula_pb2.RelatorioDisciplina(
                            disciplina=disciplina_info,
                            professor=professor_info,
                            alunos=alunos_final
                        )
            else:
                return PortalDeMatricula_pb2.RelatorioDisciplina()
        except grpc.RpcError:
            raise grpc.RpcError

    def ObtemDisciplinasAluno(self, request, context):
        matricula_aluno = request.id

        sigla_turma_associado = []
        nome_turma_associado = []
        vagas_usadas_asssociado = []
        vagas_totais_associado = []
        professor_associado = []

        try:
            if matricula_aluno in self.alunos:
                for turma_id, dados_turma in self.turmas.items():
                    if matricula_aluno in dados_turma["alunos"]:
                        sigla_turma_associado.append(turma_id)
                        nome_turma_associado.append(self.disciplinas[turma_id][0])
                        vagas_totais_associado.append(self.disciplinas[turma_id][1])
                        vagas_usadas_asssociado.append(dados_turma["vagas_usadas"])

                        siape_professor_disc = dados_turma["professor"]

                        if siape_professor_disc is None:
                            professor_associado.append(
                                ('', '')
                            )
                        else:
                            professor_associado.append(
                                (siape_professor_disc, self.professores[siape_professor_disc])
                            )

                for sigla_dics, nome_dics, vagas_usadas, vagas_totais, professor in (
                        zip(sigla_turma_associado, nome_turma_associado, vagas_usadas_asssociado,
                            vagas_totais_associado, professor_associado)):
                    disciplina_info = PortalDeMatricula_pb2.Disciplina(
                        sigla=sigla_dics,
                        nome=nome_dics,
                        vagas=vagas_totais
                    )

                    professor_info = PortalDeMatricula_pb2.Professor(
                        siape=professor[0],
                        nome=professor[1]
                    )

                    yield PortalDeMatricula_pb2.ResumoDisciplina(
                        disciplina=disciplina_info,
                        professor=professor_info,
                        totalAlunos=vagas_usadas
                    )
            else:
                return PortalDeMatricula_pb2.ResumoDisciplina()
        except grpc.RpcError:
            raise grpc.RpcError


def sincroniza_pub_sub(class_work: PortalMatriculaServidor) -> None:
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
    class_work = PortalMatriculaServidor()

    server = None

    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        PortalDeMatricula_pb2_grpc.add_PortalMatriculaServicer_to_server(class_work, server)
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
        porta = 50051

    run_server(porta)
