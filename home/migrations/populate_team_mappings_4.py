# Generated by Django 3.0.1 on 2020-03-20 06:06
import sys
from django.db import migrations


def load_team_mappings(apps, schema_editor):
    TeamMapping = apps.get_model('home', 'TeamMapping')

    # Arsenal
    fpl_arsenal_map = TeamMapping(id=1, value_id=0, api_id=0,
                                  numeric_external_identifier=1)
    fpl_arsenal_map.save()

    fbdata_arsenal_map = TeamMapping(id=2, value_id=0, api_id=1,
                                     numeric_external_identifier=57)
    fbdata_arsenal_map.save()

    # Aston Villa
    fpl_aston_villa_map = TeamMapping(id=3, value_id=1, api_id=0,
                                      numeric_external_identifier=2)
    fpl_aston_villa_map.save()

    fbdata_aston_villa_map = TeamMapping(id=4, value_id=1, api_id=1,
                                         numeric_external_identifier=58)
    fbdata_aston_villa_map.save()

    # Bournemouth
    fpl_bournemouth_map = TeamMapping(id=5, value_id=2, api_id=0,
                                      numeric_external_identifier=3)
    fpl_bournemouth_map.save()

    fbdata_bournemouth_map = TeamMapping(id=6, value_id=2, api_id=1,
                                         numeric_external_identifier=1044)
    fbdata_bournemouth_map.save()

    # Brighton
    fpl_brighton_map = TeamMapping(id=7, value_id=3, api_id=0,
                                   numeric_external_identifier=4)
    fpl_brighton_map.save()

    fbdata_brighton_map = TeamMapping(id=8, value_id=3, api_id=1,
                                      numeric_external_identifier=397)

    fbdata_brighton_map.save()
    # Burnley
    fpl_burnley_map = TeamMapping(id=9, value_id=4, api_id=0,
                                  numeric_external_identifier=5)
    fpl_burnley_map.save()

    fbdata_burnley_map = TeamMapping(id=10, value_id=4, api_id=1,
                                     numeric_external_identifier=328)
    fbdata_burnley_map.save()

    # Chelsea
    fpl_chelsea_map = TeamMapping(id=11, value_id=5, api_id=0,
                                  numeric_external_identifier=6)
    fpl_chelsea_map.save()

    fbdata_chelsea_map = TeamMapping(id=12, value_id=5, api_id=1,
                                     numeric_external_identifier=61)
    fbdata_chelsea_map.save()

    # Crystal Palace
    fpl_crystal_palace_map = TeamMapping(id=13, value_id=6, api_id=0,
                                         numeric_external_identifier=7)
    fpl_crystal_palace_map.save()

    fbdata_crystal_palace_map = TeamMapping(id=14, value_id=6, api_id=1,
                                            numeric_external_identifier=354)
    fbdata_crystal_palace_map.save()

    # Everton
    fpl_everton_map = TeamMapping(id=15, value_id=7, api_id=0,
                                  numeric_external_identifier=8)
    fpl_everton_map.save()

    fbdata_everton_map = TeamMapping(id=16, value_id=7, api_id=1,
                                     numeric_external_identifier=62)
    fbdata_everton_map.save()

    # Leicester
    fpl_leicester_map = TeamMapping(id=17, value_id=8, api_id=0,
                                    numeric_external_identifier=9)
    fpl_leicester_map.save()

    fbdata_leicester_map = TeamMapping(id=18, value_id=8, api_id=1,
                                       numeric_external_identifier=338)
    fbdata_leicester_map.save()

    # Liverpool
    fpl_liverpool_map = TeamMapping(id=19, value_id=9, api_id=0,
                                    numeric_external_identifier=10)
    fpl_liverpool_map.save()

    fbdata_liverpool_map = TeamMapping(id=20, value_id=9, api_id=1,
                                       numeric_external_identifier=64)
    fbdata_liverpool_map.save()

    # Man City
    fpl_man_city_map = TeamMapping(id=21, value_id=10, api_id=0,
                                   numeric_external_identifier=11)
    fpl_man_city_map.save()

    fbdata_man_city_map = TeamMapping(id=22, value_id=10, api_id=1,
                                      numeric_external_identifier=65)
    fbdata_man_city_map.save()

    # Man United
    fpl_man_united_map = TeamMapping(id=23, value_id=11, api_id=0,
                                     numeric_external_identifier=12)
    fpl_man_united_map.save()

    fbdata_man_united_map = TeamMapping(id=24, value_id=11, api_id=1,
                                        numeric_external_identifier=66)
    fbdata_man_united_map.save()

    # Newcastle
    fpl_newcastle_map = TeamMapping(id=25, value_id=12, api_id=0,
                                    numeric_external_identifier=13)
    fpl_newcastle_map.save()

    fbdata_newcastle_map = TeamMapping(id=26, value_id=12, api_id=1,
                                       numeric_external_identifier=67)
    fbdata_newcastle_map.save()

    # Norwich
    fpl_norwich_map = TeamMapping(id=27, value_id=13, api_id=0,
                                  numeric_external_identifier=14)
    fpl_norwich_map.save()

    fbdata_norwich_map = TeamMapping(id=28, value_id=13, api_id=1,
                                     numeric_external_identifier=68)
    fbdata_norwich_map.save()

    # Sheffield United
    fpl_sheffield_map = TeamMapping(id=29, value_id=14, api_id=0,
                                    numeric_external_identifier=15)
    fpl_sheffield_map.save()

    fbdata_sheffield_map = TeamMapping(id=30, value_id=14, api_id=1,
                                       numeric_external_identifier=356)
    fbdata_sheffield_map.save()

    # Southampton
    fpl_southampton_map = TeamMapping(id=31, value_id=15, api_id=0,
                                      numeric_external_identifier=16)
    fpl_southampton_map.save()

    fbdata_southampton_map = TeamMapping(id=32, value_id=15, api_id=1,
                                         numeric_external_identifier=340)
    fbdata_southampton_map.save()

    # Tottenham
    fpl_tottenham_map = TeamMapping(id=33, value_id=16, api_id=0,
                                    numeric_external_identifier=17)
    fpl_tottenham_map.save()

    fbdata_tottenham_map = TeamMapping(id=34, value_id=16, api_id=1,
                                       numeric_external_identifier=73)
    fbdata_tottenham_map.save()

    # Watford
    fpl_watford_map = TeamMapping(id=35, value_id=17, api_id=0,
                                  numeric_external_identifier=18)
    fpl_watford_map.save()

    fbdata_watford_map = TeamMapping(id=36, value_id=17, api_id=1,
                                     numeric_external_identifier=346)
    fbdata_watford_map.save()

    # West Ham
    fpl_west_ham_map = TeamMapping(id=37, value_id=19, api_id=0,
                                   numeric_external_identifier=19)
    fpl_west_ham_map.save()

    fbdata_west_ham_map = TeamMapping(id=38, value_id=19, api_id=1,
                                      numeric_external_identifier=563)
    fbdata_west_ham_map.save()

    # Wolves
    fpl_wolves_map = TeamMapping(id=39, value_id=20, api_id=0,
                                 numeric_external_identifier=20)
    fpl_wolves_map.save()

    fbdata_wolves_map = TeamMapping(id=40, value_id=20, api_id=1,
                                    numeric_external_identifier=76)
    fbdata_wolves_map.save()


def delete_team_mappings(apps, schema_editor):
    TeamMapping = apps.get_model('home', 'TeamMapping')
    TeamMapping.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', 'populate_request_types')
    ]

    operations = [
       migrations.RunPython(load_team_mappings, delete_team_mappings)
    ] if 'test' not in sys.argv[1:] else []
