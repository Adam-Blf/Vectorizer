import cv2
import numpy as np
import pyautogui
import time
import os

# --- SÉCURITÉ ---
# Si tu coinces la souris dans un coin de l'écran, le script s'arrête immédiatement.
# SUR UN DELL AVEC TOUCHPAD : Si tu n'y arrives pas, fais CTRL+C dans le terminal.
pyautogui.FAILSAFE = True 
# Temps de pause entre chaque mouvement (0.0 pour aller le plus vite possible)
pyautogui.PAUSE = 0.005 

def draw_image_on_screen(image_path, scale_factor=0.4):
    """
    Lit une image, détecte les contours, et prend le contrôle de la souris
    pour les dessiner à l'écran.
    """
    
    if not os.path.exists(image_path):
        print(f"Erreur: Image '{image_path}' introuvable.")
        return

    # Info système pour vérifier la compatibilité
    screen_w, screen_h = pyautogui.size()
    print(f"INFO: Résolution d'écran détectée sur ton Dell : {screen_w}x{screen_h}")

    # 1. Chargement et Traitement
    print("Chargement de l'image...")
    img = cv2.imread(image_path)
    
    if img is None:
        print("Erreur: Impossible de lire l'image. Vérifie le nom du fichier.")
        return

    # Redimensionner l'image
    # Sur un écran de portable, on réduit souvent un peu plus
    width = int(img.shape[1] * scale_factor)
    height = int(img.shape[0] * scale_factor)
    img = cv2.resize(img, (width, height))
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    print(f"{len(contours)} traits détectés.")
    print("---------------------------------------------------")
    print("!!! PRÊT À DESSINER !!!")
    print("1. Ouvre Affinity Designer (ou Paint)")
    print("2. Sélectionne le PINCEAU (couleur noire)")
    print("3. Mets ta souris là où tu veux COMMENCER le dessin (coin haut-gauche)")
    print("---------------------------------------------------")

    # Compte à rebours
    for i in range(5, 0, -1):
        print(f"Le robot prend le contrôle dans {i}...")
        time.sleep(1)

    print(">>> DESSIN EN COURS <<<")
    print("Pour arrêter d'urgence : Place la souris TRÈS VITE dans un coin de l'écran.")
    
    start_x, start_y = pyautogui.position()
    pyautogui.PAUSE = 0 

    for contour in contours:
        if cv2.contourArea(contour) < 20:
            continue
            
        epsilon = 0.005 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        points = approx.reshape(-1, 2)
        
        if len(points) > 0:
            # On vérifie que le point ne sort pas de l'écran (sécurité supplémentaire)
            first_x = start_x + points[0][0]
            first_y = start_y + points[0][1]
            
            if first_x >= screen_w or first_y >= screen_h:
                continue # On saute ce trait s'il sort de l'écran

            pyautogui.mouseUp()
            pyautogui.moveTo(first_x, first_y)
            pyautogui.mouseDown()
            
            for x, y in points[1:]:
                target_x = start_x + x
                target_y = start_y + y
                pyautogui.moveTo(target_x, target_y)
            
            pyautogui.mouseUp()
            time.sleep(0.01)

    print("Terminé ! N'oublie pas d'enregistrer ton travail sur Affinity.")

if __name__ == "__main__":
    # Nom exact de ton image
    INPUT_FILE = "Gemini_Generated_Image_ftladiftladiftla.jpg"
    
    # ÉCHELLE : 
    # 0.3 ou 0.4 est bien pour un écran de pc portable Dell standard (13-15 pouces)
    # Si c'est trop gros, mets 0.2
    SCALE = 0.4 
    
    draw_image_on_screen(INPUT_FILE, SCALE)