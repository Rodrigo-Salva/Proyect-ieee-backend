from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.organization.models import Branch, Chapter, Member
from apps.content.models import News, Event, Announcement
from apps.contact.models import ContactForm
from apps.resources.models import EducationalResource
from apps.users.models import User
from datetime import timedelta
import random
from faker import Faker

class Command(BaseCommand):
    help = 'Popula la base de datos con datos masivos de prueba (min 20 por tabla)'

    def handle(self, *args, **kwargs):
        fake = Faker(['es_ES'])
        self.stdout.write('Iniciando población masiva de datos...')

        # 1. Crear Usuario Admin
        admin_user, _ = User.objects.get_or_create(
            username='admin_test',
            email='admin@test.com',
            defaults={
                'is_staff': True, 
                'is_superuser': True,
                'role': 'admin'
            }
        )
        if _:
            admin_user.set_password('admin123')
            admin_user.save()

        # 2. Rama Principal
        branch, _ = Branch.objects.get_or_create(
            name='IEEE Tecsup',
            defaults={
                'description': fake.text(max_nb_chars=200),
                'is_active': True
            }
        )

        # 3. Capítulos (Asegurar min 5)
        chapter_names = ['Computer Society', 'RAS', 'PES', 'WIE', 'IAS', 'ComSoc']
        chapters = []
        for name in chapter_names:
            chapter, _ = Chapter.objects.get_or_create(
                name=name,
                branch=branch,
                defaults={'description': fake.text(max_nb_chars=150)}
            )
            chapters.append(chapter)
        
        # 4. Miembros (Min 25)
        current_members = Member.objects.count()
        if current_members < 25:
            to_create = 25 - current_members
            self.stdout.write(f'Creando {to_create} miembros...')
            for _ in range(to_create):
                is_direct = random.choice([True, False])
                chapter = random.choice(chapters) if not is_direct else None
                
                Member.objects.create(
                    full_name=fake.name(),
                    email=fake.email(),
                    phone=fake.phone_number()[:20],
                    position=fake.job(),
                    branch=branch,
                    chapter=chapter,
                    is_active=True
                )

        # 5. Noticias (Min 25)
        current_news = News.objects.count()
        if current_news < 25:
            to_create = 25 - current_news
            self.stdout.write(f'Creando {to_create} noticias...')
            categories = [c[0] for c in News.CATEGORY_CHOICES]
            for _ in range(to_create):
                News.objects.create(
                    title=fake.sentence(nb_words=6),
                    content=fake.text(max_nb_chars=500),
                    category=random.choice(categories),
                    author=admin_user,
                    is_published=True,
                    published_date=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
                )

        # 6. Eventos (Min 25)
        current_events = Event.objects.count()
        if current_events < 25:
            to_create = 25 - current_events
            self.stdout.write(f'Creando {to_create} eventos...')
            for _ in range(to_create):
                Event.objects.create(
                    title=fake.catch_phrase(),
                    description=fake.text(max_nb_chars=300),
                    event_date=fake.date_time_between(start_date='-6m', end_date='+6m', tzinfo=timezone.get_current_timezone()),
                    location=fake.address(),
                    created_by=admin_user
                )

        # 7. Convocatorias (Min 25)
        current_ann = Announcement.objects.count()
        if current_ann < 25:
            to_create = 25 - current_ann
            self.stdout.write(f'Creando {to_create} convocatorias...')
            for _ in range(to_create):
                Announcement.objects.create(
                    title=f"Convocatoria: {fake.job()}",
                    description=fake.text(max_nb_chars=400),
                    deadline=fake.date_time_between(start_date='now', end_date='+3m', tzinfo=timezone.get_current_timezone()),
                    requirements=fake.text(max_nb_chars=200),
                    created_by=admin_user,
                    is_active=True
                )

        # 8. Formularios de Contacto (Min 25)
        current_forms = ContactForm.objects.count()
        if current_forms < 25:
            to_create = 25 - current_forms
            self.stdout.write(f'Creando {to_create} forms de contacto...')
            for _ in range(to_create):
                # Usar create directamente ya que submitted_at es auto_now_add, 
                # no podemos setearlo facilmente sin hackear, pero está bien que sean 'ahora'
                ContactForm.objects.create(
                    full_name=fake.name(),
                    email=fake.email(),
                    subject=fake.sentence(nb_words=5),
                    message=fake.text(max_nb_chars=300),
                    is_read=random.choice([True, False])
                )

        # 9. Recursos Educativos (Min 25)
        current_resources = EducationalResource.objects.count()
        if current_resources < 25:
            to_create = 25 - current_resources
            self.stdout.write(f'Creando {to_create} recursos educativos...')
            categories = [c[0] for c in EducationalResource.CATEGORY_CHOICES]
            for _ in range(to_create):
                EducationalResource.objects.create(
                    title=f"Recurso: {fake.catch_phrase()}",
                    description=fake.text(max_nb_chars=300),
                    category=random.choice(categories),
                    uploaded_by=admin_user,
                    file='resources/sample.pdf', # Placeholder
                    download_count=fake.random_int(min=0, max=100)
                )

        self.stdout.write(self.style.SUCCESS(f'Población masiva completada. Base de datos rica en datos.'))
