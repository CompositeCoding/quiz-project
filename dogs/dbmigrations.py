from .models import Dog, HardDealbreaker, SoftDealbreaker, Score
from airtable import Airtable
from airtable.auth import AirtableAuth
import requests
from quiz.settings import env
import time
import requests

"""
'_db_h_size'         = klein, middel, groot, 3
'_db_h_owner'        = type eigenaar, 5
'_db_h_move'         = hoe veel beweging, 4
'_db_s_child'        = Wel kinds, geen kids, 2
'_db_s_fur'          = verharen,
'_db_s_care'         = veel, medium, weinig, 3
'_db_s_train'        = hoe makkelijk opvoeden, 4
'_db_s_house'        = Hoe groot woon je, 4
'_db_s_experience'   = hoe veel ervaring, 3
"""


def migrate_dogs():
    Dog.objects.all().delete()
    airtable = Airtable(env('BASE_KEY'),env('TABLE_NAME'),env('API_KEY'))
    table = airtable.get_all()
    for i in table:
        if len(i['fields']) > 8 :
            if '_db_image' in i['fields'] and '_db_link' in i['fields']:

                d = Dog(id=i['id'],name=i['fields']['Ras'],image=i['fields']['_db_image'],link=i['fields']['_db_link'])
                d.save()

                for field in i['fields']:
                    if '_db_h_' in field:
                        for rec in i['fields'][field]:
                            record =  airtable.get(rec)
                            HardDealbreaker.objects.get_or_create(dog=d,name=field,value=record['fields']['Value'])

                    if '_db_s_' in field:
                        for rec in i['fields'][field]:
                            record =  airtable.get(rec)
                            SoftDealbreaker.objects.get_or_create(dog=d,name=field,value=record['fields']['Value'])

                    if '_db_c_' in field:
                        for rec in i['fields'][field]:
                            record =  airtable.get(rec)
                            Score.objects.get_or_create(dog=d,name=field,value=record['fields']['Value'])
