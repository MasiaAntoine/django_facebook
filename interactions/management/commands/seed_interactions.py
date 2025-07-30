from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from interactions.models import Reaction, Commentaire, Partage
from posts.models import Post
from faker import Faker
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeder pour créer des interactions de test (réactions, commentaires, partages)'

    def handle(self, *args, **options):
        fake = Faker('fr_FR')
        # Ne supprime plus les interactions existantes
        self.stdout.write('Aucune suppression des interactions existantes (préservation totale).')
        # Récupérer tous les utilisateurs et posts
        users = list(User.objects.all())
        posts = list(Post.objects.all())
        
        if not users:
            self.stdout.write(
                self.style.ERROR('Aucun utilisateur trouvé. Veuillez d\'abord exécuter le seeder des utilisateurs.')
            )
            return
            
        if not posts:
            self.stdout.write(
                self.style.ERROR('Aucun post trouvé. Veuillez d\'abord exécuter le seeder des posts.')
            )
            return
        
        # Créer des réactions
        self.stdout.write('Création des réactions...')
        reactions = []
        reaction_types = ['like', 'love', 'happy', 'angry', 'sad']
        
        for i in range(100):
            user = random.choice(users)
            post = random.choice(posts)
            reaction_type = random.choice(reaction_types)
            
            # Éviter les doublons (un utilisateur ne peut réagir qu'une fois par post)
            if not Reaction.objects.filter(user=user, post=post).exists():
                reaction = Reaction.objects.create(
                    user=user,
                    post=post,
                    type=reaction_type
                )
                reactions.append(reaction)
        
        # Créer des commentaires
        self.stdout.write('Création des commentaires...')
        commentaires = []
        
        for i in range(80):
            user = random.choice(users)
            post = random.choice(posts)
            
            commentaire = Commentaire.objects.create(
                user=user,
                post=post,
                contenu=fake.text(max_nb_chars=200)
            )
            commentaires.append(commentaire)
        
        # Créer des partages
        self.stdout.write('Création des partages...')
        partages = []
        
        for i in range(40):
            user = random.choice(users)
            post = random.choice(posts)
            
            # Éviter les doublons (un utilisateur ne peut partager qu'une fois par post)
            if not Partage.objects.filter(user=user, post=post).exists():
                partage = Partage.objects.create(
                    user=user,
                    post=post
                )
                partages.append(partage)
                    
        self.stdout.write(
            self.style.SUCCESS(f'Seeder interactions terminé : {len(reactions)} réactions, {len(commentaires)} commentaires, {len(partages)} partages créés')
        )
