# Importation des modules
import pygame
import random
import os
import datetime

# Définition des constantes
Grille = 8               # Taille de la grille en nombre de cellules (8x8)
CELL_SIZE = 60              # Taille de chaque cellule en pixels (60x60)
Marge = 10                 # Espace entre les cellules en pixels
HEADER_HEIGHT = 80          # Hauteur de l'espace pour le score et l'heure
Root = Grille * (CELL_SIZE + Marge) - Marge  # Largeur de la fenêtre de jeu
SCREEN_HEIGHT = HEADER_HEIGHT + Grille * (CELL_SIZE + Marge) - Marge # Hauteur de la fenêtre de jeu
Image_direction = "icon/"         # Chemin vers le dossier contenant les images des bonbons

# Points attribués en fonction du nombre d'éléments détruits
SCORES = {3: 10 ,4: 20 ,5: 50, 6: 100}

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((Root, SCREEN_HEIGHT))  # Définir la taille de la fenêtre de jeu
pygame.display.set_caption("Candy Crush  Game")              # Définir le titre de la fenêtre de jeu

# Chargement des images de bonbons depuis le dossier ICON_PATH
def load_images():
    candy_images = {}  # Dictionnaire pour stocker les images des bonbons
    for filename in os.listdir(Image_direction):
        if filename.endswith(".png"):  # Vérifie que le fichier est une image PNG
            image_name = filename.split(".")[0]  # Extrait le nom de l'image sans extension
            image_path = os.path.join(Image_direction, filename)  # Chemin complet vers l'image
            image = pygame.image.load(image_path).convert_alpha()  # Charge l'image avec transparence
            candy_images[image_name] = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))  # Redimensionne l'image à la taille des cellules
    return candy_images  # Retourne le dictionnaire des images chargées

# Création de la grille avec des bonbons aléatoires
def create_grid():
    candy_types = list(load_images().keys())  # Liste des types de bonbons disponibles (basée sur les images chargées)
    return [[random.choice(candy_types) for _ in range(Grille)] for _ in range(Grille)]  # Crée une grille 8x8 remplie de bonbons aléatoires

# Dessin de la grille à l'écran
def draw_grid(grid, candy_images):
    for row in range(Grille):
        for col in range(Grille):
            candy_type = grid[row][col]  # Type de bonbon à la position (row, col)
            image = candy_images[candy_type]  # Récupère l'image correspondant à ce type de bonbon
            x = col * (CELL_SIZE + Marge)  # Position horizontale avec marge
            y = HEADER_HEIGHT + row * (CELL_SIZE + Marge)  # Position verticale avec marge
            screen.blit(image, (x, y))  # Affiche l'image à la position correcte sur l'écran

# Permutation de deux bonbons dans la grille
def Permute(grid, row1, col1, row2, col2):
    grid[row1][col1], grid[row2][col2] = grid[row2][col2], grid[row1][col1]  # Échange les positions de deux bonbons dans la grille

# Vérification des correspondances de bonbons
def Verification(grid):
    matches = []  # Liste pour stocker les positions des bonbons qui forment une correspondance

    # Vérification des correspondances horizontales
    for row in range(Grille):
        count = 1  # Compteur de correspondances consécutives
        for col in range(1, Grille):
            if grid[row][col] == grid[row][col - 1] and grid[row][col] is not None:  # Vérifie si les bonbons sont du même type
                count += 1  # Incrémente le compteur si les bonbons sont les mêmes
            else:
                if count >= 3:  # Si trois bonbons ou plus sont alignés, on les ajoute aux correspondances
                    for c in range(col - count, col):
                        matches.append((row, c))
                count = 1  # Réinitialise le compteur
        if count >= 3:  # Gère le cas où la correspondance se termine à la fin de la ligne
            for c in range(Grille - count, Grille):
                matches.append((row, c))

    # Vérification des correspondances verticales
    for col in range(Grille):
        count = 1  # Compteur de correspondances consécutives
        for row in range(1, Grille):
            if grid[row][col] == grid[row - 1][col] and grid[row][col] is not None:  # Vérifie si les bonbons sont du même type
                count += 1  # Incrémente le compteur si les bonbons sont les mêmes
            else:
                if count >= 3:  # Si trois bonbons ou plus sont alignés, on les ajoute aux correspondances
                    for r in range(row - count, row):
                        matches.append((r, col))
                count = 1  # Réinitialise le compteur
        if count >= 3:  # Gère le cas où la correspondance se termine à la fin de la colonne
            for r in range(Grille - count, Grille):
                matches.append((r, col))

    return matches  # Retourne la liste des correspondances trouvées

