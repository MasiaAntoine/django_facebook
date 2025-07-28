from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from notifications.models import Notification
from faker import Faker
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeder pour créer des notifications de test'

    def handle(self, *args, **options):
        fake = Faker('fr_FR')
        
        # Reset: supprimer toutes les notifications existantes
        self.stdout.write('Suppression des notifications existantes...')
        Notification.objects.all().delete()
        
        # Récupérer tous les utilisateurs
        users = list(User.objects.all())
        
        if len(users) < 2:
            self.stdout.write(
                self.style.ERROR('Au moins 2 utilisateurs sont nécessaires. Veuillez d\'abord exécuter le seeder des utilisateurs.')
            )
            return
        
        # Créer des notifications
        self.stdout.write('Création des notifications...')
        notifications = []
        notif_types = ['like', 'comment', 'friend_request', 'share']
        
        messages_templates = {
            'like': '{emetteur} a aimé votre publication',
            'comment': '{emetteur} a commenté votre publication',
            'friend_request': '{emetteur} vous a envoyé une demande d\'ami',
            'share': '{emetteur} a partagé votre publication'
        }
        
        for i in range(60):
            utilisateur = random.choice(users)
            emetteur = random.choice([u for u in users if u != utilisateur])
            notif_type = random.choice(notif_types)
            
            message = messages_templates[notif_type].format(
                emetteur=emetteur.get_full_name() or emetteur.username
            )
            
            notification = Notification.objects.create(
                utilisateur=utilisateur,
                emetteur=emetteur,
                type=notif_type,
                message=message,
                lu=random.choice([True, False])
            )
            notifications.append(notification)
                    
        self.stdout.write(
            self.style.SUCCESS(f'Seeder notifications terminé : {len(notifications)} notifications créées')
        )
