import random
import time
from pprint import pprint

from django.shortcuts import render, redirect
from django.http import HttpResponse
import redis
from django.conf import settings as django_settings
from django.urls import reverse

from .models import Message, RedisMessage
from django.contrib.auth import authenticate, login

DB_REDIS = django_settings.DB_REDIS

APP_REDIS_PREFIX = "redischat/"


def page_index(request):
    """
    Home page of Redischat app
        - display app descriptif
        - display home page requested count
    """
    return render(request, APP_REDIS_PREFIX + 'index.html', {
        'room_count': get_room_count(),
        'view_count': get_view_count(),
    })


def page_room_list(request):
    """
    TODO : a faire
    TODO : rejoindre ou connexion
    """
    return render(request, APP_REDIS_PREFIX + 'room_list.html', {
        'room_count': get_room_count(),
    })


def page_room_new(request):
    """
    Room creation page ask to user :
        - room name
        - user pseudo
        - pseudo password
        - room color
    """
    return render(request, APP_REDIS_PREFIX + 'room_create.html', {
        'room_count': get_room_count(),
    })


def compute_room_create(request):
    if request.method != 'POST':
        return redirect("redischat:room_list")

    room_name = request.POST.get('room_name')
    room_owner = request.POST.get('room_owner_pseudo')
    room_owner_password = request.POST.get('room_owner_password')
    room_color = request.POST.get('room_color')

    room_id = redis_create_room(room_name, room_owner, room_color)
    if room_id is None:
        # TODO : message flash ?
        return redirect('redischat:room_create')

    user_id = redis_add_user_to_room(room_id, room_owner, room_owner_password)
    if user_id is None:
        # TODO : message flash ?
        return redirect('redischat:room_create')

    return redirect('redischat:room', room_id)


def page_room(request, room_id):
    # Growing spinner
    # TODO :recupéré tout les message d'un chat : évalué le temps de récupération / nombre de requete
    # TODO: user_name passé au template

    # messages = Message.objects.filter(room=room_name)[0:25]
    # messages = [
    #     RedisMessage(room_owner, "message 1", room_name),
    #     RedisMessage(room_owner, "message 2", room_name),
    #     RedisMessage(room_owner, "message 3", room_name)
    # ]
    room_name = redis_get_room_name_by_id(room_id)
    room_owner = redis_get_room_owner_by_id(room_id)
    room_color = redis_get_room_color_by_id(room_id)
    username = request.session['username'] if 'username' in request.session else None

    messages = Message.objects.filter(room=room_name)

    pprint(room_name)
    pprint(room_owner)
    pprint(room_color)

    if request.method == "POST":
        if "isAuth" in request.session:
            if "disconnect" in request.POST:
                request.session.pop("isAuth")

                return redirect("redischat:room", room_id)

        if "connexion" in request.POST:
            username = request.POST.get("conn_username")
            password = request.POST.get("conn_password")
            if username is not None and password is not None:
                conn = redis_conn_user_on_room(room_id, username, password)
                request.session['isAuth'] = room_id if conn else conn
                request.session['username'] = username if username else None

                return redirect("redischat:room", room_id)

        if "register" in request.POST:
            username = request.POST.get("reg_username")
            password = request.POST.get("reg_password")
            if username is not None and password is not None:
                reg = redis_add_user_to_room(room_id, username, password)
                request.session['isAuth'] = room_id if reg else reg
                request.session['username'] = username if username else None

                return redirect("redischat:room", room_id)

    return render(request, APP_REDIS_PREFIX + 'room.html', {
        'room_count': get_room_count(),
        'room_id': room_id,
        'room_name': room_name if room_name else None,
        'room_owner': room_owner if room_owner else None,
        'room_color': room_color if room_color else None,
        'username': username if username else None,
        'messages': messages,
    })


def page_tmp(request):
    # TODO : remove
    return render(request, APP_REDIS_PREFIX + 'tmp.html', {
        'room_count': get_room_count(),
    })


def page_redis(request):
    # TODO : remove
    return HttpResponse(f"Current hits : {get_view_count()}")


# ############
# # Function #
##############