# Animation de fusion des bonbons
def Animation(grid, matches, candy_images):
    for _ in range(5):  # Répète l'animation quelques fois
        screen.fill((255, 255, 255))  # Remplit l'écran avec une couleur blanche
        draw_grid(grid, candy_images)  # Dessine la grille de bonbons

        for (row, col) in matches:  # Pour chaque bonbon dans une correspondance
            candy_type = grid[row][col]  # Type de bonbon à la position (row, col)
            if candy_type is not None:
                image = candy_images[candy_type]  # Récupère l'image du bonbon
                x = col * (CELL_SIZE + Marge)  # Position horizontale avec marge
                y = HEADER_HEIGHT + row * (CELL_SIZE + Marge)  # Position verticale avec marge
                scale = 1.2 if _ % 2 == 0 else 0.8  # Alterne la taille pour un effet de pulsation
                scaled_image = pygame.transform.scale(image, (int(CELL_SIZE * scale), int(CELL_SIZE * scale)))  # Redimensionne l'image
                offset_x = (CELL_SIZE - scaled_image.get_width()) // 2  # Centre l'image
                offset_y = (CELL_SIZE - scaled_image.get_height()) // 2  # Centre l'image
                screen.blit(scaled_image, (x + offset_x, y + offset_y))  # Affiche l'image à la position correcte sur l'écran

        pygame.display.flip()  # Met à jour l'affichage
        pygame.time.delay(100)  # Pause pour l'effet d'animation

# Traitement des correspondances trouvées
def process_matches(grid, candy_images):
    matches = Verification(grid)  # Trouve les correspondances actuelles dans la grille
    total_score = 0  # Initialisation du score total

    while matches:  # Tant qu'il y a des correspondances
        Animation(grid, matches, candy_images)  # Anime les correspondances
        points = SCORES.get(len(matches), 10)  # Calcule les points basés sur le nombre de bonbons détruits
        display_points(points, matches)  # Affiche les points gagnés
        pygame.display.flip()  # Met à jour l'affichage pour montrer les points gagnés
        pygame.time.delay(500)  # Pause pour que les points soient visibles

        for (row, col) in matches:
            grid[row][col] = None  # Supprime le bonbon en le remplaçant par None

        collapse_grid(grid)  # Réorganise la grille en faisant tomber les bonbons
        fill_empty_spaces(grid)  # Remplit les espaces vides avec de nouveaux bonbons
        total_score += points  # Ajoute les points au score total
        matches = Verification(grid)  # Vérifie à nouveau les correspondances

    return total_score  # Retourne le score cumulé pour les correspondances trouvées

# Réorganisation de la grille après la suppression des bonbons
def collapse_grid(grid):
    for col in range(Grille):
        new_col = [grid[row][col] for row in range(Grille) if grid[row][col] is not None]  # Garde uniquement les bonbons non nuls dans la colonne
        new_col = [None] * (Grille - len(new_col)) + new_col  # Ajoute des None en haut pour remplacer les espaces vides
        for row in range(Grille):
            grid[row][col] = new_col[row]  # Met à jour la colonne dans la grille

