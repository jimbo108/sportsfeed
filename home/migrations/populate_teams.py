# Generated by Django 3.0.1 on 2019-12-31 09:54

from django.db import migrations

def load_teams(apps, schema_editor):
    Team = apps.get_model('home', 'Team')
    team_arsenal = Team(id=0, name="Arsenal")
    team_arsenal.save()
    
    team_aston_villa = Team(id=1, name="Aston Villa")
    team_aston_villa.save()

    team_bournemouth = Team(id=2, name="AFC Bournemouth")
    team_bournemouth.save()

    team_brighton = Team(id=3, name="Brighton and Hove Albion")
    team_brighton.save()

    team_burnley = Team(id=4, name="Burnley")
    team_burnley.save()

    team_chelsea = Team(id=5, name="Chelsea")
    team_chelsea.save()

    team_crystal_palace = Team(id=6, name="Crystal Palace")
    team_crystal_palace.save()

    team_everton = Team(id=7, name="Everton")
    team_everton.save()

    team_leicester = Team(id=8, name="Leicester City")
    team_leicester.save()

    team_liverpool = Team(id=9, name="Liverpool")
    team_liverpool.save()

    team_man_city = Team(id=10, name="Manchester City")
    team_man_city.save()

    team_man_united = Team(id=11, name="Manchester United")
    team_man_united.save()

    team_newcastle = Team(id=12, name="Newcastle United")
    team_newcastle.save()

    team_norwich = Team(id=13, name="Norwich City")
    team_norwich.save()

    team_sheffield = Team(id=14, name="Sheffield United")
    team_sheffield.save()

    team_southampton = Team(id=15, name="Southampton")
    team_southampton.save()

    team_tottenham = Team(id=16, name="Tottenham Hotspur")
    team_tottenham.save()

    team_watford = Team(id=17, name="Watford")
    team_watford.save()

    team_west_ham = Team(id=19, name="West Ham United")
    team_west_ham.save()

    team_wolves = Team(id=20, name="Wolverhampton Wanderers")
    team_wolves.save()

def delete_teams(apps, schema_editor):
    Team = apps.get_model("home", "Team")
    Team.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_teams, delete_teams)
    ]