def get_room_count():
    """
    Get number of room created
    """
    try:
        result = DB_REDIS.hlen("rooms")
        return result if result else None
    except redis.exceptions.ConnectionError as e:
        raise e


def get_view_count():
    retries = 5
    while True:
        try:
            return DB_REDIS.incr('view_count')

        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc

            retries -= 1
            time.sleep(0.5)


def redis_get_room_id_by_name(room_name):
    """
    Get room id from rooms tuples corresponding to room_name
    Return room_name id id exist Else None
    """
    try:
        result = DB_REDIS.hget("rooms", room_name)
        return result.decode("utf-8") if result else None
    except redis.exceptions.ConnectionError as e:
        raise e


def redis_get_room_name_by_id(room_id):
    """
    Get room name from rooms tuples corresponding to room_id
    Return room_id if exist Else None
    """
    try:
        result = DB_REDIS.hget(f"room:{room_id}", "name")
        return result.decode("utf-8") if result else None
    except redis.exceptions.ConnectionError as e:
        raise e


def redis_get_room_owner_by_id(room_id):
    """
    Get room owner from rooms tuples corresponding to room_id
    """
    try:
        result = DB_REDIS.hget(f"room:{room_id}", "owner")
        return result.decode("utf-8") if result else None
    except redis.exceptions.ConnectionError as e:
        raise e


def redis_get_room_color_by_id(room_id):
    """
    Get room color from rooms tuples corresponding to room_id
    """
    try:
        result = DB_REDIS.hget(f"room:{room_id}", "color")
        return result.decode("utf-8") if result else None
    except redis.exceptions.ConnectionError as e:
        raise e


def redis_get_room_last_user_id(room_id):
    """
    Get last room user id from rooms tuples corresponding to room_id
    Return last user id if exist Else None
    """
    try:
        result = DB_REDIS.hget(f"room:{room_id}", "last_user_id")
        return result.decode("utf-8") if result else None
    except redis.exceptions.ConnectionError as e:
        raise e


def redis_username_exist_in_room(room_id, username):
    """
    Check if username is free for the room
    Return true if exist Else false
    """
    try:
        result = DB_REDIS.hget(f"room:{room_id}:users", username)
        return True if result else False
    except redis.exceptions.ConnectionError as e:
        raise e


def redis_create_room(room_name, room_owner, room_color):
    """
    TODO = faire une descrpition
    tools
    """
    room_id = redis_get_room_id_by_name(room_name)
    if room_id is not None:
        print("##\n## Error : \n## room name already used\n##")
        return None

    while True:
        room_id = random.randint(0, 99999)
        if DB_REDIS.hget(f"room:{room_id}", 'owner') is None:
            break

    DB_REDIS.hmset(f"room:{room_id}", {
        "name": room_name,
        "owner": room_owner,
        "color": room_color,
        "last_user_id": 1,
    })
    DB_REDIS.hset("rooms", room_name, room_id)

    return room_id


def redis_add_user_to_room(room_id, user_name, user_pwd):
    """
    TODO = faire le com
    """
    user_id = redis_get_room_last_user_id(room_id)
    if redis_username_exist_in_room(room_id, user_name):
        print("##\n## Error : \n## user name already used in room\n##")
        return None

    DB_REDIS.hmset(f"room:{room_id}:user:{user_id}", {
        "password": user_pwd,
    })
    DB_REDIS.hset(f"room:{room_id}:users", user_name, user_id)
    DB_REDIS.hincrby(f"room:{room_id}", "last_user_id", 1)

    return user_id


def redis_conn_user_on_room(room_id, user_name, user_pwd):
    """
    TODO = faire le com
    """
    try:
        user_id = DB_REDIS.hget(f"room:{room_id}:users", user_name)
        user_id = user_id.decode('utf-8')
        print(f"####\n## user_id : '{user_id}'\n####")
        result = DB_REDIS.hget(f"room:{room_id}:user:{user_id}", "password")
        result = result.decode('utf-8')
        print(f"####\n## result : '{result}'\n####")

        return True if user_pwd == result else False
    except redis.exceptions.ConnectionError as e:
        raise e

