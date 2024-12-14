import cv2

def couper_retourner(video_path,output_path):
    video=cv2.VideoCapture(video_path)

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f"Impossible d'ouvrir la vidéo : {video_path}")
    else:
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))  # Largeur
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Hauteur
        fps = int(video.get(cv2.CAP_PROP_FPS))  # Frames par seconde
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # Nombre total de frames

        print(f"Caractéristiques de la vidéo : {video_path}")
        print(f"  - Résolution : {width}x{height}")
        print(f"  - FPS : {fps}")
        print(f"  - Nombre total de frames : {frame_count}")

        print("Début du recadrage et de la rotation...")

        ratio = 1.5 / 15  # Ratio de la hauteur à couper
        crop_height = int(height * ratio)
        new_height = height - crop_height

        # Initialiser le VideoWriter pour la vidéo de sortie
        out = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*'mp4v'),  # Utiliser 'mp4v' pour générer un MP4
            fps,
            (width, new_height)
        )

        # Lire et traiter les frames
        frame_index = 0
        while True:
            ret, frame = video.read()  # Lire une frame
            if not ret:  # Si plus de frames, quitter la boucle
                print("Lecture des frames terminée.")
                break

            # Découper la partie inférieure de la frame
            cropped_frame = frame[:new_height, :]

            # Appliquer une rotation de 180 degrés
            rotated_frame = cv2.rotate(cropped_frame, cv2.ROTATE_180)

            # Écrire la frame dans la vidéo de sortie
            out.write(rotated_frame)
            frame_index += 1

            # Afficher la progression
            if frame_index % 100 == 0:
                print(f"Frames traitées : {frame_index}/{frame_count}")

        # Libérer les ressources
        video.release()
        out.release()
        cv2.destroyAllWindows()

        print("Vidéo recadrée et tournée sauvegardée sous 'video_coupe.mp4'")
    print("Fin")