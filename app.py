from flask import Flask, jsonify, request
import datetime
import os

app = Flask(__name__)

# Захардкоженные данные для разных API-методов
MOCK_USERS = {
    "79885746845": {
        "id": 1,
        "first_name": "Иван",
        "last_name": "Иванов",
        "phone_number": "79885746845"
    },
    "79002345678": {
        "id": 2,
        "first_name": "Петр",
        "last_name": "Петров",
        "phone_number": "79002345678"
    },
    "79003456789": {
        "id": 3,
        "first_name": "Алексей",
        "last_name": "Сидоров",
        "phone_number": "79003456789"
    }
}

MOCK_TEAMS = {
    1: [
        {
            "id": 101,
            "name": "Команда А",
            "sport": "Футбол",
            "is_captain": True,
            "count_member": 11,
            "members": [
                {"first_name": "Иван", "last_name": "Иванов", "is_captain": True},
                {"first_name": "Алексей", "last_name": "Петров", "is_captain": False},
                {"first_name": "Дмитрий", "last_name": "Смирнов", "is_captain": False}
            ],
            "wins": 5,
            "loss": 2
        },
        {
            "id": 102,
            "name": "Команда Б",
            "sport": "Баскетбол",
            "is_captain": False,
            "count_member": 5,
            "members": [
                {"first_name": "Петр", "last_name": "Соколов", "is_captain": True},
                {"first_name": "Иван", "last_name": "Иванов", "is_captain": False}
            ],
            "wins": 3,
            "loss": 4
        }
    ],
    2: [
        {
            "id": 103,
            "name": "Команда В",
            "sport": "Волейбол",
            "is_captain": True,
            "count_member": 6,
            "members": [
                {"first_name": "Петр", "last_name": "Петров", "is_captain": True},
                {"first_name": "Андрей", "last_name": "Андреев", "is_captain": False}
            ],
            "wins": 7,
            "loss": 1
        }
    ],
    3: [
        {
            "id": 104,
            "name": "Команда Г",
            "sport": "Хоккей",
            "is_captain": False,
            "count_member": 6,
            "members": [
                {"first_name": "Сергей", "last_name": "Сергеев", "is_captain": True},
                {"first_name": "Алексей", "last_name": "Сидоров", "is_captain": False}
            ],
            "wins": 2,
            "loss": 8
        }
    ]
}

MOCK_CHAMPIONSHIPS = {
    1: [
        {
            "id": 201,
            "name": "Городской кубок по футболу",
            "sport": "Футбол",
            "city": "Москва",
            "status": "active",
            "position": "1 место",
            "team_members_count": 11,
            "application_deadline": "2025-06-01",
            "description": "Ежегодный городской кубок по футболу среди любительских команд",
            "org_name": "Городской спорткомитет",
            "is_stopped": False,
            "stages": [
                {"name": "Групповой этап", "is_published": True},
                {"name": "1/4 финала", "is_published": True},
                {"name": "1/2 финала", "is_published": False},
                {"name": "Финал", "is_published": False}
            ]
        },
        {
            "id": 202,
            "name": "Зимний турнир по баскетболу",
            "sport": "Баскетбол",
            "city": "Москва",
            "status": "past",
            "position": "2 место",
            "team_members_count": 5,
            "application_deadline": "2024-12-01",
            "description": "Зимний турнир по баскетболу среди любительских команд",
            "org_name": "Баскетбольная ассоциация",
            "is_stopped": False,
            "stages": [
                {"name": "Групповой этап", "is_published": True},
                {"name": "Плей-офф", "is_published": True}
            ]
        }
    ],
    2: [
        {
            "id": 203,
            "name": "Весенний кубок по волейболу",
            "sport": "Волейбол",
            "city": "Санкт-Петербург",
            "status": "active",
            "position": "3 место",
            "team_members_count": 6,
            "application_deadline": "2025-03-15",
            "description": "Весенний кубок по волейболу среди любительских команд",
            "org_name": "Волейбольный клуб 'Победа'",
            "is_stopped": False,
            "stages": [
                {"name": "Групповой этап", "is_published": True},
                {"name": "Полуфинал", "is_published": False},
                {"name": "Финал", "is_published": False}
            ]
        }
    ],
    3: [
        {
            "id": 204,
            "name": "Хоккейная лига",
            "sport": "Хоккей",
            "city": "Новосибирск",
            "status": "active",
            "position": "4 место",
            "team_members_count": 6,
            "application_deadline": "2025-07-01",
            "description": "Городская хоккейная лига для любительских команд",
            "org_name": "Хоккейная федерация",
            "is_stopped": False,
            "stages": [
                {"name": "Регулярный сезон", "is_published": True},
                {"name": "Плей-офф", "is_published": False}
            ]
        }
    ]
}

