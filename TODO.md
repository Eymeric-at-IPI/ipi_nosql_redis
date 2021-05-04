# TODOs

## IMPORTANT

- [x] Add readme
- [x] Add todo list
- [ ] begin test
- [ ] begin redis
- [ ] .env on server

## SECONDARY

- [ ] start app skin style
- [ ] make user model ( sqlite3 )
- [ ] List des room exeistante
- [ ] Room privé lié a un user


## THINKING

Account and other model in sqlite3 \
Message in Redis

channels ( async Django view )
channels_redis





Creation d'un chat ( par nom de room, nom unique )
    ajout de label au chat ( liste déroulante avec 3 choix possible par exemple (pour trié))
    affiché le nombre de personne connecté au tchat en temps réel~~~~
Connexion de pseudo au chat ( par nom d'envoyeur, nom unique )

Liste des room disponible pour les rejoindres ( besoin d'un liste avec les nom )
    trié les salle par nom ( alpha ) ou par type ( label / tag )

Possibilité de férmé un salon ?
    salon perisable ( suprimé en cas d'incativité prolongé ( suprimé tout les message assosié))

Stylisé le tout

-> page d'acceuil qui liste les chats
-> page de creation d'un tchat
-> page de tchat
