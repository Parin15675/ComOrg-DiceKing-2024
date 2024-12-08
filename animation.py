import os
import pygame
from PIL import Image




# Download animation from the folder
def load_frames_from_folder(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            frame_path = os.path.join(folder_path, filename)
            frame = pygame.image.load(frame_path).convert_alpha()
            frames.append(frame)
    return frames