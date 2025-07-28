from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Category, Post
from faker import Faker
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeder pour créer des catégories et posts de test'

    def handle(self, *args, **options):
        fake = Faker('fr_FR')
        
        # Reset: supprimer toutes les catégories et posts existants
        self.stdout.write('Suppression des posts et catégories existants...')
        Post.objects.all().delete()
        Category.objects.all().delete()
        
        # Créer 5 catégories
        self.stdout.write('Création des catégories...')
        categories = []
        category_names = ['Technologie', 'Voyage', 'Cuisine', 'Sport', 'Musique']
        
        for name in category_names:
            category = Category.objects.create(
                title=name,
                description=fake.text(max_nb_chars=200)
            )
            categories.append(category)
        
        # Récupérer tous les utilisateurs
        users = list(User.objects.all())
        
        if not users:
            self.stdout.write(
                self.style.ERROR('Aucun utilisateur trouvé. Veuillez d\'abord exécuter le seeder des utilisateurs.')
            )
            return
        
        # Créer 50 posts
        self.stdout.write('Création des posts...')
        posts = []
        
        for i in range(50):
            user = random.choice(users)
            category = random.choice(categories) if random.choice([True, False]) else None
            is_story = random.choice([True, False])
            
            post = Post.objects.create(
                user=user,
                title=fake.sentence(nb_words=6),
                description=fake.text(max_nb_chars=500),
                category=category,
                is_story=is_story
            )
            posts.append(post)
            
        self.stdout.write(
            self.style.SUCCESS(f'Seeder posts terminé : {len(categories)} catégories et {len(posts)} posts créés')
        )
