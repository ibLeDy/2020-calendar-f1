from ics import Calendar
from ics import Event
from ics.parse import ContentLine

from translations import months, locations, coordinates


calendar = Calendar()

calendar.creator = 'bLeDy'
calendar.extra.extend([
    ContentLine(name="X-ORIGINAL-URL", value="https://github.com/ibLeDy"),
    ContentLine(name="X-WR-CALNAME", value="F1 Calendar 2020")
])

with open('calendar.csv', 'r') as f:
    races = f.read().strip().splitlines()

# TODO: calculate FP1, FP2, FP3, Q
for race in races:
    event = Event()
    number, date, gp, location = race.split(',')

    splitted_location = location.split('-')
    if len(splitted_location) > 1:
        if location != 'Spa-Francorchamps':
            location = ' '.join(splitted_location)

    day, month = date.split('-')
    if int(day) < 10:
        day = f'0{day}'

    event.name = f'{locations[gp]} Grand Prix'
    event.begin = f'2020-{months[month]}-{day} 00:00:00'
    event.location = location
    event.geo = coordinates[location]

    calendar.events.add(event)
    print(f'Added {event.name !r} to calendar')


with open('calendar.ics', 'w') as f:
    f.writelines(calendar)

print('Wrote calendar')
