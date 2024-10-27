from flask import Flask, jsonify,request, make_response
import json
from datetime import datetime
import telebot

token = '7866617284:AAHDOfPQJdKmufOdRgFza6XA8ZWRHPeA_Yc'


# Создаем экземпляр бота
bot = telebot.TeleBot(token)


app = Flask(__name__)


last_id = ""


def get_nicname(user_id):
    with open('./DB/users.json', 'r',encoding='utf-8') as file:
        data = json.load(file)
    #print(f"Data: {data}")
    for userDb in data:
        if userDb['id_user'] == user_id:
            nicname = userDb['name']
            tg_id = userDb['id_tg']
            return nicname, tg_id
    return "",""


def get_nicname_from_tg(id_tg):
    with open('./DB/users.json', 'r',encoding='utf-8') as file:
        data = json.load(file)
    #print(f"Data: {data}")
    for userDb in data:
        if userDb['id_tg'] == id_tg:
            nicname = userDb['name']
            id_user = userDb['id_user']
            return nicname, id_user
    return "",""

@app.route('/get_event', methods=['GET', 'OPTIONS'])
def get_event():
    """
    Метод для получения списка пользователей.
    """
    
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response


    # Чтение JSON-файла
    with open('DB/events.json', 'r',encoding='utf-8') as file:
        data = json.load(file)
    response = make_response(jsonify(data))
    response.headers['Access-Control-Allow-Origin'] = '*'  # Разрешить доступ с любых источников
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'  # Разрешенные методы
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Разрешенные заголовки
    return response

@app.route('/add_event', methods=['POST', 'OPTIONS'])
def add_event():
    """
    Метод для получения списка пользователей.
    """
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    json_data = request.get_json()  # Получение JSON-данных из тела запроса

    with open('./DB/events.json', 'r',encoding='utf-8') as file:
        data = json.load(file)
    # Вывод данных запроса в консоль
    #print("JSON Data:", json_data)
        # "event_id": "1",
        # "event_name": "Игра в PS",
        # "description": "Описание",
        # "created_by": "1",
        # "event_date": "2024-10-30 18:00:00"

    date_obj = datetime.strptime(json_data['event_date'], "%Y-%m-%dT%H:%M")
    formatted_date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")

    data.append({"event_id":"100","event_name":json_data['event_name'],"description":json_data['description'],"created_by":"47","event_date":formatted_date_str})


    with open('./DB/events.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

    response = make_response(jsonify({"status":"ok"}))
    response.headers['Access-Control-Allow-Origin'] = '*'  # Разрешить доступ с любых источников
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'  # Разрешенные методы
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Разрешенные заголовки
    return response

# API для отправки сообщения о регистрации
@app.route('/last_chat_id', methods=['POST','GET','OPTIONS'])
def last_id():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    data = request.json
    #print(f"Data: {data}")

    last_id = data['last_id']
    response = make_response(jsonify({"status":"ok"}))
    response.headers['Access-Control-Allow-Origin'] = '*'  # Разрешить доступ с любых источников
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Разрешенные методы
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Разрешенные заголовки
    return response

# API для отправки сообщения о регистрации
@app.route('/register_event', methods=['POST','GET','OPTIONS'])
def register_event():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    data = request.json


    #print(f"Data reg event: {data}")
    user_id = data["user_id"]
    event_name = data["event_name"]

    if user_id and event_name:
        # Отправляем сообщение в Telegram
        bot.send_message(user_id, f"Вы зарегистрировались на событие: {event_name}")
        response = make_response(jsonify({"status": "success", "message": "Notification sent"}))
        response.headers['Access-Control-Allow-Origin'] = '*'  # Разрешить доступ с любых источников
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Разрешенные методы
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Разрешенные заголовки

        return response
    else:
        return jsonify({"status": "error", "message": "User ID or Event name is missing"}), 400

@app.route('/users_reg', methods=['GET','POST','OPTIONS'])
def users_reg():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response
    #print(request.method)
    json_data = request.get_json() 
    #print(f"JSON: {json_data}")

    with open('./DB/users.json', 'r',encoding='utf-8') as file:
        data = json.load(file)
    #print(f"Data: {data}")

    new_user = {}
    
    id_new_user = len(data) + 1
    for user in data:
        if id_new_user == user['id_user']:
            id_new_user = int(user['id_user'])  * 7 + 1

    
    if 'id' in json_data:
        new_user['id_tg'] = json_data['id']
        new_user['name'] = json_data['name']
    new_user['id_user'] = id_new_user
    new_user['fullname'] = json_data['fullname']
    new_user['photo'] = json_data['photo']
    new_user['interests'] = json_data['interests']
    new_user['about'] = json_data['about']


    data.append(new_user)
    with open('./DB/users.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    
    if 'id' in json_data:
        bot.send_message(json_data['id'], f"Вы зарегистрировались!")


    response = make_response(jsonify({"status":"ok"}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response
    



@app.route('/users', methods=['GET'])
def get_users():
    """
    Метод для получения списка пользователей.
    """
    

    # Чтение JSON-файла
    with open('./DB/users.json', 'r') as file:
        data = json.load(file)
    
    #json_data = request.get_json() 
    #if\
    
    response = make_response(jsonify(data))
    response.headers['Access-Control-Allow-Origin'] = '*'  # Разрешить доступ с любых источников
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'  # Разрешенные методы
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Разрешенные заголовки
    
    return response

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/like', methods=['POST','OPTIONS','GET'])
def likes():
    if request.method == 'OPTIONS':
        # Preflight request; respond with allowed methods and headers
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response

    json_data = request.get_json() 
    #print(f"JSON: {json_data}")

    if "critic_id" in json_data:
        likes_user = json_data['user_id']
        who_like = json_data['critic_id']

        nicname_who, id_user_who = get_nicname_from_tg(who_like)
        nicname, tg_id = get_nicname(likes_user)

        with open('./DB/likes.json', 'r',encoding='utf-8') as file:
            data = json.load(file)
        
        for like in data:
            if like['where_like'] == id_user_who and like['who_like'] == likes_user:
                
                nick2, tg_id2 = get_nicname(like['where_like'])
                print(f"Match: @{nick2} and @{nicname}")
                bot.send_message(tg_id2,f"У вас взаимный интерес с @{nicname}, приятного общения!")
                bot.send_message(tg_id,f"У вас взаимный интерес с @{nick2}, приятного общения!")
                break

        # nicname, tg_id = get_nicname(likes_user)
        # if nicname != "":
        #     print(f"Nickname: {nicname}, Telegram ID: {tg_id}")
            
        #nicname_tg
        data.append({"who_like":id_user_who,"where_like":likes_user})
        with open('./DB/likes.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)

    response = make_response(jsonify({"status":"ok"}))
    response.headers['Access-Control-Allow-Origin'] = '*'  # Разрешить доступ с любых источников
    response.headers['Access-Control-Allow-Methods'] = '*'  # Разрешенные методы
    response.headers['Access-Control-Allow-Headers'] = '*'  # Разрешенные заголовки
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@app.route('/dislike', methods=['POST','OPTIONS','GET'])
def dislikes():
    if request.method == 'OPTIONS':
        # Preflight request; respond with allowed methods and headers
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response
    
    json_data = request.get_json() 
    #print(f"JSON: {json_data}")

    response = make_response(jsonify({"status":"ok"}))
    response.headers['Access-Control-Allow-Origin'] = '*'  # Разрешить доступ с любых источников
    return response


if __name__ == '__main__':
    app.run(debug=True,port = 81,host="0.0.0.0")  # Укажите нужный порт, например, 8080