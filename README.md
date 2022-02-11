# main.py

main.py is a module to create html map,
which contains closest locations of shooting sites of films.

The program is launcher from terminal and takes four parametrs:
the year of release of the films, which will be displayed on the map,
latitude and longtitude of your location, and path to the database file
(database file can be formed from locations.list file using nfc.py module)

The result of execution is html file map_of_films.html, on which are displayed:
10 or less films, closest to the entered location, the entered location itself
and number of films close to each other.

# launch example

>>> main.py 2016 49.83826 24.02324 .\locations2.list

![image](https://user-images.githubusercontent.com/91616531/153612742-7d8a80d0-d642-4890-afaa-9e10c6f2cd01.png)
