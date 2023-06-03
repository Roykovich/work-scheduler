# Importing libraries
import imaplib, yaml, re, datetime
import os.path

# Regex string to parse the email content that I want
REGEX = "(lunes|martes|mi=C3=A9rcoles|jueves|viernes|s=C3=A1bado|domingo), (\d+) de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre) de (2022|2023|2024) (\d{1,2}:\d{1,2}) - (\d{1,2}:\d{1,2}), (\w*)"
# The IMAP URL I'm going to use
IMAP_URL = 'imap.gmail.com'
# Month object to identify the months as numbers to parse the later with datetime
MONTHS = {
    'enero': {
        'month': 1,
        'endMonth': 31 
        },
    'febrero': {
        'month': 2,
        'endMonth': 28
        },
    'marzo': {
        'month': 3,
        'endMonth': 31
        },
    'abril': {
        'month': 4,
        'endMonth': 30
        },
    'mayo': {
        'month': 5,
        'endMonth': 31
        },
    'junio': {
        'month': 6,
        'endMonth': 30
        },
    'julio': {
        'month': 7,
        'endMonth': 31
        },
    'agosto': {
        'month': 8,
        'endMonth': 31
        },
    'septiembre': {
        'month': 9,
        'endMonth': 30
        },
    'octubre': {
        'month': 10,
        'endMonth': 21
        },
    'noviembre': {
        'month': 11,
        'endMonth': 30
        },
    'diciembre': {
        'month': 12,
        'endMonth': 31
    }
}
# Google calendar colors id
EVENT_COLORS_ID = [
    '1', # blue
    '2', # green
    '3' # purple
    '4' # re
    '5' # yellow
    '6' # orange
    '7' # turquoise
    '8' # gray
    '9' # bold blue
    '10' # bold gree
    '11'  #bold red
]

# We check first
if os.path.exists('credentials.yml'):
    with open("credentials.yml") as f:
        content = f.read()
    
# from credentials.yml import user name and password
my_credentials = yaml.load(content, Loader=yaml.FullLoader)

# Load the user name and passwd from yaml file
user, password, correo = my_credentials["user"], my_credentials["password"], my_credentials["email"]

# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

# Function to search for a key value pair
def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data # the type return is bytes

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
                day = parsed[0]
                
                # We filter both of this strings 
                if (parsed[0] == "mi=C3=A9rcoles"):
                    day = "miércoles"

                if (parsed[0] == "s=C3=A1bado"):
                    day = "sábado"

                schedule.append(
                    [
                        "{} {}".format(day, parsed[1]), 
                        parsed[2], 
                        parsed[4], 
                        parsed[5], 
                        parsed[6],
                        parsed[3], # Month thats going to be sustracted
                        parsed[1]  # Day thats going to be sustracted
                    ]
                )

            return schedule

        except UnicodeEncodeError as e:
            pass

def parse_date(day):
    dates = {
        "start_date": None,
        "end_date": None
    }

    # We parse the hours in mm:ss style for datetime
    entrance = re.findall('(\d+):(\d+)', day[2])
    clockout = re.findall('(\d+):(\d+)', day[3])
    
    start_date = datetime.datetime(int(day[5]), MONTHS[day[1]]['month'], int(day[6]), int(entrance[0][0]), int(entrance[0][1]), 0)
    # With this condition flow we can check if the clockout is in the other
    # day
    if int(clockout[0][0]) < int(entrance[0][0]):
        if end_of_month(day[1], day[6]):
            end_date = datetime.datetime(int(day[5]), MONTHS[day[1]]['month'] + 1, 1, int(clockout[0][0]), int(clockout[0][1]), 0)
        else:    
            end_date = datetime.datetime(int(day[5]), MONTHS[day[1]]['month'], int(day[6]) + 1, int(clockout[0][0]), int(clockout[0][1]), 0)
    else:
        end_date = datetime.datetime(int(day[5]), MONTHS[day[1]]['month'], int(day[6]), int(clockout[0][0]), int(clockout[0][1]), 0)

    dates['start_date'] = start_date
    dates['end_date'] = end_date

    return dates

def create_events_object(schedule):
    events = []

    for day in schedule:

        dates = parse_date(day)
        entrance = dates['start_date'].hour
        clockout = dates['end_date'].hour
        summary = None
        colorID = None
        
        if entrance >= 11 and clockout == 22: # Medium
            colorID = '11'
            summary = "Turno medio"
        elif entrance >= 15 and clockout == 1: # closing
            colorID = '10'
            summary = "Turno cierre"
        elif entrance >= 20 and clockout <= 8: # Nocturnal
            colorID = '8'
            summary = "Turno nocturno"
        else:
            colorID = '1'
            summary = "Turno apertura"
        
        print(summary)
        event = {
            'summary': summary,
            'location': 'Av. las Condes 12207, Las Condes, Región Metropolitana, Chile',
            'description': 'Estas posicionado como %s' % day[4],
            'start': {
                'dateTime': dates["start_date"].isoformat("T"),
                'timeZone': 'America/Santiago',
            },
            'end': {
                'dateTime': dates["end_date"].isoformat("T"),
                'timeZone': 'America/Santiago',
            },
            'colorId': colorID,
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

        archive_email()

        return schedule
    else:
        print('No email found.')
        return False

def archive_email():
    # This two lines are used to archive the email
    con.store(message_set[0], '+FLAGS', '\\Deleted')
    con.expunge()

def end_of_month(month, day):
    end_day = MONTHS[month]['endMonth']
    next_day = int(day) + 1
    return end_day < next_day


con = imaplib.IMAP4_SSL(IMAP_URL)

con.login(user, password)

con.select('Inbox')

message_set = search('FROM', correo, con)
msgs = get_emails(message_set)
