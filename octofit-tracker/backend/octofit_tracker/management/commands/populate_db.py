from django.core.management.base import BaseCommand
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index([("email", 1)], unique=True)

        # Sample users (super heroes)
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "marvel"},
            {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
            {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
        ]
        db.users.insert_many(users)

        # Teams
        teams = [
            {"name": "marvel", "members": [u["email"] for u in users if u["team"] == "marvel"]},
            {"name": "dc", "members": [u["email"] for u in users if u["team"] == "dc"]},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {"user_email": "ironman@marvel.com", "activity": "Running", "duration": 30},
            {"user_email": "superman@dc.com", "activity": "Flying", "duration": 60},
            {"user_email": "batman@dc.com", "activity": "Martial Arts", "duration": 45},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"team": "marvel", "points": 300},
            {"team": "dc", "points": 350},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"user_email": "spiderman@marvel.com", "workout": "Web Swinging", "intensity": "high"},
            {"user_email": "wonderwoman@dc.com", "workout": "Lasso Training", "intensity": "medium"},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
