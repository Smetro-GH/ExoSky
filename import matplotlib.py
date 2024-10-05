import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D

# Generar datos simulados
def generate_mock_data(num_stars=500):
    np.random.seed(42)  # For reproducibility
    return {
        'source_id': np.arange(num_stars),
        'ra': np.random.uniform(0, 360, num_stars),  # Rango más amplio
        'dec': np.random.uniform(-90, 90, num_stars),  # Rango más amplio
        'bp_rp': np.random.uniform(-0.5, 2, num_stars),
        'phot_g_mean_mag': np.random.uniform(3, 6, num_stars),
    }

def mock_process_spectra(num_stars=500, num_wavelengths=600):
    # Generar datos espectrales simulados
    return np.random.rand(num_stars, num_wavelengths)

def calculate_color_temperature(spectra):
    blue_flux = np.mean(spectra[:, 100:150], axis=1)  # ~400-450 nm
    red_flux = np.mean(spectra[:, 450:500], axis=1)   # ~750-800 nm
    return blue_flux / red_flux

def galactic_coordinates(ra, dec):
    # Aproximación simple para conversión de coordenadas ecuatoriales a galácticas
    # Nota: Esta es una aproximación cruda y no precisa para uso real
    l = (ra + 123.932) % 360
    b = dec
    return l, b

# Función para crear el mapa estelar en 3D

def create_3d_starmap(stars, spectra):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Coordenadas galácticas distribuidas esféricamente
    l, b = galactic_coordinates(stars['ra'], stars['dec'])
    r = np.random.uniform(1, 10, size=len(l))  # Distancias aleatorias
    x = r * np.cos(np.radians(b)) * np.cos(np.radians(l))
    y = r * np.cos(np.radians(b)) * np.sin(np.radians(l))
    z = r * np.sin(np.radians(b))

    # Calcular el centro exacto de la distribución de estrellas
    center_x, center_y, center_z = np.mean(x), np.mean(y), np.mean(z)

    # Tamaños y temperaturas de color de las estrellas
    sizes = 50 * 10**(-stars['phot_g_mean_mag']/5)
    color_temp = calculate_color_temperature(spectra)

    # Paleta de colores realista para las temperaturas de color
    colors = ['blue', 'white', 'yellow', 'orange', 'red']
    cmap = LinearSegmentedColormap.from_list('star_cmap', colors, N=100)

    scatter = ax.scatter(x, y, z, s=sizes, c=color_temp, cmap=cmap, alpha=0.8)

    # Configuración del fondo negro
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.grid(False)
    
    # Ocultar ejes
    ax.set_axis_off()

    # Centrar la vista en las estrellas
    max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max() / 2.0
    ax.set_xlim(center_x - max_range, center_x + max_range)
    ax.set_ylim(center_y - max_range, center_y + max_range)
    ax.set_zlim(center_z - max_range, center_z + max_range)

    # Ajustar la posición de la cámara
    ax.view_init(elev=20, azim=45)
    ax.dist = 8  # Ajusta este valor para acercar o alejar la cámara

    # Añadir título
    ax.text2D(0.5, 0.95, f'Centered 3D Star Map ({len(stars["source_id"])} Stars)', 
              transform=ax.transAxes, color='white', fontsize=14, 
              horizontalalignment='center', verticalalignment='center')

    # Colorbar
    cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('Color Temperature (Blue/Red Flux Ratio)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.tight_layout()
    plt.show()

# Ejecución principal
num_stars = 500
stars = generate_mock_data(num_stars)
spectra = mock_process_spectra(num_stars)
create_3d_starmap(stars, spectra)
plt.xlim(175, 200)