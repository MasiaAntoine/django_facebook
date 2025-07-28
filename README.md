# Projet Django-facebook

## Introduction

Le but de ce projet est de faire un facebook-Like en django.
Pour ce faire, on utilisera en technologie :

| Technologies | Utilisations                                                           |
| ------------ | ---------------------------------------------------------------------- |
| Docker       | Initialisation du projet, creation d'un super user, et de la base de done |
| Django       | Partie back et front du projet                                         |
| Bootstrap    | style du projet                                                        |

## Initiation du projet

Avant toutes choses, il faut bien penser à creer un **.env** contenant les different credentials de notre application.

Une fois ce .env modifier, on peux passer a la deuxieme etape qui est le docker.

## Docker

On a donc fait un docker pour une initialisation du projet plus simple, rapide et opérationnelle sur tous les OS.

Pour lancer le projet docker, il suffit de lancer la commande suivante pour construire et démarrer le container :

```bash
docker compose up --build -d
```

Ou bien une fois qu'ils sont construits :

```bash
docker compose up
```

Pour vérifier que docker s'est bien lancé, vous devez voir apparaître 2 containers.
Utilisez la commande suivante pour vérifier que les deux containers sont bien lancés :

```bash
docker ps
```

Le résultat attendu :

```bash
docker ps
CONTAINER ID   IMAGE                        COMMAND                  CREATED         STATUS         PORTS                                         NAMES
515a93abfc3c   django_facebook-django-web   "./entrypoint.sh"        4 minutes ago   Up 4 minutes   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   django-docker
197bfd50104e   postgres:latest              "docker-entrypoint.s…"   4 minutes ago   Up 4 minutes   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   postgres_django
```

Si vous avez besoin de relancer le docker avec des changements d'architecture ou de Dockerfile|docker-compose, utilisez :

```bash
docker compose down -v
```

Sinon, un simple redémarrage suffit :

```bash
docker compose restart
```

## Application

Les deux urls de l'application sont :

- localhost:5432 pour la base de donnee,
- localhost:8000 pour l'application django en elle meme.

## Applications créées pour une meilleure segmentation

Pour avoir une meilleure segmentation du code, on peut créer plusieurs apps qui permettent d'avoir un code mieux décomposé.

Commande de création d'une app :

```bash
python manage.py startapp nom_de_l_app
```

### Applications créées :

- **utilisateurs** : _Gestion des utilisateurs : profil, inscription, suppression, RGPD_
- **amis** : _Demandes, blocages, amis en commun_
- **posts** : _Création de posts, stories, catégories_
- **interactions** : _Likes (réactions), commentaires, partages_
- **notifications** : _Logique de notifications utilisateurs_

### URLs configurées :

Toutes les applications sont connectées via l'app `facebook` avec les routes suivantes :

- `/utilisateurs/` - Gestion des utilisateurs
- `/amis/` - Gestion des amis
- `/posts/` - Gestion des posts
- `/interactions/` - Gestion des interactions
- `/notifications/` - Gestion des notifications

### Commandes utiles Django :

Créer les migrations :

```bash
python manage.py makemigrations
```

Appliquer les migrations :

```bash
python manage.py migrate
```

Lancer le serveur de développement :

```bash
python manage.py runserver
```

Créer un superutilisateur :

```bash
python manage.py createsuperuser
```
