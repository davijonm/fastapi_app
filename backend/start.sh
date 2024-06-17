#!/bin/bash

# Aguardar 3 segundos para o banco de dados inicializar
sleep 3

# Executar o servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000
