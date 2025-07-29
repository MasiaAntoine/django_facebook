from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeder pour créer des utilisateurs de test'

    def handle(self, *args, **options):
        fake = Faker('fr_FR')
        
        # Reset: supprimer tous les utilisateurs existants
        self.stdout.write('Suppression des utilisateurs existants...')
        User.objects.all().delete()
        
        # Créer 20 utilisateurs
        self.stdout.write('Création de 20 utilisateurs...')
        users = []
        
        for i in range(20):
            username = f"user_{i+1}"
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            # Générer un numéro de téléphone plus court
            telephone = fake.numerify('0#########')  # 10 chiffres maximum
            ville = fake.city()
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',
                first_name=first_name,
                last_name=last_name,
                telephone=telephone,
                ville=ville
            )
            users.append(user)
            
        self.stdout.write(
            self.style.SUCCESS(f'Seeder utilisateurs terminé : {len(users)} utilisateurs créés')
        )
