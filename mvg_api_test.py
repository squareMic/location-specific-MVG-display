import requests
import datetime

# Deaktiviere SSL-Zertifikatsprüfung für Testzwecke
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class MvgApiWrapper:
    def __init__(self):
        self.base_url = 'https://www.mvg.de/api/fib/v2'

    def get_station(self, query):
        response = requests.get(f"{self.base_url}/location?query={query}", verify=False)
        response.raise_for_status()
        return response.json()

    def get_departures(self, station_id):
        response = requests.get(f"{self.base_url}/departure?globalId={station_id}", verify=False)
        response.raise_for_status()
        return response.json()

def calculate_time_difference(timestamp):
    current_time = datetime.datetime.now().timestamp() * 1000
    difference_in_minutes = (timestamp - current_time) / 60000
    return round(difference_in_minutes)

def filter_departures_by_line_and_destination(departures, transport_type, label, destination):
    return [departure for departure in departures if departure['transportType'] == transport_type and departure['label'] == label and departure['destination'] == destination]

def get_next_departures(departures, count=3):
    departures_sorted = sorted(departures, key=lambda x: x['plannedDepartureTime'])
    return departures_sorted[:count]

def format_station_name(name, length=14):
    if len(name) > length:
        return name[:length]
    else:
        return name.ljust(length)

try:
    mvgapi_wrapper = MvgApiWrapper()
    stations = mvgapi_wrapper.get_station('Böhmerwaldplatz, München')
    station = next((s for s in stations if s['name'] == 'Böhmerwaldplatz' and s['place'] == 'München'), None)
    if station:
        try:
            departures = mvgapi_wrapper.get_departures(station['globalId'])
            formatted_station_name = format_station_name(station['name'])
            #print(f"Station: {formatted_station_name}:")
            #print("Alle Abfahrten:")
            for departure in departures:
                planned_diff = calculate_time_difference(departure['plannedDepartureTime'])
                realtime_diff = calculate_time_difference(departure['realtimeDepartureTime'])
                delay = departure.get('delayInMinutes', 0)
                transport_type = departure['transportType']
                label = departure['label']
                destination = departure['destination']
            #    print(f"{transport_type:<6} {label:<4} nach {destination:<20} geplant in {planned_diff:>2} Minuten, echt in {realtime_diff:>2} Minuten, Verspätung {delay} Minuten")

            # Ziele für U4 und Bus 59
            u4_destinations = ['Theresienwiese', 'Arabellapark']
            bus59_destinations = ['Ackermannbogen', 'Giesing Bf.']

            # Nächste 3 Abfahrten für jede Richtung der U4
            for destination in u4_destinations:
                u4_departures = filter_departures_by_line_and_destination(departures, 'UBAHN', 'U4', destination)
                next_u4_departures = get_next_departures(u4_departures, 2)
                #print(f"\nNächste 3 Abfahrten (U4 nach {destination}):")
                for departure in next_u4_departures:
                    planned_diff = calculate_time_difference(departure['plannedDepartureTime'])
                    realtime_diff = calculate_time_difference(departure['realtimeDepartureTime'])
                    delay = departure.get('delayInMinutes', 0)
                    transport_type = departure['transportType']
                    label = departure['label']
                    destination = departure['destination']
                    print(f"{label:<3} {destination:<15} {realtime_diff:>2} min (+{delay})")

                if not next_u4_departures:
                    print(f"Keine Abfahrten für U4 nach {destination} gefunden.")

            # Nächste 3 Abfahrten für jede Richtung des Bus 59
            for destination in bus59_destinations:
                bus59_departures = filter_departures_by_line_and_destination(departures, 'BUS', '59', destination)
                next_bus59_departures = get_next_departures(bus59_departures, 2)
                #print(f"\nNächste 3 Abfahrten (Bus 59 nach {destination}):")
                for departure in next_bus59_departures:
                    planned_diff = calculate_time_difference(departure['plannedDepartureTime'])
                    realtime_diff = calculate_time_difference(departure['realtimeDepartureTime'])
                    delay = departure.get('delayInMinutes', 0)
                    transport_type = departure['transportType']
                    label = departure['label']
                    destination = departure['destination']
                    print(f"{label:<3} {destination:<15} {realtime_diff:>2} min (+{delay})")

                if not next_bus59_departures:
                    print(f"Keine Abfahrten für Bus 59 nach {destination} gefunden.")

        except Exception as e:
            print(f"Fehler beim Abrufen der Abfahrten: {e}")
    else:
        print("Station nicht gefunden.")
except Exception as e:
    print(f"Fehler beim Abrufen der Station: {e}")
