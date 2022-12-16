import datetime 

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