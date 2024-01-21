import os
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from tqdm import tqdm 

# Import aller Bibliotheken

# CRYOSAT - 2 amsr2 Meereiskonzentration Visualisierung
# Diese Anwendung ist spezifisch für die Daten unter folgendem Link angepasst: https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/n6250/netcdf/

# Bevor die Anwendung auf den Datensatz angepasst wurde, wurde die Datei mithilfe eines kleines Hilfscript ausgelesen. (data_view.py)
# Mithilfe dieser kleinen Anwenung wurden die Variablen sowie die Projektionsdetails ausgelesen und danach in dieses Script eingebettet. 

# Zusammenfassung der Funktionsweise:
# Die Anwendung bekommt als Eingabeordner ein Jahr zugeordnet, listet alle Daten aus diesem Ordner auf und analysiert diese einzeln daraufhin. 
# Die Analyse besteht darin, dass alle Datenpunkte, die sog. Projektion sowie die Karte durch Cartopy dargestellt werden. 
# Danach wird die Datei in dem Ausgabeordner abgespeichert und korrekt benannt. 

# Erroranalyse wurde mithilfe von ChatGPT vorgenommen, so wie manche anderen Effektivitätsverbesserungen 


def plot_data(folder_path, output_folder, projection):
    
    # Die Anwendung nimmt hier alle Dateien aus dem Eingabeordner die mit der Formatendung .nc enden. Die Endung .nc steht für netCDF

    nc_files = [file for file in os.listdir(folder_path) if file.endswith('.nc')]

    # Nutzung einer Fortschrittsleiste mithilfe der Bibliothek tqdm. Sehr einfache Nutzung durch Einbau in die for - Schleife
    # Alle Dateien die in die For - Schleife laufen werden erst in der Fortschrittsleiste gespeichert, dadurch erkennt die Bibliothek wieviele Dateien schon bearbeitet und wieviel noch kommen. 

    progress_bar = tqdm(nc_files, desc="Rendering Projection Files", unit="file")

    # For - Schleife durch alle Dateien in der Fortschrittsleiste

    for nc_file in progress_bar:

        # Lesen der netCDF Datei aus dem Eingabeordner (folder_path) und der spezifischen Datei (nc_file)
        # Speichern der gelesenen Datei als 'ds'

        with nc.Dataset(os.path.join(folder_path, nc_file), 'r') as ds:
            
            # Entnahme der Variablen aus der netCDF Datei (x - Koordinate, y - Koordinate und z - Wert (Meereiskonzentration))

            x_values = ds.variables['x'][:]
            y_values = ds.variables['y'][:]
            z_values = ds.variables['z'][:]

            # Anpassung der z - Werte: In dem vorliegenden Datensatz werden die Landflächen mit einem z - Wert von 127 gekenntzeichnet.
            # Durch diese Darstellung können wir allerdings keine Cartopy Karte drüber legen, ohne dass wir Probleme mit der sog. Z- Ordnung bekommen. 
            # Die Z Ordnung wird an gegebener Stelle noch einmal erklärt. 
            # Hier werden alle Werte die größer als 100 (maximaler Wert von % -> Meereiskonzentartion kann maximal 100% sein) ignoriert, wodurch man die Karte im Hintergrund der Projektion später erkennen kann.
            # Alle Werte von z können nur zwischen 0 - 100 sein. Dadurch gehen wir sicher, dass es sich nur um den richtigen Prozentwertbereich handelt. 

            z_values = np.where(z_values > 100, np.nan, z_values)
            z_values = np.clip(z_values, 0, 100)

            # Einlesen der Variable 'polar_stereographic'
            # In dieser Variable sind alle wichtigen Werte für eine korrekte Darstellung der Karte gespeichert 

            grid_mapping = ds.variables['polar_stereographic'] 

            # Folgende Werte liegen in der Variable 'polar_stereographic':

            central_longitude = grid_mapping.straight_vertical_longitude_from_pole
            false_easting = grid_mapping.false_easting # Darstellung für ArcGis
            false_northing = grid_mapping.false_northing # Darstellung für ArcGis
            latitude_of_projection_origin = grid_mapping.latitude_of_projection_origin

            # Dieser Teil kann theoretisch ignoriert werden, da die Werte für false_northing & false_easting nicht mit Cartopy dargestellt werden können 
            # und zudem auch 0 betragen, also ignoriert werden können. Allerdings wäre dies wichtig für ein allgemeinen Ansatz für ein Datenverarbeitungsprogramm, welches ArcGis Daten verarbeiten kann 
            # (Projekt für einen anderen Zeitlichen Rahmen)

            projection_params = {
                'central_longitude': central_longitude,
                'false_easting': false_easting,
                'false_northing': false_northing,
                'latitude_of_projection_origin': latitude_of_projection_origin,
            }

            # Definieren der Datenprojektion. ccrs ist Cartopy (Oben als als ccrs importiert)
            # Hier habe ich ein Problem in der Datendarstellung gefunden: 
                # Der Wert für die Skalierung beträgt laut der dateneignenen Projektionsvariable 1. Allerdings hat man, bei dem Faktor 1 eine Verschiebung von Karte und Datenprojektion erkennen können.
                # Den Wert habe ich daraufhin durch ausprobieren angepasst.

            projection = ccrs.Stereographic(central_longitude=central_longitude,
                                            central_latitude=latitude_of_projection_origin,
                                            false_easting=0,
                                            false_northing=0,
                                            scale_factor=0.97)

            # Dies ist ein Herzstück der Anwendung. Hier wird die Darstellung mithilfe der Matplot Bibliothek initalisiert. Allerdings werden hier nur die gurndlegenden Darstellung, noch ohne Daten und Karte erzeugt, worauf dann die anderen Projektionen basieren.  

            fig, ax = plt.subplots(subplot_kw={'projection': projection}, figsize=(12, 8))

            # In der folgenden Zeile wird ein sog. Meshgrid erzeugt. Das bedeutet, dass aus den x & y Daten ein Koordinaten System erstellt wird.
            # Dieses Koordinaten System funktioniet genau wie ein Koordinatensystem in dem Graphen dargestellt werden. Dieses Koordinatensystem hat die Dimensionen von x und y.
            # Durch dieses Koordinatensystem kann der z - Wert eindeutig zugewiesen werden - Auf der x Achse wird der zugehörige Wert gesucht und auf der y - Achse auch. Dadurch ergibt sich ein bestimmter Punkt, zu dem der z- Wert gehört. 

            x, y = np.meshgrid(x_values, y_values)

            # Hier werden die Daten dann auf die Darstellung projiziert. 
            # Dafür sind folgende Parameter angeben: Welche Daten sollen projiziert werden? x, y und z Daten
            # in welchem Farbschema: 'blues_r' - blues reversed. Ausgesucht da Maximum weiß und Minimum Blau ist - Passend zu Meer und Eis
            # Transform gibt an, wie die Daten projiziert werden sollen. Dies soll genauso geschehen, wie im netCDF als Variable angeben ist. Wir haben ja alle Werte aus der Variable in projection gespeichert
            # Hier kommen wir jetzt auch zur Z- Order. Die Z - Ordner bestimmt auf welcher Ebene die Daten angezeigt werden. Mithilfe dieses Wertes können wir zum Beispiel sagen, dass die Karte auf den Daten liegen soll und nicht anders herum. 
            # Allerdings musstenw ir hier ein wenig tricksen: 
            # Dadurch, dass in den Daten die Landfläche mit einem Wert dargestellt wurde und nun ignoriert wurde, hat die Datenprojektion hier ein "Loch". 

            img = ax.contourf(x, y, z_values, origin='lower', cmap='Blues_r', transform=projection, zorder=2)

            # Durch dieses "Loch" in der Datenprojektion können wir die nächste Zeile überall dort sehen, wo Land ist. Dies ist eine Funktion welche in Cartopy enthalten ist:
            # Die Möglichkeit ein Bild mit verschiedenen Farben auf die Karte zu legen. Da das deutloch besser aussieht als eine einzige Farbe für das Land, haben wir das hier genutzt. 
            # Da allerdings dieses "stock_img" acuh für Wasser gilt, konnten wir nicht sagen, dass dieses einfach die höchste Z - Ordnung erhält, da man sonst unsere Datenprojektion nicht mehr gesehen hätte.

            ax.stock_img()

            # Die folgenden Zeile ist eine Liniendarstellung der Küstenlinie

            ax.add_feature(cfeature.COASTLINE, zorder=4)

            # Mit dem nächsten Abschnitt fügen wir die Linien für Längen und Breitengrade hinzu. (Dieser Teil stammt aus der Cartopy Dokumentation)

            gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                          linewidth=1, color='gray', alpha=0.5, linestyle='--')
            gl.top_labels = False
            gl.left_labels = False
            gl.xformatter = LONGITUDE_FORMATTER
            gl.yformatter = LATITUDE_FORMATTER

            # Hier fügen wir die Skala am rechten Rand der Karte hinzu und bennen diese wie gewünscht. 

            cbar = plt.colorbar(img, ax=ax, orientation='vertical')
            cbar.set_label('sea ice concentration (in %)')

            # Der folgende Abschnitt ermittelt das Datum der zu untersuchenden Datei. 
            # Wie man an den Daten erkennen kann, liegt das Datum im Format YYYYMMDD am Ende jedes Dateinamens vor:
            # Beispielname: asi-AMSR2-n6250-20120702-v5.4.nc
            # Um aus dem Namen das Datum zu extrahieren nutzen wir einfache Indexbestimmung:
            # Der Dateiname ist als String gespiechert. Dadurch können wir, wenn wir den Teil -v5.4.nc ignorieren das Datum abgreifen. 


            date = nc_file[:-8][-8:]
            print(date)

            # Wenn wir das haben, können wir ganz einfach das Datum umstellen

            day = date[6:8]
            month = date[4:6]
            year = date[0:4]
            correct_date = f'{day}.{month}.{year}'

            # Für die korrekte Darstellung, damit die Dateien innerhalb des Ordners automatisch sortiert werden, müssen wir das Datum noch einmal in die YYYY-MM-DD Schreibweise bringen.

            name_date = f'{year}-{month}-{day}'
            print(f"Processing file: {nc_file}")
            print(f"Date extracted: {day}.{month}.{year}")

            # Beschriftung der gesamten Darstellung 

            ax.set_title(f'CryoSat-2 - SEA ICE CONCENTRATION {correct_date}')

            # Benennung des Bildes
            output_path = os.path.join(output_folder, f'{name_date}sea_ice_concentration.png')
            #Speichern der Datei im Ausgabeordner mit der Auflösung von 200dpi. Der Parameter bbox_inches='tight' und close(fig) hilft dabei, dass die gesamten Bilder 
            # nicht im Arbeitsspeicher zwischengespeichert werden, sondern direkt auf dem Hauptspeicher. Ohne den Paramter ergab sich das Problem, dass die Bilder im RAM zwischen gespiechert wurden da sie nie durch close(fig) wirdklich geschlossen wurden. 
            plt.savefig(output_path, dpi=200, bbox_inches='tight')
            plt.close(fig)


## Funktionsaufruf ##
            
# Angabe aller Jahre, welche durchlaufen werden sollen
            
years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Ausgabeordner 
# !!! Absolute Pfade müssen natürlich angepasst werden !!! #

output_folder = '/User/path/output'

# For - Schleife für alle Jahre

for year in years:
    folder_path = f'User/path/input/{year}'

    # Angabe der Projektion außerhalb der For Schleife in der plot_data Funktion. Ohne diese Angabe enstand ein Error. 
    projection = None

    # Darstellung, welches Jahr das Programm gerade bearbeitet
    print(f"Processing data for {year}")

    # Funktionsaufruf

    plot_data(folder_path, output_folder, projection)

    # Mitteilung, dass das Jahr fertig bearbeitet wurde und nun das nächste bearbeitet wird.
    print(f"Year {year} completed. Moving on to the next year.")

# Ausgabe, wenn alle Jahre fertig bearbeitet wurden. 
print("All years and functions completed.")