MOCK_MATCHES = {
    "upcoming": {
        1: [
            {
                "id": 301,
                "tournament_name": "Городской кубок по футболу",
                "tournament_id": 201,
                "opponent_name": "Команда Звезда",
                "location_name": "Стадион 'Спартак'",
                "address": "ул. Спортивная, 10",
                "date": "2025-05-15",
                "time": "18:00"
            },
            {
                "id": 302,
                "tournament_name": "Зимний турнир по баскетболу",
                "tournament_id": 202,
                "opponent_name": "Команда Метеор",
                "location_name": "Спортзал 'Олимп'",
                "address": "ул. Олимпийская, 5",
                "date": "2025-05-20",
                "time": "19:30"
            }
        ],
        2: [
            {
                "id": 303,
                "tournament_name": "Весенний кубок по волейболу",
                "tournament_id": 203,
                "opponent_name": "Команда Феникс",
                "location_name": "Волейбольный центр",
                "address": "пр. Ленина, 25",
                "date": "2025-05-18",
                "time": "17:00"
            }
        ],
        3: [
            {
                "id": 304,
                "tournament_name": "Хоккейная лига",
                "tournament_id": 204,
                "opponent_name": "Команда Молния",
                "location_name": "Ледовый дворец",
                "address": "ул. Зимняя, 8",
                "date": "2025-05-25",
                "time": "20:00"
            }
        ]
    },
    "past": {
        1: [
            {
                "id": 305,
                "tournament_name": "Городской кубок по футболу",
                "tournament_id": 201,
                "opponent_name": "Команда Буревестник",
                "location_name": "Стадион 'Спартак'",
                "address": "ул. Спортивная, 10",
                "date": "2025-04-10",
                "time": "18:00",
                "result": "2:1",
                "winner": "Команда А"
            }
        ],
        2: [
            {
                "id": 306,
                "tournament_name": "Весенний кубок по волейболу",
                "tournament_id": 203,
                "opponent_name": "Команда Сокол",
                "location_name": "Волейбольный центр",
                "address": "пр. Ленина, 25",
                "date": "2025-04-12",
                "time": "17:00",
                "result": "3:2",
                "winner": "Команда В"
            }
        ]
    }
}

MOCK_INVITATIONS = {
    1: [
        {
            "invitation_id": 401,
            "type": "team",
            "team_name": "Команда Динамо",
            "sport": "Футбол",
            "inviter_name": "Михаил Михайлов"
        },
        {
            "invitation_id": 402,
            "type": "committee",
            "committee_name": "Оргкомитет летнего турнира",
            "inviter_name": "Александр Александров"
        }
    ],
    2: [
        {
            "invitation_id": 403,
            "type": "team",
            "team_name": "Команда Торпедо",
            "sport": "Хоккей",
            "inviter_name": "Сергей Сергеев"
        }
    ],
    3: []
}

MOCK_RECOMMENDED_CHAMPIONSHIPS = {
    1: [
        {
            "tournament_id": 205,
            "name": "Летний кубок по мини-футболу",
            "sport": "Футбол",
            "city": "Москва",
            "team_members_count": 5,
            "application_deadline": "2025-06-15",
            "description": "Летний турнир по мини-футболу для любительских команд"
        },
        {
            "tournament_id": 206,
            "name": "Баскетбольный турнир 3x3",
            "sport": "Баскетбол",
            "city": "Москва",
            "team_members_count": 3,
            "application_deadline": "2025-07-01",
            "description": "Турнир по баскетболу 3x3 среди любительских команд"
        }
    ],
    2: [
        {
            "tournament_id": 207,
            "name": "Осенний турнир по волейболу",
            "sport": "Волейбол",
            "city": "Санкт-Петербург",
            "team_members_count": 6,
            "application_deadline": "2025-09-01",
            "description": "Осенний турнир по волейболу для любительских команд"
        }
    ],
    3: [
        {
            "tournament_id": 208,
            "name": "Зимний кубок по хоккею",
            "sport": "Хоккей",
            "city": "Новосибирск",
            "team_members_count": 6,
            "application_deadline": "2025-11-15",
            "description": "Зимний кубок по хоккею для любительских команд"
        }
    ]
}


# API маршруты

# Получение данных пользователя по номеру телефона
@app.route('/api/users/by-phone/<phone_number>', methods=['GET'])
def get_user_by_phone(phone_number):
    user = MOCK_USERS.get(phone_number)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404


