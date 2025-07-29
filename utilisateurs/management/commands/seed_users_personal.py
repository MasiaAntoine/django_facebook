from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from PIL import Image
import io
import urllib.request

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeder pour créer les profils personnels (Antoine MASIA et Maël Badet)'

    def download_profile_image_from_url(self, url, username):
        """Télécharge une image depuis une URL et la convertit pour la base de données"""
        try:
            # Télécharger l'image
            with urllib.request.urlopen(url) as response:
                image_data = response.read()
            
            # Ouvrir l'image avec PIL pour la redimensionner
            image = Image.open(io.BytesIO(image_data))
            
            # Redimensionner à 200x200 et convertir en RGB si nécessaire
            image = image.convert('RGB')
            image = image.resize((200, 200), Image.Resampling.LANCZOS)
            
            # Convertir en bytes
            img_io = io.BytesIO()
            image.save(img_io, format='JPEG', quality=90)
            img_io.seek(0)
            
            return ContentFile(img_io.getvalue(), name=f'{username}_profile.jpg')
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Erreur téléchargement image pour {username}: {str(e)}')
            )
            return None

    def handle(self, *args, **options):
        # Vérifier et créer/recréer Antoine MASIA
        if User.objects.filter(username='amasia').exists():
            self.stdout.write(
                self.style.WARNING('L\'utilisateur amasia existe déjà. Suppression et recréation...')
            )
            User.objects.filter(username='amasia').delete()
        
        # Créer le profil spécifique d'Antoine MASIA
        self.stdout.write('Création du profil Antoine MASIA...')
        antoine_user = User.objects.create_user(
            username='amasia',
            email='pro.antoine.masia@gmail.com',
            password='password123',
            first_name='Antoine',
            last_name='MASIA',
            telephone='0612345678',
            ville='Toulouse',
            est_privee=False
        )
        
        # Télécharger et assigner la photo de profil d'Antoine depuis l'URL
        antoine_image_url = 'https://scontent-cdg4-2.xx.fbcdn.net/v/t39.30808-1/496967156_2867948320043464_2608270349292282823_n.jpg?stp=cp6_dst-jpg_s480x480_tt6&_nc_cat=109&ccb=1-7&_nc_sid=e99d92&_nc_ohc=xajj8oL75xIQ7kNvwHL2JAz&_nc_oc=Adlizf5dYXJeesOYHc9vTJaA9YU393rFyAQ2wE8OqoAqk1PZqPHh_GJJ5P4MPlSqrhNq0JV3rifBFOv7DIieWRrj&_nc_zt=24&_nc_ht=scontent-cdg4-2.xx&_nc_gid=NrfGWc7lOUMPsi8-R2k8YQ&oh=00_AfRfzsNO4W0P2nGJAX6wACXMQ52T-weoqQ2we3-Etpx7VQ&oe=688E9E7D'
        
        self.stdout.write('Téléchargement de la photo de profil Antoine...')
        profile_image = self.download_profile_image_from_url(antoine_image_url, 'amasia')
        
        if profile_image:
            antoine_user.photo_profil.save(
                'amasia_profile.jpg',
                profile_image,
                save=True
            )
            self.stdout.write(
                self.style.SUCCESS('✓ Photo téléchargée et assignée pour Antoine MASIA')
            )
        else:
            self.stdout.write(
                self.style.WARNING('❌ Photo par défaut utilisée pour Antoine MASIA')
            )
        
        # Vérifier et créer/recréer Maël Badet
        if User.objects.filter(username='mbadet').exists():
            self.stdout.write(
                self.style.WARNING('L\'utilisateur mbadet existe déjà. Suppression et recréation...')
            )
            User.objects.filter(username='mbadet').delete()
        
        # Créer le profil spécifique de Maël Badet
        self.stdout.write('Création du profil Maël Badet...')
        mael_user = User.objects.create_user(
            username='mbadet',
            email='maelbadet21@gmail.com',
            password='password123',
            first_name='Maël',
            last_name='Badet',
            telephone='0623456789',
            ville='Saint-Saturnin',
            est_privee=False
        )
        
        # Télécharger et assigner la photo de profil de Maël depuis l'URL
        mael_image_url = 'https://media.licdn.com/dms/image/v2/D4E03AQHHXP24k4ym1Q/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1682530646392?e=2147483647&v=beta&t=sF5v_uwWgc9aO21edJuhDLIuhKoyEjAqlMHV6CsJX4U'
        
        self.stdout.write('Téléchargement de la photo de profil Maël...')
        mael_profile_image = self.download_profile_image_from_url(mael_image_url, 'mbadet')
        
        if mael_profile_image:
            mael_user.photo_profil.save(
                'mbadet_profile.jpg',
                mael_profile_image,
                save=True
            )
            self.stdout.write(
                self.style.SUCCESS('✓ Photo téléchargée et assignée pour Maël Badet')
            )
        else:
            self.stdout.write(
                self.style.WARNING('❌ Photo par défaut utilisée pour Maël Badet')
            )
        
        self.stdout.write(
            self.style.SUCCESS('✓ Profils personnels créés avec succès!')
        )
        
        # Informations de connexion
        self.stdout.write('')
        self.stdout.write('📋 Informations de connexion:')
        self.stdout.write('')
        self.stdout.write('👤 Antoine MASIA:')
        self.stdout.write(f'   Username: amasia')
        self.stdout.write(f'   Password: password123')
        self.stdout.write(f'   Email: pro.antoine.masia@gmail.com')
        self.stdout.write(f'   Ville: Toulouse')
        self.stdout.write(f'   Profil: Public')
        self.stdout.write('')
        self.stdout.write('👤 Maël Badet:')
        self.stdout.write(f'   Username: mbadet')
        self.stdout.write(f'   Password: password123')
        self.stdout.write(f'   Email: maelbadet21@gmail.com')
        self.stdout.write(f'   Ville: Saint-Saturnin')
        self.stdout.write(f'   Profil: Public')
