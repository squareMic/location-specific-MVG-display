import time

from mvg import MvgApi, TransportType

station = MvgApi.station('Böhmerwaldplatz, München')
if station:
    mvgapi = MvgApi(station['id'])
    departures_ubahn = mvgapi.departures(
        limit=3,
        offset=5,
        transport_types=[TransportType.UBAHN]
        )
    departures_bus = mvgapi.departures(
        limit=3,
        offset=5,
        transport_types=[TransportType.BUS]
        )
    print(departures_ubahn[0]["time"]/1800)
    #print(station, departures_bus)


epoch_time =  departures_ubahn[0]["time"] # Replace with your epoch time


 
 
formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch_time))
print(formatted_time)
