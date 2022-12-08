import datetime 
from gmail import parse_date

# def create_calculations_v1(schedule):
#   calculations = {
#     "total-diurno": 0,
#     "total-nocturno": 0,
#     "hours": []
#   }

#   for day in schedule:
#     parsed = parse_date(day)

#     hours = {
#       "diurno": 0,
#       "nocturno": 0
#     }

#     parsed["start_date"] += datetime.timedelta(minutes=30)

#     while parsed["start_date"] < parsed["end_date"]:

#       if (6 <= parsed["start_date"].hour < 22):
#         calculations["total-diurno"] += 1
#         hours["diurno"] += 1
#       else:
#         calculations["total-nocturno"] += 1
#         hours["nocturno"] += 1

#       parsed["start_date"] += datetime.timedelta(hours=1)

#     calculations["hours"].append(hours)
  
#   print(calculations)

def create_calculations(date):
  if type(date) is list: return
  
  new_dict = dict(date)

  calculations = {
    "total-diurno": 0,
    "total-nocturno": 0,
  }
  new_dict["start_date"] += datetime.timedelta(minutes=30)

  while new_dict["start_date"] < new_dict["end_date"]:
    if (6 <= new_dict["start_date"].hour < 22):
      calculations["total-diurno"] += 1
    else:
      calculations["total-nocturno"] += 1

    new_dict["start_date"] += datetime.timedelta(hours=1)

  return calculations