# Получение предстоящих матчей
@app.route('/api/matches/upcoming', methods=['GET'])
def get_upcoming_matches():
    days = request.args.get('days', default=1, type=int)
    # Для простоты возвращаем все предстоящие матчи, независимо от days
    all_matches = []
    for user_matches in MOCK_MATCHES['upcoming'].values():
        all_matches.extend(user_matches)
    return jsonify(all_matches)


# Получение рекомендуемых чемпионатов для пользователя
@app.route('/api/championships/recommended/<int:user_id>', methods=['GET'])
def get_recommended_championships(user_id):
    championships = MOCK_RECOMMENDED_CHAMPIONSHIPS.get(user_id, [])
    return jsonify(championships)


# Подтверждение доставки уведомления
@app.route('/api/notifications/confirm-delivery', methods=['POST'])
def confirm_notification_delivery():
    data = request.json
    return jsonify({"success": True, "notification_id": data.get('notification_id')})


# Получение команд пользователя
@app.route('/api/users/<int:user_id>/teams', methods=['GET'])
def get_user_teams(user_id):
    teams = MOCK_TEAMS.get(user_id, [])
    return jsonify(teams)


# Получение чемпионатов пользователя
@app.route('/api/users/<int:user_id>/championships', methods=['GET'])
def get_user_championships(user_id):
    championships = MOCK_CHAMPIONSHIPS.get(user_id, [])
    return jsonify(championships)


# Получение матчей пользователя
@app.route('/api/users/<int:user_id>/matches', methods=['GET'])
def get_user_matches(user_id):
    status = request.args.get('status', default="upcoming", type=str)
    if status == "upcoming":
        matches = MOCK_MATCHES['upcoming'].get(user_id, [])
    elif status == "past":
        matches = MOCK_MATCHES['past'].get(user_id, [])
    else:  # all
        matches = MOCK_MATCHES['upcoming'].get(user_id, []) + MOCK_MATCHES['past'].get(user_id, [])
    return jsonify(matches)


# Получение детальной информации о команде
@app.route('/api/teams/<int:team_id>', methods=['GET'])
def get_team_details(team_id):
    # Ищем команду по ID во всех пользовательских командах
    for user_teams in MOCK_TEAMS.values():
        for team in user_teams:
            if team['id'] == team_id:
                return jsonify(team)
    return jsonify({"error": "Team not found"}), 404


# Получение детальной информации о чемпионате
@app.route('/api/championships/<int:tournament_id>', methods=['GET'])
def get_championship_details(tournament_id):
    # Ищем чемпионат по ID во всех пользовательских чемпионатах
    for user_championships in MOCK_CHAMPIONSHIPS.values():
        for championship in user_championships:
            if championship['id'] == tournament_id:
                return jsonify(championship)
    return jsonify({"error": "Championship not found"}), 404


# Принятие приглашения в команду
@app.route('/api/invitations/team/<int:invitation_id>/accept', methods=['POST'])
def accept_team_invitation(invitation_id):
    return jsonify({"success": True, "team_name": "Команда Динамо"})


# Отклонение приглашения в команду
@app.route('/api/invitations/team/<int:invitation_id>/decline', methods=['POST'])
def decline_team_invitation(invitation_id):
    return jsonify({"success": True})


# Принятие приглашения в оргкомитет
@app.route('/api/invitations/committee/<int:invitation_id>/accept', methods=['POST'])
def accept_committee_invitation(invitation_id):
    return jsonify({"success": True, "committee_name": "Оргкомитет летнего турнира"})


# Отклонение приглашения в оргкомитет
@app.route('/api/invitations/committee/<int:invitation_id>/decline', methods=['POST'])
def decline_committee_invitation(invitation_id):
    return jsonify({"success": True})


# Получение приглашений пользователя
@app.route('/api/users/<int:user_id>/invitations', methods=['GET'])
def get_user_invitations(user_id):
    invitation_type = request.args.get('type', default="all", type=str)
    invitations = MOCK_INVITATIONS.get(user_id, [])

    if invitation_type != "all":
        invitations = [inv for inv in invitations if inv['type'] == invitation_type]

    return jsonify(invitations)


# Отклонение участия в матче
@app.route('/api/matches/<int:match_id>/decline', methods=['POST'])
def decline_match(match_id):
    data = request.json
    return jsonify({"success": True, "match_id": match_id, "team_id": data.get('team_id')})


# Показываем доступные endpoints при обращении к корню
@app.route('/')
def index():
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append({
                'endpoint': rule.endpoint,
                'methods': [method for method in rule.methods if method not in ['OPTIONS', 'HEAD']],
                'route': str(rule)
            })
    return jsonify({
        'name': 'Mock API для тестирования Telegram-бота',
        'available_routes': routes
    })


if __name__ == '__main__':
    # Используем порт из переменной окружения или 8080 по умолчанию
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)