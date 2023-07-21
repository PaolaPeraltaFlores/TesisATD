from colorthief import ColorThief
import matplotlib.pyplot as plt
import numpy as np

class ColorAnalyzer:
    def __init__(self, file):
        self.color_thief = ColorThief(file)

    def get_color(self, quality=10):
        return self.color_thief.get_color(quality)

    def get_palette(self, color_count=10, quality=10):
        return self.color_thief.get_palette(color_count, quality)

def analyze_image(image_path):
    color_analyzer = ColorAnalyzer(image_path)

    dominant_color = color_analyzer.get_color(quality=1)
    palette = color_analyzer.get_palette(color_count=6)

    # Crear una figura y mostrar el color dominante como una imagen
    fig, ax = plt.subplots()
    color_image = np.array([[dominant_color]])
    ax.imshow(color_image)
    ax.axis('off')
    fig.savefig('colordm.jpg', bbox_inches='tight', pad_inches=0)  # Ajuste para eliminar el borde blanco
    plt.show()

    if palette:
        # Mostrar la paleta de colores como imágenes
        fig, axs = plt.subplots(1, len(palette))
        for i, color in enumerate(palette):
            axs[i].imshow(np.array([[color]]))
            axs[i].axis('off')
        fig.savefig('colorpm.jpg', bbox_inches='tight', pad_inches=0)  # Ajuste para eliminar el borde blanco
        plt.show()
    else:
        print("No se encontraron colores en la paleta.")

# Ejemplo de uso
analyze_image('a.jpg')