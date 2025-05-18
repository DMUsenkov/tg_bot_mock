#!/bin/bash
# Примеры curl-запросов для тестирования Sports Platform Mock API

# Базовый URL для API
BASE_URL="http://localhost:8080/api"

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для выполнения запроса и вывода результата
do_request() {
    echo -e "${BLUE}==== $1 ====${NC}"
    echo "$ $2"
    eval $2
    echo -e "${GREEN}==== Конец запроса ====${NC}\n"
}

# Проверка доступности API
do_request "Проверка доступности API" "curl -s $BASE_URL | jq"

# Получение данных пользователей
do_request "Получение данных пользователя по номеру телефона (Иван Иванов)" "curl -s $BASE_URL/users/by-phone/79001234567 | jq"
do_request "Получение данных пользователя по номеру телефона (Петр Петров)" "curl -s $BASE_URL/users/by-phone/79002345678 | jq"
do_request "Получение данных пользователя по номеру телефона (Алексей Сидоров)" "curl -s $BASE_URL/users/by-phone/79003456789 | jq"
do_request "Получение данных несуществующего пользователя" "curl -s $BASE_URL/users/by-phone/79009999999 | jq"

# Получение команд пользователей
do_request "Получение команд пользователя 1 (Иван Иванов)" "curl -s $BASE_URL/users/1/teams | jq"
do_request "Получение команд пользователя 2 (Петр Петров)" "curl -s $BASE_URL/users/2/teams | jq"
do_request "Получение команд пользователя 3 (Алексей Сидоров)" "curl -s $BASE_URL/users/3/teams | jq"

# Получение чемпионатов пользователей
do_request "Получение чемпионатов пользователя 1 (Иван Иванов)" "curl -s $BASE_URL/users/1/championships | jq"
do_request "Получение чемпионатов пользователя 2 (Петр Петров)" "curl -s $BASE_URL/users/2/championships | jq"
do_request "Получение чемпионатов пользователя 3 (Алексей Сидоров)" "curl -s $BASE_URL/users/3/championships | jq"

# Получение матчей пользователей
do_request "Получение предстоящих матчей пользователя 1" "curl -s \"$BASE_URL/users/1/matches?status=upcoming\" | jq"
do_request "Получение прошедших матчей пользователя 1" "curl -s \"$BASE_URL/users/1/matches?status=past\" | jq"
do_request "Получение всех матчей пользователя 1" "curl -s \"$BASE_URL/users/1/matches?status=all\" | jq"

# Получение деталей команд и чемпионатов
do_request "Получение информации о команде с ID 101" "curl -s $BASE_URL/teams/101 | jq"
do_request "Получение информации о чемпионате с ID 201" "curl -s $BASE_URL/championships/201 | jq"

# Получение предстоящих матчей
do_request "Получение всех предстоящих матчей" "curl -s \"$BASE_URL/matches/upcoming\" | jq"
do_request "Получение предстоящих матчей на 3 дня" "curl -s \"$BASE_URL/matches/upcoming?days=3\" | jq"

# Получение рекомендуемых чемпионатов
do_request "Получение рекомендуемых чемпионатов для пользователя 1" "curl -s $BASE_URL/championships/recommended/1 | jq"
do_request "Получение рекомендуемых чемпионатов для пользователя 2" "curl -s $BASE_URL/championships/recommended/2 | jq"
do_request "Получение рекомендуемых чемпионатов для пользователя 3" "curl -s $BASE_URL/championships/recommended/3 | jq"

# Получение приглашений пользователей
do_request "Получение всех приглашений пользователя 1" "curl -s \"$BASE_URL/users/1/invitations\" | jq"
do_request "Получение приглашений в команду для пользователя 1" "curl -s \"$BASE_URL/users/1/invitations?type=team\" | jq"
do_request "Получение приглашений в оргкомитет для пользователя 1" "curl -s \"$BASE_URL/users/1/invitations?type=committee\" | jq"

# Действия с приглашениями (POST запросы)
do_request "Принятие приглашения в команду" "curl -s -X POST $BASE_URL/invitations/team/401/accept | jq"
do_request "Отклонение приглашения в команду" "curl -s -X POST $BASE_URL/invitations/team/403/decline | jq"
do_request "Принятие приглашения в оргкомитет" "curl -s -X POST $BASE_URL/invitations/committee/402/accept | jq"
do_request "Отклонение приглашения в оргкомитет" "curl -s -X POST $BASE_URL/invitations/committee/402/decline | jq"

# Отклонение участия в матче
do_request "Отклонение участия в матче" "curl -s -X POST -H \"Content-Type: application/json\" -d '{\"team_id\":101,\"reason\":\"Не можем участвовать по уважительной причине\"}' $BASE_URL/matches/301/decline | jq"

# Подтверждение доставки уведомления
do_request "Подтверждение доставки уведомления" "curl -s -X POST -H \"Content-Type: application/json\" -d '{\"notification_id\":501,\"delivered\":true}' $BASE_URL/notifications/confirm-delivery | jq"