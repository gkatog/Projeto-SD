#!/bin/bash
# mosquitto local deve estar inicializado
source venv/bin/activate
python ./src/servidorAdministrativo.py $1
