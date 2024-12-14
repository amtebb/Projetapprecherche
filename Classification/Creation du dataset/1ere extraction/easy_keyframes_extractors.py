import cv2
import os
import numpy as np
import shutil
from datetime import datetime

class ImageSorter:
    def __init__(self, input_folder):
        """
        input_folder: dossier contenant les images à trier
        """
        self.input_folder = input_folder
        self.clear_folder = os.path.join(input_folder, "clear_images")
        os.makedirs(self.clear_folder, exist_ok=True)

    def calculate_blur_score(self, image_path):
        """Calcule le score de netteté d'une image"""
        image = cv2.imread(image_path)
        if image is None:
            return 0
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    def generate_stats(self, image_scores, n_keep, stats_file):
        """Génère et sauvegarde les statistiques"""
        scores = [score for _, score in image_scores]
        
        stats = [
            f"Date du tri: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Dossier source: {self.input_folder}",
            f"Nombre total d'images: {len(image_scores)}",
            f"Nombre d'images gardées: {n_keep}",
            f"Pourcentage gardé: {(n_keep/len(image_scores))*100:.1f}%",
            f"/nStatistiques des scores de netteté:",
            f"Score minimum: {min(scores):.2f}",
            f"Score maximum: {max(scores):.2f}",
            f"Score moyen: {np.mean(scores):.2f}",
            f"Score médian: {np.median(scores):.2f}",
            f"Écart-type: {np.std(scores):.2f}",
            f"/nSeuil de netteté retenu: {scores[n_keep-1]:.2f}",
            f"(Les images avec un score supérieur à ce seuil ont été gardées)",
        ]
        
        # Ajouter quelques exemples d'images
        stats.append("\nExemples d'images (nom : score):")
        stats.append("\nTop 5 plus nettes:")
        for name, score in image_scores[:5]:
            stats.append(f"{name}: {score:.2f}")
        
        stats.append("\n5 plus floues:")
        for name, score in image_scores[-5:]:
            stats.append(f"{name}: {score:.2f}")

        # Sauvegarder les stats
        with open(stats_file, 'w') as f:
            f.write('\n'.join(stats))

    def sort_images(self, keep_percentage=0.4):
        """
        Trie les images en gardant les keep_percentage% les moins floues
        """
        # Liste toutes les images avec leur score
        image_scores = []
        print("Analyse des images...")
        
        for image_name in os.listdir(self.input_folder):
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(self.input_folder, image_name)
                score = self.calculate_blur_score(image_path)
                image_scores.append((image_name, score))

        # Trie par score de netteté
        image_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Calcule combien d'images garder
        n_keep = int(len(image_scores) * keep_percentage)
        
        print(f"Total images: {len(image_scores)}")
        print(f"Images à garder: {n_keep}")
        
        # Génère et sauvegarde les statistiques
        stats_file = os.path.join(self.input_folder, 'tri_stats.txt')
        self.generate_stats(image_scores, n_keep, stats_file)
        
        # Déplace les meilleures images
        for i, (image_name, score) in enumerate(image_scores):
            if i < n_keep:
                src = os.path.join(self.input_folder, image_name)
                dst = os.path.join(self.clear_folder, image_name)
                shutil.move(src, dst)

        print(f"Images nettes déplacées vers: {self.clear_folder}")
        print(f"Statistiques sauvegardées dans: {stats_file}")

