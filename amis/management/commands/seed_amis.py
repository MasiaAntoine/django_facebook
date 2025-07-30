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
        
        # Ne supprime plus aucune relation d'amitié existante
        self.stdout.write('Aucune suppression de relations d\'amitié existantes (préservation totale).')
        
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
        
        # Récupérer les relations existantes pour éviter les doublons
        existing_relations = set()
        for relation in Ami.objects.all():
            existing_relations.add((relation.demandeur.id, relation.receveur.id))
        
        # Créer environ 30 nouvelles relations d'amitié
        attempts = 0
        max_attempts = 100  # Éviter une boucle infinie
        
        while len(amis) < 30 and attempts < max_attempts:
            attempts += 1
            
            demandeur = random.choice(users)
            receveur = random.choice(users)
            
            # Éviter les auto-relations et les doublons
            if demandeur != receveur:
                # Vérifier si cette relation existe déjà (dans les deux sens)
                if ((demandeur.id, receveur.id) not in existing_relations and
                    (receveur.id, demandeur.id) not in existing_relations):
                    
                    pair = tuple(sorted([demandeur.id, receveur.id]))
                    if pair not in created_pairs:
                        created_pairs.add(pair)
                        existing_relations.add((demandeur.id, receveur.id))
                        
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
