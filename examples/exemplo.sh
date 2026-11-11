#!/usr/bin/env bash
# exemplo.sh — script simples de build/deploy incorporado na documentação.
set -euo pipefail

echo "Construindo a imagem Docker..."
docker build -t teste-mkdocks:latest .

echo "Publicando a imagem no registry..."
docker push teste-mkdocks:latest
