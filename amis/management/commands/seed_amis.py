from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import models
from amis.models import Ami
from faker import Faker
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeder pour créer des relations d\'amitié de test'

    def handle(self, *args, **options):
        fake = Faker('fr_FR')
        
        # Reset: supprimer toutes les relations d'amitié existantes
        self.stdout.write('Suppression des relations d\'amitié existantes...')
        Ami.objects.all().delete()
        
        # Récupérer tous les utilisateurs
        users = list(User.objects.all())
        
        if len(users) < 2:
            self.stdout.write(
                self.style.ERROR('Au moins 2 utilisateurs sont nécessaires. Veuillez d\'abord exécuter le seeder des utilisateurs.')
            )
            return
        
        # Créer des relations d'amitié
        self.stdout.write('Création des relations d\'amitié...')
        amis = []
        created_pairs = set()
        
        # Créer environ 30 relations d'amitié
        for i in range(30):
            demandeur = random.choice(users)
            receveur = random.choice(users)
            
            # Éviter les auto-relations et les doublons
            if demandeur != receveur:
                pair = tuple(sorted([demandeur.id, receveur.id]))
                if pair not in created_pairs:
                    created_pairs.add(pair)
                    
                    ami = Ami.objects.create(
                        demandeur=demandeur,
                        receveur=receveur,
                        accepter=random.choice([True, False]),
                        bloquer=random.choice([True, False]) if random.random() < 0.1 else False
                    )
                    amis.append(ami)
                    
        self.stdout.write(
            self.style.SUCCESS(f'Seeder amis terminé : {len(amis)} relations d\'amitié créées')
        )
