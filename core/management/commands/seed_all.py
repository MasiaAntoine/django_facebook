from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction


class Command(BaseCommand):
    help = 'Seeder général qui exécute tous les seeders dans le bon ordre'

    def handle(self, *args, **options):
        self.stdout.write('=== DÉBUT DU SEEDING GÉNÉRAL ===')
        
        try:
            with transaction.atomic():
                # 1. Seeder les utilisateurs en premier (prérequis pour les autres)
                self.stdout.write('\n1. Exécution du seeder utilisateurs...')
                call_command('seed_users')
                
                # 2. Seeder les utilisateurs personnels
                self.stdout.write('\n2. Exécution du seeder utilisateurs personnels...')
                call_command('seed_users_personal')
                
                # 3. Seeder les posts et catégories
                self.stdout.write('\n3. Exécution du seeder posts...')
                call_command('seed_posts')
                
                # 4. Seeder les relations d'amitié
                self.stdout.write('\n4. Exécution du seeder amis...')
                call_command('seed_amis')
                
                # 5. Seeder les interactions
                self.stdout.write('\n5. Exécution du seeder interactions...')
                call_command('seed_interactions')
                
                # 6. Seeder les notifications
                self.stdout.write('\n6. Exécution du seeder notifications...')
                call_command('seed_notifications')
                
                self.stdout.write(
                    self.style.SUCCESS('\n=== SEEDING GÉNÉRAL TERMINÉ AVEC SUCCÈS ===')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n=== ERREUR LORS DU SEEDING : {str(e)} ===')
            )
            raise
