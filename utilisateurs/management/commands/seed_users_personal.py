from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db.models import Q
from PIL import Image
import io
import urllib.request
import random
from faker import Faker
from datetime import datetime, timedelta
from django.utils import timezone

# Import des modèles
from posts.models import Post, Category
from amis.models import Ami
from interactions.models import Reaction, Commentaire, Partage
from notifications.models import Notification

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
        mael_image_url = 'https://scontent-cdg4-2.cdninstagram.com/v/t51.2885-19/498682209_18301623964244205_1426888806743377396_n.jpg?stp=dst-jpg_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby4xMDgwLmMyIn0&_nc_ht=scontent-cdg4-2.cdninstagram.com&_nc_cat=109&_nc_oc=Q6cZ2QH_YzOXa8J29cr7jbS_sgQwvDk3eke548C8GHAvf8LHFejoeh2rD9BsPx82h5SHSaAUxqNjBk5hLrgB0Pj41QSZ&_nc_ohc=o_s5nMwffaUQ7kNvwHVdoay&_nc_gid=Kfd4WcKg3XHUI5NSdNQcdg&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_AfQxOYAl0tLI3JToZ9mm2l39NLaUauMnc8nTthSAM3bWPw&oe=68925249&_nc_sid=8b3546'
        
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
        
        # Récupérer tous les utilisateurs existants
        all_users = list(User.objects.exclude(username__in=['amasia', 'mbadet']))
        
        if len(all_users) == 0:
            self.stdout.write(
                self.style.WARNING('⚠️  Aucun autre utilisateur trouvé. Lancez d\'abord: python manage.py seed_users')
            )
            return
        
        # Créer des relations d'amitié et des données complètes
        self.stdout.write('')
        self.stdout.write('🔗 Création des relations d\'amitié...')
        self.create_friendships(antoine_user, mael_user, all_users)
        
        self.stdout.write('📝 Création des catégories et posts...')
        posts = self.create_categories_and_posts(antoine_user, mael_user, all_users)
        
        self.stdout.write('❤️ Création des interactions (réactions, commentaires, partages)...')
        self.create_interactions(antoine_user, mael_user, all_users, posts)
        
        self.stdout.write('🔔 Création des notifications...')
        self.create_notifications(antoine_user, mael_user, all_users)
        
        # Statistiques finales
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Données personnelles créées avec succès !'))
        self.stdout.write('')
        self.stdout.write('📊 Résumé des données créées:')
        
        # Statistiques Antoine
        antoine_amis = Ami.objects.filter(
            Q(demandeur=antoine_user, accepter=True) |
            Q(receveur=antoine_user, accepter=True)
        ).count()
        antoine_posts = Post.objects.filter(user=antoine_user).count()
        antoine_reactions = Reaction.objects.filter(user=antoine_user).count()
        antoine_commentaires = Commentaire.objects.filter(user=antoine_user).count()
        antoine_notifications = Notification.objects.filter(utilisateur=antoine_user).count()
        
        self.stdout.write(f'👤 Antoine: {antoine_amis} amis, {antoine_posts} posts, {antoine_reactions} réactions, {antoine_commentaires} commentaires, {antoine_notifications} notifications')
        
        # Statistiques Maël
        mael_amis = Ami.objects.filter(
            Q(demandeur=mael_user, accepter=True) |
            Q(receveur=mael_user, accepter=True)
        ).count()
        mael_posts = Post.objects.filter(user=mael_user).count()
        mael_reactions = Reaction.objects.filter(user=mael_user).count()
        mael_commentaires = Commentaire.objects.filter(user=mael_user).count()
        mael_notifications = Notification.objects.filter(utilisateur=mael_user).count()
        
        self.stdout.write(f'👤 Maël: {mael_amis} amis, {mael_posts} posts, {mael_reactions} réactions, {mael_commentaires} commentaires, {mael_notifications} notifications')
        
        # Totaux
        total_posts = Post.objects.count()
        total_reactions = Reaction.objects.count()
        total_commentaires = Commentaire.objects.count()
        total_amis = Ami.objects.filter(accepter=True).count()
        
        self.stdout.write('')
        self.stdout.write(f'🌍 Totaux: {total_posts} posts, {total_reactions} réactions, {total_commentaires} commentaires, {total_amis} amitiés')

    def create_friendships(self, antoine, mael, all_users):
        """Créer des relations d'amitié pour Antoine et Maël"""
        fake = Faker('fr_FR')
        
        # Antoine et Maël sont amis
        Ami.objects.get_or_create(
            demandeur=antoine,
            receveur=mael,
            defaults={'accepter': True}
        )
        
        # Antoine a des amis (60% des utilisateurs)
        antoine_friends = random.sample(all_users, min(12, len(all_users)))
        for friend in antoine_friends:
            if friend != antoine and friend != mael:
                # Créer l'amitié (parfois Antoine demande, parfois l'autre)
                if random.choice([True, False]):
                    demandeur, receveur = antoine, friend
                else:
                    demandeur, receveur = friend, antoine
                
                Ami.objects.get_or_create(
                    demandeur=demandeur,
                    receveur=receveur,
                    defaults={'accepter': True}
                )
        
        # Maël a des amis (40% des utilisateurs)
        mael_friends = random.sample(all_users, min(8, len(all_users)))
        for friend in mael_friends:
            if friend != mael and friend != antoine and not Ami.objects.filter(
                Q(demandeur=mael, receveur=friend) | 
                Q(demandeur=friend, receveur=mael)
            ).exists():
                # Créer l'amitié
                if random.choice([True, False]):
                    demandeur, receveur = mael, friend
                else:
                    demandeur, receveur = friend, mael
                
                Ami.objects.get_or_create(
                    demandeur=demandeur,
                    receveur=receveur,
                    defaults={'accepter': True}
                )
        
        # Quelques demandes d'amitié en attente
        pending_requests = random.sample(all_users, min(3, len(all_users)))
        for user in pending_requests:
            if user != antoine and user != mael:
                Ami.objects.get_or_create(
                    demandeur=user,
                    receveur=antoine,
                    defaults={'accepter': False}
                )
    
    def create_categories_and_posts(self, antoine, mael, all_users):
        """Créer des catégories et des posts"""
        fake = Faker('fr_FR')
        
        # Créer des catégories
        categories_data = [
            ('Technologie', 'Posts sur la tech, programmation, etc.'),
            ('Voyage', 'Souvenirs et photos de voyages'),
            ('Sport', 'Activités sportives et fitness'),
            ('Nourriture', 'Recettes et restaurants'),
            ('Musique', 'Découvertes musicales'),
            ('Cinéma', 'Films et séries'),
            ('Personnel', 'Pensées et moments personnels'),
        ]
        
        categories = []
        for title, desc in categories_data:
            category, _ = Category.objects.get_or_create(
                title=title,
                defaults={'description': desc}
            )
            categories.append(category)
        
        # Posts d'Antoine (développeur passionné)
        antoine_posts_data = [
            ("Nouveau projet Django", "Je viens de terminer une app Facebook-like avec Django ! Très content du résultat 🚀", 'Technologie'),
            ("Weekend à Toulouse", "Belle journée ensoleillée dans la ville rose ☀️", 'Personnel'),
            ("Apprentissage React", "En train de me former sur React pour compléter mes compétences backend", 'Technologie'),
            ("Restaurant découverte", "Excellent restaurant japonais découvert près de chez moi 🍜", 'Nourriture'),
            ("Session de code", "Nuit blanche sur un bug... mais finalement résolu ! 💪", 'Technologie'),
            ("Motivation matinale", "Rien de mieux qu'un bon café pour commencer la journée de développement ☕", 'Personnel'),
        ]
        
        antoine_posts = []
        for title, desc, cat_name in antoine_posts_data:
            category = next((c for c in categories if c.title == cat_name), None)
            post = Post.objects.create(
                user=antoine,
                title=title,
                description=desc,
                category=category,
                created_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            antoine_posts.append(post)
        
        # Posts de Maël 
        mael_posts_data = [
            ("Soirée entre amis", "Excellente soirée avec les copains ! 🎉", 'Personnel'),
            ("Match de foot", "Victoire 3-1 aujourd'hui, on était en forme ! ⚽", 'Sport'),
            ("Série du moment", "En train de binge-watcher la nouvelle saison de ma série préférée", 'Cinéma'),
            ("Sortie vélo", "45km aujourd'hui sous le soleil, ça fait du bien ! 🚴‍♂️", 'Sport'),
            ("Cuisine maison", "Premier essai de lasagnes maison... pas mal du tout ! 🍝", 'Nourriture'),
        ]
        
        mael_posts = []
        for title, desc, cat_name in mael_posts_data:
            category = next((c for c in categories if c.title == cat_name), None)
            post = Post.objects.create(
                user=mael,
                title=title,
                description=desc,
                category=category,
                created_at=timezone.now() - timedelta(days=random.randint(1, 20))
            )
            mael_posts.append(post)
        
        # Quelques posts d'autres utilisateurs
        other_posts = []
        for user in random.sample(all_users, min(5, len(all_users))):
            if user != antoine and user != mael:
                post = Post.objects.create(
                    user=user,
                    title=fake.sentence(nb_words=4),
                    description=fake.text(max_nb_chars=200),
                    category=random.choice(categories),
                    created_at=timezone.now() - timedelta(days=random.randint(1, 15))
                )
                other_posts.append(post)
        
        return antoine_posts + mael_posts + other_posts
    
    def create_interactions(self, antoine, mael, all_users, posts):
        """Créer des réactions, commentaires et partages"""
        fake = Faker('fr_FR')
        
        # Réactions sur les posts
        for post in posts:
            # Antoine et Maël interagissent beaucoup
            if post.user != antoine and random.random() < 0.8:
                Reaction.objects.get_or_create(
                    user=antoine,
                    post=post,
                    defaults={
                        'type': random.choice(['like', 'love', 'happy']),
                        'created_at': post.created_at + timedelta(minutes=random.randint(5, 120))
                    }
                )
            
            if post.user != mael and random.random() < 0.7:
                Reaction.objects.get_or_create(
                    user=mael,
                    post=post,
                    defaults={
                        'type': random.choice(['like', 'love', 'happy']),
                        'created_at': post.created_at + timedelta(minutes=random.randint(5, 120))
                    }
                )
            
            # Autres utilisateurs réagissent
            for user in random.sample(all_users, random.randint(1, min(5, len(all_users)))):
                if user != post.user and random.random() < 0.4:
                    Reaction.objects.get_or_create(
                        user=user,
                        post=post,
                        defaults={
                            'type': random.choice(['like', 'love', 'happy', 'sad']),
                            'created_at': post.created_at + timedelta(minutes=random.randint(5, 240))
                        }
                    )
        
        # Commentaires
        comments_antoine = [
            "Super post ! 👍",
            "J'adore cette idée !",
            "Merci pour le partage 😊",
            "Excellent travail !",
            "Très inspirant !",
            "Bravo pour ce projet !",
        ]
        
        comments_mael = [
            "Trop cool ! 🔥",
            "J'ai hâte de voir la suite",
            "Bien joué mec !",
            "Ça donne envie !",
            "Super moment !",
        ]
        
        for post in posts:
            # Antoine commente
            if post.user != antoine and random.random() < 0.6:
                Commentaire.objects.create(
                    user=antoine,
                    post=post,
                    contenu=random.choice(comments_antoine),
                    created_at=post.created_at + timedelta(minutes=random.randint(10, 180))
                )
            
            # Maël commente
            if post.user != mael and random.random() < 0.5:
                Commentaire.objects.create(
                    user=mael,
                    post=post,
                    contenu=random.choice(comments_mael),
                    created_at=post.created_at + timedelta(minutes=random.randint(10, 180))
                )
            
            # Autres commentaires
            for user in random.sample(all_users, random.randint(0, 3)):
                if user != post.user and random.random() < 0.3:
                    Commentaire.objects.create(
                        user=user,
                        post=post,
                        contenu=fake.sentence(nb_words=random.randint(3, 10)),
                        created_at=post.created_at + timedelta(minutes=random.randint(15, 300))
                    )
        
        # Quelques partages
        for post in random.sample(posts, min(8, len(posts))):
            for user in random.sample(all_users, random.randint(0, 2)):
                if user != post.user and random.random() < 0.2:
                    Partage.objects.get_or_create(
                        user=user,
                        post=post,
                        defaults={
                            'created_at': post.created_at + timedelta(hours=random.randint(1, 48))
                        }
                    )
    
    def create_notifications(self, antoine, mael, all_users):
        """Créer des notifications pour Antoine et Maël"""
        fake = Faker('fr_FR')
        
        # Notifications pour Antoine
        notifications_antoine = [
            (mael, 'friend_request'),
            (random.choice(all_users), 'like'),
            (random.choice(all_users), 'comment'),
            (random.choice(all_users), 'friend_request'),
        ]
        
        for emetteur, type_notif in notifications_antoine:
            if emetteur != antoine:
                Notification.objects.create(
                    utilisateur=antoine,
                    emetteur=emetteur,
                    type=type_notif,
                    lu=random.choice([True, False]),
                    date=timezone.now() - timedelta(hours=random.randint(1, 72))
                )
        
        # Notifications pour Maël
        notifications_mael = [
            (antoine, 'friend_request'),
            (random.choice(all_users), 'like'),
            (random.choice(all_users), 'comment'),
        ]
        
        for emetteur, type_notif in notifications_mael:
            if emetteur != mael:
                Notification.objects.create(
                    utilisateur=mael,
                    emetteur=emetteur,
                    type=type_notif,
                    lu=random.choice([True, False]),
                    date=timezone.now() - timedelta(hours=random.randint(1, 72))
                )