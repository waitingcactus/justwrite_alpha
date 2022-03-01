from django.core.management.base import BaseCommand, CommandError

from projects.models import Project


class Command(BaseCommand):

    def handle(*args, **options):
        print("checking")
        checked_ids = []
        for project in Project.objects.all():
            if (project.user not in checked_ids) and (project.goalProgress >= 1):
                checked_ids.append(project.user)
            project.goalProgress = 0
            project.save()

        for x in checked_ids:
            x.increment_streak()

        for project in Project.objects.all():
            if project.user not in checked_ids:
                project.user.wipe_streak()