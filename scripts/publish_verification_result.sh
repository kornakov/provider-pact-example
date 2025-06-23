#!/usr/bin/env bash
# Публикация результатов проверки  контракта в Pact Broker

set -euo pipefail

# ---- Конфигурация ----
# Переменные берутся из окружения или используют значения по умолчанию
BROKER_URL="${PACT_BROKER_URL:-http://localhost:9292/}"
BROKER_USERNAME="${PACT_BROKER_USERNAME:-username}"
BROKER_PASSWORD="${PACT_BROKER_PASSWORD:-password}"
DOCKER_IMAGE="pactfoundation/pact-cli:latest"


# ---- Публикация ----
echo "🚀 Publishing contracts  from $PACT_DIR to $BROKER_URL"
echo "🔖 Version:  ${GITHUB_SHA}"
echo "🌿 Branch: ${GITHUB_REF_NAME}"

    docker run --rm \
      -v ${PWD}:${PWD} \
      -w ${PWD} \
      -e PACT_BROKER_BASE_URL=${PACT_BROKER_URL} \
      -e PACT_BROKER_USERNAME=${PACT_BROKER_USERNAME} \
      -e PACT_BROKER_PASSWORD=${PACT_BROKER_PASSWORD} \
      pactfoundation/pact-cli:latest \
      broker publish-verification-results \
      --provider YourProviderService \
      --consumer-app-version ${GITHUB_SHA} \
      --verification-success \
      --branch ${GITHUB_REF_NAME} \
      ${PWD}/provider/pacts/verification-results.json

echo "✅ Verification results published successfully"