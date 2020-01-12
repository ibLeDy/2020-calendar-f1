import datetime

from ics import Calendar
from ics import Event
from ics.parse import ContentLine


def get_dates(gp):
    phases = ['FP1', 'FP2', 'FP3', 'Q', 'R']
    dates = {}

    for i, phase in enumerate(schedule[gp]):
        splitted = phase.split('_')
        if len(splitted) > 1:
            start = get_date(splitted[0])
            end = get_date(splitted[1])
            dates[phases[i]] = (start, end)
        else:
            dates[phases[i]] = get_date(phase)

    return dates


def get_date(phase):
    date, time = phase.split()
    date = [int(i) for i in date.split(':')]
    time = [int(i) for i in time.split(':')]
    return datetime.datetime(*date, *time)


calendar = Calendar()
calendar.extra.extend([
    ContentLine(name='X-ORIGINAL-URL', value='https://github.com/ibLeDy/2020-calendar-f1'),
    ContentLine(name='X-WR-CALNAME', value='F1 Calendar 2020')
])

with open('data/races.csv', 'r') as f:
    races = f.read().strip().splitlines()


with open('data/schedule.csv', 'r') as f:
    sessions = f.read().strip().splitlines()

schedule = {}
for s in sessions:
    name, fp1, fp2, fp3, q, r = s.split(',')
    schedule[name] = [fp1, fp2, fp3, q, r]


for race in races:
    event = Event()
    today = datetime.datetime.now()
    gp, circuit, coords, name = race.split(',')
    if gp != 'JAPAN':
        dates = get_dates(gp)

        event.name = f'{name} Grand Prix'
        event.begin = dates['R']
        # event.end = ''
        event.location = circuit
        event.geo = [float(i) for i in coords.split()]
        event.transparent = False
        event.created = today
        event.last_modified = today
        event.extra.extend([ContentLine(name='SEQUENCE', value='0')])
    else:
        event.name = f'{name} Grand Prix'
        event.begin = '2020-10-11 00:00:00'
        # event.end = ''
        event.location = circuit
        event.geo = [float(i) for i in coords.split()]
        event.transparent = False
        event.created = today
        event.last_modified = today
        event.extra.extend([ContentLine(name='SEQUENCE', value='0')])

    calendar.events.add(event)
    print(f'Added {event.name !r} to calendar')


with open('calendar.ics', 'w') as f:
    f.writelines(calendar)

print('Wrote calendar')

# NOTE: Recommendation: Import the file to a new calendar in Google Calendar
# TODO: calculate FP1, FP2, FP3, Q

# NOTE: Monaco: Free Practice 1 and 2 take place on Thursday in Monaco, with FP3 on Saturday. At all other rounds, FP1 and 2 are on Friday
# NOTE: Hungary: FP1 and FP2 are the 31st of July, FP3 and Q 1st of August
# NOTE: Japan: Times will be confirmed in the next few weeks
# NOTE: Mexico: FP2 and FP3 are the 31st of October, Race is the 1st if November
