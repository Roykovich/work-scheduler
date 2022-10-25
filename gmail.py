# Importing libraries
import imaplib, email, yaml, re, datetime
from image import draw_table
import os.path

REGEX = "(lunes|martes|mi=C3=A9rcoles|jueves|viernes|sabado|domingo), (\d+) de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre) de (2022|2023|2024) (\d{1,2}:\d{1,2}) - (\d{1,2}:\d{1,2}), (\w*)"
IMAP_URL = 'imap.gmail.com'
MONTHS = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12
}

if os.path.exists('credentials.yml'):
    with open("credentials.yml") as f:
        content = f.read()
    
# from credentials.yml import user name and password
my_credentials = yaml.load(content, Loader=yaml.FullLoader)

#Load the user name and passwd from yaml file
user, password, email = my_credentials["user"], my_credentials["password"], my_credentials["email"]

# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

# Function to search for a key value pair
def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data

# Function to get the list of emails under this label 
def get_emails(result_bytes):
    msgs = [] # all the email data are pushed into here
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)   

    return msgs

# Regex for the body
def regex_body(body):
    return re.findall(REGEX, body)

# Function that parse emails
def parse_emails(email):
    if type(email) is tuple:

        # encoding set as utf-8
        content = str(email[1], 'utf-8')
        data = str(content)

        # Handling errors related to unicode
        try: 
            indexstart = data.find("ltr")
            data2 = data[indexstart + 5: len(data)]
            indexend = data2.find("</div>")

            parsed_email = regex_body(data2[0: indexend])

            schedule = []

            # printing the required content which we need
            # to extract from our email i.e our body
            for parsed in parsed_email:
                schedule.append(["{} {}".format(
                    re.sub("mi=C3=A9rcoles", "miércoles", parsed[0]),
                     parsed[1]), 
                     parsed[2], 
                     parsed[4], 
                     parsed[5], 
                     parsed[6],
                     parsed[3], # Month thats going to be sustracted
                     parsed[1] # Day thats going to be sustracted
                    ]
                )

            return schedule

        except UnicodeEncodeError as e:
            pass

def create_events_object(schedule):
    events = []

    for day in schedule:

        entrance = re.findall('(\d+):(\d+)', day[2])
        clockout = re.findall('(\d+):(\d+)', day[3])
        
        start_date = datetime.datetime(int(day[5]), MONTHS[day[1]], int(day[6]), int(entrance[0][0]), int(entrance[0][1]), 0)
        end_date = datetime.datetime(int(day[5]), MONTHS[day[1]], int(day[6]), int(clockout[0][0]), int(clockout[0][1]), 0)

        event = {
            'summary': 'Turno',
            'location': 'Av. las Condes 12207, Las Condes, Región Metropolitana, Chile',
            'description': 'Estas posicionado como %s' % day[4],
            'start': {
                'dateTime': start_date.isoformat('T'),
                'timeZone': 'America/Santiago',
            },
            'end': {
                'dateTime': end_date.isoformat('T'),
                'timeZone': 'America/Santiago',
            },
            'colorId': '5',
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 150}
                ]
            }
        }

        events.append(event)
    
    return events
        
def create_schedule():
    if len(msgs) == 1:
        schedule = parse_emails(msgs[0][0])

        return schedule

con = imaplib.IMAP4_SSL(IMAP_URL)

con.login(user, password)

con.select('Inbox')

msgs = get_emails(search('FROM', email, con))

# for msg in msgs[::-1]:
#     for sent in msg:
#         schedule = parse_emails(sent)
#         # print(schedule)
#         draw_table(
#             schedule, 
#             HEADER, 
#             FONT, 
#             (20 * 4, 10 * 4), 
#             (10 * 4, 10 * 4), 
#             ALIGN, 
#             {}, 
#             False
#         )