# Remplissage des espaces vides avec de nouveaux bonbons
def fill_empty_spaces(grid):
    candy_types = list(load_images().keys())  # Liste des types de bonbons disponibles
    for row in range(Grille):
        for col in range(Grille):
            if grid[row][col] is None:  # Si la cellule est vide
                grid[row][col] = random.choice(candy_types)  # Remplace par un bonbon aléatoire

# Affichage du score et de l'heure à l'écran
def display_score_and_time(score):
    font = pygame.font.Font(None, 36)  # Définit la police de caractères et la taille
    time_text = datetime.datetime.now().strftime("%H:%M:%S")  # Formate l'heure actuelle
    score_text = f"Score: {score}"  # Texte du score

    time_surface = font.render(time_text, True, (0, 0, 0))  # Crée le texte de l'heure
    score_surface = font.render(score_text, True, (0, 0, 0))  # Crée le texte du score

    screen.blit(score_surface, (5, 5))  # Affiche le score en haut à gauche de l'écran
    screen.blit(time_surface, (Root - time_surface.get_width() - 5, 5))  # Affiche l'heure en haut à droite de l'écran

# Affichage des points gagnés
def display_points(points, matches):
    font = pygame.font.Font(None, 24)  # Définit la police de caractères et la taille
    for (row, col) in matches:
        points_text = f"+{points}"  # Texte des points gagnés
        points_surface = font.render(points_text, True, (255, 0, 0))  # Crée le texte des points avec une couleur rouge
        x = col * (CELL_SIZE + Marge)  # Position horizontale avec marge
        y = HEADER_HEIGHT + row * (CELL_SIZE + Marge)  # Position verticale avec marge
        screen.blit(points_surface, (x, y))  # Affiche le texte à la position correcte sur l'écran

# Fonction principale du jeu
def main():
    clock = pygame.time.Clock()  # Crée une horloge pour contrôler la fréquence des mises à jour
    running = True  # Indicateur de boucle de jeu en cours
    grid = create_grid()  # Crée une grille initiale de bonbons
    candy_images = load_images()  # Charge les images des bonbons
    selected_bonbon = None  # Bonbon sélectionné lors du clic
    first_click = True  # Indicateur pour gérer le premier clic
    score = 0  # Initialisation du score

    while running:  # Boucle principale du jeu
        screen.fill((255, 255, 255))  # Remplit l'écran avec une couleur blanche
        draw_grid(grid, candy_images)  # Dessine la grille de bonbons
        display_score_and_time(score)  # Affiche le score et l'heure à l'écran
        pygame.display.flip()  # Met à jour l'affichage

        for event in pygame.event.get():  # Gère les événements Pygame
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                running = False  # Arrête la boucle de jeu
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Si l'utilisateur clique avec le bouton gauche de la souris
                x, y = pygame.mouse.get_pos()  # Obtient la position de la souris
                col = x // (CELL_SIZE + Marge)  # Convertit la position en colonne de la grille
                row = (y - HEADER_HEIGHT) // (CELL_SIZE + Marge)  # Convertit la position en ligne de la grille
                if row >= 0 and col >= 0 and row < Grille and col < Grille:  # Vérifie si le clic est dans la grille
                    if first_click:
                        selected_bonbon = (row, col)  # Enregistre la position du premier clic
                        first_click = False  # Passe à l'état du deuxième clic
                    else:
                        first_click = True  # Réinitialise pour le prochain cycle de clics
                        sel_row, sel_col = selected_bonbon  # Récupère la position du bonbon sélectionné
                        # Vérifie si les deux bonbons sont adjacents
                        if (row == sel_row and abs(col - sel_col) == 1) or (col == sel_col and abs(row - sel_row) == 1):
                            Permute(grid, sel_row, sel_col, row, col)  # Échange les positions des bonbons
                            score += process_matches(grid, candy_images)  # Traite les correspondances et met à jour le score

        clock.tick(30)  # Contrôle la fréquence d'images (30 FPS)

    pygame.quit()  # Ferme proprement Pygame


main()  # Exécute la fonction principale si le script est exécuté directement

