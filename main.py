from math import *
import matplotlib.pyplot as plt

# Partie Léopold
base = [] 
def creation_base(nom_fichier):
    """
    Crée une base de données à partir d'un fichier contenant des informations sur les points de suivi (trkpt) du trajet Fameck-Florange.

    Entrée :
        nom_fichier (str): Le nom du fichier contenant les données.

    Sortie:
        base: Une liste contenant les informations de latitude, longitude et altitude pour chaque point de suivi.

    """
    global base # Liste pour stocker les points de suivi
    
    with open(nom_fichier, 'r') as f:
        contenu = f.read()
        trkpts = contenu.split('<trkpt ')[1:]

        for trkpt in trkpts:
            # Extraction de la latitude
            latitude_start = trkpt.find('lat="') + len('lat="')
            latitude_end = trkpt.find('"', latitude_start)
            latitude = float(trkpt[latitude_start:latitude_end])

            # Extraction de la longitude
            longitude_start = trkpt.find('lon="') + len('lon="')
            longitude_end = trkpt.find('"', longitude_start)
            longitude = float(trkpt[longitude_start:longitude_end])

            # Extraction de l'altitude
            altitude_start = trkpt.find('<ele>') + len('<ele>')
            altitude_end = trkpt.find('</ele>', altitude_start)
            altitude = float(trkpt[altitude_start:altitude_end])

            # Ajout des coordonnées à la base de données
            base.append([latitude, longitude, altitude])

    return base
base = creation_base("Fameck-Florange.gpx")
def denivele_cumule_positif():
    """
    Calcule le dénivelé cumulé positif à partir d'une base de données de points de suivi.

    Entrée :
        base (list): Une liste contenant les informations de latitude, longitude et altitude pour chaque point de suivi.

    Sortie :
        float: Le dénivelé cumulé positif.
    """
    global base
    cumule = []  # Liste pour stocker les dénivelés positifs
    somme = 0  # Variable pour stocker la somme cumulée des dénivelés positifs

    # Parcourir les points de suivi dans la base de données
    for i in range(len(base) - 1):
        if base[i][2] < base[i + 1][2]: # Vérifier si l'altitude du point suivant est supérieure à celle du point actuel
            diff = base[i + 1][2] - base[i][2] # Calculer la différence d'altitude entre les deux points
            cumule.append(diff) # Ajouter la différence d'altitude à la liste cumule
            somme = sum(cumule) # Mettre à jour la somme cumulée des dénivelés positifs

    return somme

def distance_oiseau():
    """
    Calcule la distance totale entre les points d'une base de données de suivi.

    Entrée :
        Aucune

    Sortie :
        float: La distance totale entre les points.

    """
    global base
    d_fini = 0  # Variable pour stocker la distance totale

    # Parcourir les points de suivi dans la base de données
    for i in range(len(base) - 1):
        # Coordonnées du point A
        lat_A = radians(float(base[i][0]))
        lon_A = radians(float(base[i][1]))

        # Coordonnées du point B
        lat_B = radians(float(base[i+1][0]))
        lon_B = radians(float(base[i+1][1]))

        # Calcul de la distance entre les points A et B
        d = 6371 * acos(sin(lat_A) * sin(lat_B) + cos(lat_A) * cos(lat_B) * cos(lon_B - lon_A))
        
        # Ajouter la distance à la distance totale
        d_fini += d

    return d_fini


# Partie Romain 
def graphique_altitude1():
    """
    Cette fonction extrait les altitudes à partir d'un tableau de points d'acheminement entre les points A et B,
    puis crée un graphique pour visualiser l'évolution du dénivelé en fonction des points.

    Sortie :
        Fenêtre graphique 
    """
    global base
    # Tableau des points d'acheminement entre les points A et B
    altitudes = [point[2] for point in base]  # Extraire les altitudes du tableau

    # Création du graphique
    plt.plot(altitudes)
    plt.xlabel('Point')
    plt.ylabel('Altitude (m)')
    plt.title("Évolution du dénivelé point par point")
    plt.show()

def graphique_altitude2():
    """
    Cette fonction calcule les altitudes par rapport au point de départ à partir d'un tableau de points d'acheminement entre les points A et B.
    En utilisant les indices des points, elle représente la distance parcourue et les altitudes dans un graphique.
    
    Sortie :
        Fenêtre graphique 
    """
    global base
   
    longitudes = [0] # On initialise une liste vide pour les abscisses, qui commence à 0 pour la première valeur
    distance_totale = 0 # On initialise la distance totale à parcourir
    
    for i in range(len(base) - 1):
        # Coordonnées du point A
        lat_A = radians(float(base[i][0]))
        lon_A = radians(float(base[i][1]))

        # Coordonnées du point B
        lat_B = radians(float(base[i+1][0]))
        lon_B = radians(float(base[i+1][1]))

        # Calcul de la distance entre les points A et B
        d = 6371 * acos(sin(lat_A) * sin(lat_B) + cos(lat_A) * cos(lat_B) * cos(lon_B - lon_A))
        
        # Ajouter la distance à la distance totale
        distance_totale += d

        longitudes.append(distance_totale)

    altitudes = []  # Liste des altitudes par rapport au point de départ
    altitude_depart = base[0][2]  # Altitude du point de départ

    # Calcul des altitudes
    for point in base:
        altitude_relative = point[2] - altitude_depart
        altitudes.append(altitude_relative)

    # Création du graphique 
    plt.plot(longitudes, altitudes)
    plt.xlabel('Distance réelles (km)')
    plt.ylabel('Altitude (m)')
    plt.title('Évolution du dénivelé')
    plt.show()

def graphique_carte():
    """
    Cette fonction extrait les latitudes et longitudes à partir d'un tableau de points d'acheminement entre les points A et B.
    Elle crée ensuite un graphique représentant le trajet sur une carte en utilisant les latitudes et longitudes.
    
    Sortie :
        Fenêtre graphique 
    """
    global base
    latitudes = [point[0] for point in base]  # Extraire les latitudes du tableau
    longitudes = [point[1] for point in base]  # Extraire les longitudes du tableau

    # Création du graphique de carte
    styles = ['-', '--', ':', '-.', '-', '--', ':']  # Liste des styles de ligne
    couleurs = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'black']  # Liste des couleurs

    # Création du graphique de carte avec des styles de ligne et des couleurs différents pour chaque point
    for i in range(len(latitudes) - 1):
        plt.plot([longitudes[i], longitudes[i+1]], [latitudes[i], latitudes[i+1]], linestyle=styles[i], color=couleurs[i])
    
    # Création du graphique d'altitude
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title("Trajet sur la carte")
    plt.show()
 
print(graphique_carte())