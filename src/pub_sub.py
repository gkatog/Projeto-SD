import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import json
from queue import Queue

MQTT_HOST = "127.0.0.1"
MQTT_TOPIC = "projeto-sd"
MQTT_QOS = 2
msg_q = Queue()


# mosquitto_sub -h 127.0.0.1 -t projeto-sd

class mqttClient(mqtt.Client):
    def __init__(self):
        super().__init__(mqtt.CallbackAPIVersion.VERSION2)

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")

    def on_connect_fail(self, mqttc, obj):
        print("Connect failed")

    def on_message(self, mqttc, obj, msg):
        print("topic:" + msg.topic + "," + "qos:" + str(msg.qos) + ",payload:" + str(msg.payload))
        msg_q.put(str(msg.topic) + ',' + str(msg.payload.decode("utf-8")))

    def on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))

    def on_subscribe(self, client, userdata, mid, reason_code_list, properties):
        if reason_code_list[0].is_failure:
            print(f"Broker rejected you subscription: {reason_code_list[0]}")
        else:
            print(f"Broker granted the following QoS: {reason_code_list[0].value}")

    def on_log(self, mqttc, obj, level, string):
        ...

    def run(self):
        self.connect(MQTT_HOST, 1883, 60)
        self.subscribe(MQTT_TOPIC + str('/+'), MQTT_QOS)

        rc = 0
        while rc == 0:
            rc = self.loop()

        return rc

    def sub(self):
        self.subscribe(topic=MQTT_TOPIC, qos=MQTT_QOS)


def pub_novo_aluno(matricula: str, nome: str) -> None:
    dados = {
        "matricula": matricula,
        "nome": nome
    }

    try:
        publish.single(topic=MQTT_TOPIC + '/addAluno',
                       payload=json.dumps(dados),
                       qos=MQTT_QOS)
    except Exception as e:
        raise Exception(e)


def pub_edita_aluno(matricula: str, nome: str) -> None:
    dados = {
        "matricula": matricula,
        "nome": nome
    }

    try:
        publish.single(topic=MQTT_TOPIC + '/editaAluno',
                       payload=json.dumps(dados),
                       qos=MQTT_QOS)
    except Exception as e:
        raise Exception(e)


def pub_remove_aluno(matricula: str) -> None:
    dados = {"matricula": matricula}

    try:
        publish.single(topic=MQTT_TOPIC + '/removeAluno',
                       payload=json.dumps(dados),
                       qos=MQTT_QOS)
    except Exception as e:
        raise Exception(e)


def pub_novo_professor(siape: str, nome: str) -> None:
    dados = {
        "siape": siape,
        "nome": nome
    }

    try:
        publish.single(topic=MQTT_TOPIC + '/addProfessor',
                       payload=json.dumps(dados),
                       qos=MQTT_QOS)
    except Exception as e:
        raise Exception(e)


def pub_edita_professor(siape: str, nome: str) -> None:
    dados = {
        "siape": siape,
        "nome": nome
    }

    try:
        publish.single(topic=MQTT_TOPIC + '/editaProfessor',
                       payload=json.dumps(dados),
                       qos=MQTT_QOS)
    except Exception as e:
        raise Exception(e)


def pub_remove_professor(siape: str) -> None:
    dados = {"siape": siape}

    try:
        publish.single(topic=MQTT_TOPIC + '/removeProfessor',
                       payload=json.dumps(dados),
                       qos=MQTT_QOS)
    except Exception as e:
        raise Exception(e)


def pub_nova_disciplina(sigla: str, nome: str, vagas: int) -> None:
    dados = {
        "sigla": sigla,
        "nome": nome,
        "vagas": vagas
    }

    try:
        publish.single(topic=MQTT_TOPIC + '/addDisciplina',
                       payload=json.dumps(dados),
                       qos=MQTT_QOS)
    except Exception as e:
        raise Exception(e)


def pub_edita_disciplina(sigla: str, nome: str, vagas: int) -> None:
    dados = {
        "sigla": sigla,
        "nome": nome,
        "vagas": vagas
    }

    try:
        publish.single(topic=MQTT_TOPIC + '/editaDisciplina',
                       payload=json.dumps(dados),
                       qos=MQTT_QOS)
    except Exception as e:
        raise Exception(e)


def pub_remove_disciplina(sigla: str) -> None:
    dados = {"sigla": sigla}

    try:
        publish.single(topic=MQTT_TOPIC + '/removeDisciplina',
                       payload=json.dumps(dados),
                       qos=MQTT_QOS)
    except Exception as e:
        raise Exception(e)


def get_queue():
    return msg_q


def empty_queue():
    with msg_q.mutex:
        msg_q.queue.clear()
