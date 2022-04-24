from django.core.management.base import BaseCommand, CommandError

from justwrite.settings import goal_progress_total, goal_progress_wipe
from projects.models import Project


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("checking")
        checked_ids = []
        for project in Project.objects.all():
            if (project.user not in checked_ids) and (project.goalProgress >= goal_progress_total):
                checked_ids.append(project.user)
            project.goalProgress = goal_progress_wipe
            project.save()

        for x in checked_ids:
            x.increment_streak()

        for project in Project.objects.all():
            if project.user not in checked_ids:
                project.user.wipe_streak()