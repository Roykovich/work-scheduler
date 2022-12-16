import yaml
import os.path

from gmail import parse_date
from calculations import create_calculations

if os.path.exists('credentials.yml'):
  with open("credentials.yml") as f:
    content = f.read()

my_credentials = yaml.load(content, Loader=yaml.FullLoader)

databaseId, first_payment, second_payment = my_credentials["database"], my_credentials["first_payment"], my_credentials["second_payment"]

def create_notion_object(schedule):
    pages = []
    
    for day in schedule:
        date = parse_date(day)
        calculations = create_calculations(date)
        entrance = date["start_date"].day

        page = {
            "parent": {
                "database_id": databaseId
            },
            "properties": {
                "Entrada" : {
                    "type": "date",
                    "date": {
                        "start": date["start_date"].isoformat("T") + "-03:00",
                        "end": None,
                    }
                },
                "Salida" : {
                    "type": "date",
                    "date": {
                        "start": date["end_date"].isoformat("T") + "-03:00",
                        "end": None,
                    }
                },
                "Diurnas": {
                    "type": "number",
                    "number": calculations["total-diurno"]
                },
                "Nocturnas": {
                    "type": "number",
                    "number": calculations["total-nocturno"]
                },
                "Relation": {
                    "relation": [
                        {
                            "id": first_payment if entrance <= 15 else second_payment
                        }
                    ],
                    "has_more": False
                },
                "Nombre":{
                    "id":"title",
                    "type":"title",
                    "title": [{
                          "type":"text",
                          "text": {
                              "content":"Turno en McDonald's",
                              "link": None
                          },
                          "plain_text":"Turno en McDonald's",
                          "href": None
                      }]
                }
            }
        }

        pages.append(page)
    
    return pages