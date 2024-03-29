import datetime, sys, requests, json

DATENOW = datetime.datetime.now()
AFFFIRMATIVE = ['yes', 'yeah', 'y']
NEGATIVE = ['no', 'nope', 'n']

def delete_old_entries(database, headers, url):
  if len(sys.argv) < 2: return
  
  delete_arg = sys.argv[1]

  if delete_arg != '-delete':
    print("wrong delete argument given. Try instead -delete")

  if DATENOW.day < 27:
    while True:
      user_answer = input("We are still in the range of days 1-14 of the month. are you sure you want to delete the old entries? [y/n].")

      if user_answer.lower() in AFFFIRMATIVE:
        delete_entries(database, headers, url)
        return
      elif user_answer.lower() in NEGATIVE:
        print("Alright, old entries won't be deleted.")
        return
      else:
        print("Try using Yes or No")

  delete_entries(database, headers, url)
      
  
def delete_entries(database, headers, url):
  print("Deleting old entries.")

  database_response = requests.request("POST", database, headers=headers)
  res_data = database_response.json()
  results_array = res_data["results"]

  for result in results_array:
    entry_date = result["properties"]["Entrada"]["date"]["start"]
    parsed_entrydate = datetime.datetime.fromisoformat(entry_date)
    entry_id = result["id"]

    if parsed_entrydate.strftime("%B") != DATENOW.strftime("%B"):
      result["properties"]["Relation"]["relation"] = []
      new_dump = json.dumps(result)
      delete_response = requests.request("PATCH", f"{url}/{entry_id}", headers=headers, data=new_dump)

  print("old entries deleted sucessfully.")