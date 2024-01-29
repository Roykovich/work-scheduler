# Work email scheduler

A simple script that reads an email inbox. 

Search mails from an specific recipient and extracts the schedule for the shift of the next week with a regular expression.

## Installation
First create a virtual environment
```
python3 -m venv email
```
Then you need to install python packages for gmail
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
After the installation of the require packages you will need to generate a credentials in order to access your gmail account. That's gonna happen when you first start the script and will ask you to log in a link and you will need to store the credentials in a file called `token.json`.

After all that you should be good to go :)



### ToDos

- [x] Add relations in the script with to the payments database
- [x] Make the script make a relation and add it to the first payment view or the secon payment view. this depends if the entrance day is after or before 15 day of month
- [x] Make a script that checks if the current page is on the current month or not. If not procede to update and delete the relation property.
- [x] Make the above happen when the main scripts is executed in half or more days in the month
- [x] Add colours if the shift is opening, middle, closing or night (opening = 07:00am to 18:30pm, middle 11:30am to 22:00pm, closing 15:30 to 01:00am and night 20:30pm to 07:00am)
- [ ] Create a property that will have the amount of money that I will gain in that shift (including bonuses, licenses, holidays and all that shit)
- [ ] Make a module that calculates the payment days, 5 working days afther 15 day of the month and the last day (maybe with a dict that has the chilean holidays to avoid counting those days)
- [ ] When the pay script is done, add that day to the calendar with the aproximate payment amount (maybe with a relation property?)
- [ ] Add instrunctions to README
