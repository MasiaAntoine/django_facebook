from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from faker import Faker
import random
from PIL import Image, ImageDraw, ImageFont
import io
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeder pour créer des utilisateurs de test'

    def generate_profile_picture(self, first_name, last_name, size=200):
        """Génère une image de profil avec les initiales de l'utilisateur"""
        # Couleurs aléatoires pour l'arrière-plan
        colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
            '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
        ]
        bg_color = random.choice(colors)
        
        # Créer une image avec arrière-plan coloré
        image = Image.new('RGB', (size, size), bg_color)
        draw = ImageDraw.Draw(image)
        
        # Obtenir les initiales
        initials = (first_name[0] + last_name[0]).upper()
        
        # Essayer de charger une police, sinon utiliser la police par défaut
        try:
            font_size = size // 3
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
        except:
            try:
                font_size = size // 3
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Calculer la position du texte pour le centrer
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        # Dessiner le texte
        draw.text((x, y), initials, fill='white', font=font)
        
        # Convertir en bytes
        img_io = io.BytesIO()
        image.save(img_io, format='PNG')
        img_io.seek(0)
        
        return ContentFile(img_io.getvalue(), name=f'{first_name}_{last_name}_profile.png')

    def handle(self, *args, **options):
        fake = Faker('fr_FR')
        
        # Reset: supprimer tous les utilisateurs existants
        self.stdout.write('Suppression des utilisateurs existants...')
        User.objects.all().delete()
        
        # Créer 20 utilisateurs aléatoires
        self.stdout.write('Création de 20 utilisateurs aléatoires avec photos de profil...')
        users = []
        
        for i in range(20):
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            # Générer un pseudo réaliste
            username_options = [
                f"{first_name.lower()}.{last_name.lower()}",
                f"{first_name.lower()}{last_name.lower()}",
                f"{first_name.lower()}_{last_name.lower()}",
                f"{first_name.lower()}{random.randint(10, 99)}",
                f"{last_name.lower()}{first_name[0].lower()}",
                f"{first_name[0].lower()}.{last_name.lower()}",
                f"{first_name.lower()}_{random.randint(1990, 2005)}",
                f"{last_name.lower()}.{first_name[0].lower()}"
            ]
            
            # Choisir un pseudo et s'assurer qu'il est unique
            username = random.choice(username_options)
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            email = fake.email()
            # Générer un numéro de téléphone plus court
            telephone = fake.numerify('0#########')  # 10 chiffres maximum
            ville = fake.city()
            # Profil privé aléatoire (30% de chance d'être privé)
            est_privee = random.choice([True, False, False, False])  # 25% True, 75% False
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',
                first_name=first_name,
                last_name=last_name,
                telephone=telephone,
                ville=ville,
                est_privee=est_privee
            )
            
            # Générer et assigner une photo de profil
            try:
                profile_picture = self.generate_profile_picture(first_name, last_name)
                user.photo_profil.save(
                    f'{username}_profile.png',
                    profile_picture,
                    save=True
                )
                self.stdout.write(f'✓ Photo créée pour {username}')
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Erreur création photo pour {username}: {str(e)}')
                )
            
            # Afficher le statut du profil
            status = "privé" if est_privee else "public"
            self.stdout.write(f'✓ Utilisateur {username} créé (profil {status})')
            
            users.append(user)
        
        self.stdout.write(
            self.style.SUCCESS(f'Seeder utilisateurs terminé : {len(users)} utilisateurs créés avec photos de profil')
        )
        
        # Statistiques des profils
        profils_prives = sum(1 for user in users if user.est_privee)
        profils_publics = len(users) - profils_prives
        self.stdout.write(f'📊 Statistiques: {profils_publics} profils publics, {profils_prives} profils privés')
        self.stdout.write('')
        self.stdout.write('� Pour créer le profil Antoine MASIA, utilisez: python manage.py seed_users_personal')
