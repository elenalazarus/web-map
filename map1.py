import folium
from geopy.geocoders import ArcGIS
import html


def user_input():
    '''
    () -> (int, int)
    This function controls the user's input
    '''
    year = int(input("Please, input the year" + '\n'))
    number = int(input("Please, input the number of films" + '\n'))
    return year, number

def reading_films(path, year):
    '''
    (str, int) -> list
    This function reads the file, chooses films with the appropriate year
    and adds their names and locations into the set
    '''
    with open('locations.list.txt', "r", encoding='utf-8',
              errors='ignore') as f:
        data = f.readlines()
    data = data[15: -1]
    # Frames for reading a file
    films = set()
    for line in data:
        # Making the information clear for understanding
        line = line.strip()
        line = line.split('\t')
        if '(' in line[-1]:
            line.remove(line[-1])
        # Looking for the year
        what_year = '(' + str(year) + ')'
        if what_year in line[0]:
            line = tuple([line[0], line[-1]])
            # Add name and coordinates of the right film to the set
            films.add(line)
    films = list(films)
    return films


def do_coordinates(films):
    '''
    list -> list
    This function takes the locations of films and turn them into the
    coordinates
    '''
    all_locations = []
    for film in films:
        location = ArcGIS(timeout=10)
        place = location.geocode(film[-1])
        # Coordinates of every film
        lat = place.latitude
        lon = place.longitude
        # Add coordinates to the list
        all_locations.append([film[0], (lat, lon)])
    return all_locations


def do_map(coordinates):
    '''
    (list) -> None
    This function creates a map and add to it coordinates, names of the
    films and information about population of the Earth
    '''
    # Creating of the map
    maps = folium.Map()
    fg = folium.FeatureGroup(name="Film_map")
    for coor in coordinates:
        lat = coor[1][0]
        lon = coor[1][1]
        film = html.escape(coor[0])
        # Adding markers of films
        fg.add_child(folium.Marker(location=[lat, lon], popup=film,
                                   icon=folium.Icon()))
    fg_pp = folium.FeatureGroup(name="Population")
    # Adding colors that depends on population
    fg_pp.add_child(folium.GeoJson
                    (data=open('world.json.txt', 'r',
                               encoding='utf-8-sig').read(),
                     style_function=lambda x: {'fillColor': 'green'
                     if x['properties']['POP2005'] < 10000000 else 'orange'
                     if 10000000 <= x['properties']['POP2005'] < 20000000
                     else 'red'}))
    # Adding all stuff at the map
    maps.add_child(fg_pp)
    maps.add_child(fg)
    maps.add_child(folium.LayerControl())
    # Save a map
    maps.save("Map_1.html")


def main():
    '''
    () -> None
    This function controls the work of all functions at this program.
    This is a boss ;)
    '''
    try:
        data = user_input()
        year, number = data[0], data[1]
        films = reading_films('locations.list.txt', year)
        current_films = films[:number]
        coordinates = do_coordinates(current_films)
        do_map(coordinates)
    except:
        return 'Input the right data'


print(main())
