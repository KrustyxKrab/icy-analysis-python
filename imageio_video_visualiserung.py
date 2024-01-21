import os
import imageio
import glob
import cv2
from tqdm import tqdm 

# Dieses Script erstellt aus einzelnen Bilder ein zusammenhängendes Video
# Dies wurde hauptsächlich mithilfe von ChatGPT geschrieben

def import_folder():
    # Eingabeordner 
    # !!! Absoluter Pfad muss angepasst werden !!! #
    folder_path = '/User/path/output/'

    # Sicherstellen, dass der Eingabeordner existiert und auch ein Ordner ist
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please enter a valid directory path.")
        return

    # Erstelle eine Liste von PNG Objekten in dem Eingabeordner
    png_files = sorted(glob.glob(os.path.join(folder_path, '*.png')))

    # Prüfen ob um Eingabeordner PNG Dateien sind
    if not png_files:
        print("No PNG files found in the specified folder.")
        return

    # Erstelle oder Suche den Ausgabeordner
    output_directory = os.path.join(folder_path, 'output_video')
    os.makedirs(output_directory, exist_ok=True)

    # Nutze Imageio um ein Video zu erstellen - Dieses Video besitzt Anfangs keine Bilder
    video_path = os.path.join(output_directory, 'amsr2_sea_ice_concentration_2012-2023.mp4')

    # FPS Anzahl - wie lange ein Bild stehen bleiben soll
    # 24 fps bedeutet: 24 Bilder in einer Sekunde, ein Bild 1/24s
    writer = imageio.get_writer(video_path, fps=24)  

    #Fortschrittsleiste mit allen PNG Dateien

    progress_bar = tqdm(png_files, desc="Processing Files", unit="file")

    # FOR Schleife um an das Video die Bilder dran zu hängen
    for png_file in progress_bar:
        img = cv2.imread(png_file)

        # Bevor die Bilder dran gehängt, Farbkodex, wenn nötig, ändern
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Anhängen der Dateien
        writer.append_data(img_rgb)

    # Schließen des "Writers"
    writer.close()

    # Ausgabebestätigung wenn das Video fertig ist (auch sichtbar an Fortschrittsdatei)
    print(f"Video created successfully at: {video_path}")

if __name__ == "__main__": # Python modul um sicher zu stellen, wenn das Script alleine ausgeführt wird (__main__), oder als Teil eines anderen Scriptes (dann Import als __name__)
    ## Funktionsaufruf ##
    import_folder() 
