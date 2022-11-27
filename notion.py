import yaml
import os.path

from gmail import parse_date

if os.path.exists('credentials.yml'):
  with open("credentials.yml") as f:
    content = f.read()

my_credentials = yaml.load(content, Loader=yaml.FullLoader)

databaseId = my_credentials["database"]

def create_notion_object(schedule):
    pages = []

    for day in schedule:
        dates = parse_date(day)

        page = {
            "parent": {
                "database_id": databaseId
            },
            "properties": {
                "Entrada" : {
                    "type": "date",
                    "date": {
                        "start": dates["start_date"] + "-03:00",
                        "end": None,
                    }
                },
                "Salida" : {
                    "type": "date",
                    "date": {
                        "start": dates["end_date"] + "-03:00",
                        "end": None,
                    }
                },
                "Nombre":{
                    "id":"title",
                    "type":"title",
                    "title": [{
                          "type":"text",
                          "text": {
                              "content":"Turno en McDonalds",
                              "link": None
                          },
                          "plain_text":"Turno en McDonalds",
                          "href": None
                      }]
                }
            }
        }

        pages.append(page)
    
    return pages