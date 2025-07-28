# Projet Django-facebook

## Introduction
Le but de ce projet est de faire un facebook-Like en django.
Pour ce faire, on utilisera en technologie :
<table>
    <thead style="background-color: #313030; text-align: center">
        <td>technologies</td>
        <td>utilisations</td>
    </thead>
    <tbody style="background-color: black">
        <tr>
            <td>Docker</td>
            <td>Initialisation du projet, creation d'un super user, et de la base de done</td>
        </tr>
        <tr>
            <td>Django</td>
            <td>Partie back et front du projet/td>
        </tr>
        <tr>
            <td>Bootstrap</td>
            <td>style du projet </td>
        </tr>
    </tbody>
</table>

## inititation du projet
Avant toutes choses, il faut bien penser à creer un **.env** contenant les different credentials de notre application.
</br>
Une fois ce .env modifier, on peux passer a la deuxieme etape qui est le docker.

## Docker
On a donc fait un docker pour une initialisation du projet plus simple rapide et operationnel sur tous les OS.
Pour lancer le projet docker, il suffit de lancer la commande `docker compose up --build -d` pour lancer le container
en le reconstruisant ou bien une fois qu'ils sont construits  `docker compose up`. </br>
Pour verifier que le docker c'est bien lancer, dans les jobs on doit voir apparaitres 5 jobs differents au build : 
il suffit de faire la commande `docker ps` et de verifier que les deux containeurs sont bien lancer : 
```aiignore
docker ps                                      
CONTAINER ID   IMAGE                        COMMAND                  CREATED         STATUS         PORTS                                         NAMES
515a93abfc3c   django_facebook-django-web   "./entrypoint.sh"        4 minutes ago   Up 4 minutes   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   django-docker
197bfd50104e   postgres:latest              "docker-entrypoint.s…"   4 minutes ago   Up 4 minutes   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   postgres_django
```
Si il y a besoind de relancer le docker avec changements d'architecture ou de Dockerfile|docker-compose : il faut faire
la commande `docker compose down -v` sinon un `docker compose restart` suffit


## application
Les deux urls de l'application sont :
- localhost:5432 pour la base de donnee,
- localhost:8000 pour l'application django en elle meme.

## Architecture du projet
```aiignore
Django-facebook/
├── core/
│ └── management/
│   ├── __init__.py
│   └── commands/
│     ├── create_superuser_if_none_exists.py
│     └── __init__.py
├── django_facebook/
│ ├── __init__.py
│ ├── sagi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── facebook/
│ ├── __init__.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── tests.py
│ └── urls.py
│ └── views.py
│ └── migrations/
│   └── __init__.py
│ ├── templates/
│   └── facebook
│     ├── home.html
├── staticfiles/
│   └── facebook/
│     └── images/
│       └── 64x64.png
│       └── 256x112.png
│       └── 960x960.png
│       └── 1024x446.png
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── manage.py
├── README.md
└── requirements.txt
```

## Creer des applications pour une meilleure segmentation 
Pour avoir une meilleure segmentation du code, on peut creer plusieurs apps qui vont 
permettre d'avoir un code mieux decomposer : `python manage.py startapp`
idee d'app a demarrer : 
- users : *Gestion des utilisateurs : profil, inscription, suppression, RGPD*
- friends : *Demandes, blocages, amis en commun*
- posts : *Création de posts, stories, catégories*
- interactions : *Likes (réactions), commentaires, partages*
- notifications : *Logique de notifications utilisateurs*

