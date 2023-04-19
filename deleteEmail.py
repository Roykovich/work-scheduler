import datetime, sys, requests, json

DATENOW = datetime.datetime.now()

def delete_old_entries(database, headers, url):
  if len(sys.argv) > 1:
    delete_arg = sys.argv[1]

    if delete_arg == '-delete':
      if  DATENOW.day >= 15:
        delete_entries(database, headers, url)
      else:
        user_answer = input("We are still in the range of days 1-14 of the month. are you sure you want to delete the old entries? y/n.")
        
        while(user_answer != 'yes' or 'y' or 'no' or 'n'):
          print("Try using Yes or No") 

        if (user_answer == 'yes' or 'y'):
          delete_entries(database, headers, url)
        else:
          print("Old dates have not been deleted.")
    else:
      print("wrong delete argument given. Try instead -delete")
  else:
    return
  
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