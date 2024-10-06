import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from astroquery.gaia import Gaia
from astropy import units as u
from astropy.coordinates import SkyCoord

# Configuración de la consulta a Gaia
def query_gaia_exoplanets(limit):
    query = f"""
    SELECT TOP {limit}
        SOURCE_ID, ra, dec, bp_rp, phot_g_mean_mag,
        phot_bp_mean_mag, phot_rp_mean_mag
    FROM gaiadr3.gaia_source
    WHERE phot_g_mean_mag < 6
      AND bp_rp IS NOT NULL
      AND phot_bp_mean_mag IS NOT NULL
      AND phot_rp_mean_mag IS NOT NULL
    ORDER BY phot_g_mean_mag ASC
    """
    job = Gaia.launch_job(query)
    return job.get_results()

# Calcular la temperatura de color
def calculate_color_temperature(bp_rp):
    # Relación aproximada de BP-RP con la temperatura (K)
    return 6400 * (1 / (0.92 * bp_rp + 1.7) + 1 / (0.92 * bp_rp + 0.62))

# Crear mapa estelar con colores reales
def create_2d_starmap(stars):
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
    
    # Usar RA y Dec directamente para las coordenadas x e y
    x = stars['ra']
    y = stars['dec'] 

    # Tamaños y temperaturas de color de las estrellas
    sizes = .8 * 10**(-stars['phot_g_mean_mag']/5)
    temperatures = calculate_color_temperature(stars['bp_rp'])

    # Normalizar temperaturas para mapear a un rango de colores
    norm = plt.Normalize(vmin=temperatures.min(), vmax=temperatures.max())
    cmap = plt.get_cmap('plasma')

    scatter = ax.scatter(x, y, s=sizes, c=temperatures, cmap=cmap, norm=norm, alpha=0.8)

    # Configuración del fondo y ejes
    ax.set_facecolor('black')
    ax.set_xlim(0, 360)
    ax.set_ylim(-90, 90)
    
    # Etiquetas de los ejes
    ax.set_xlabel('Right Ascension (degrees)', color='white')
    ax.set_ylabel('Declination (degrees)', color='white')
    ax.tick_params(colors='white')

    # Título con un exoplaneta aleatorio
    ax.set_title(f'View from Exoplanet {np.random.randint(1,5000)}', color='red')

    # Añadir barra de colores para mostrar la temperatura
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('Temperature (K)', color='black')
    cbar.ax.yaxis.set_tick_params(color='black')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='black')

    plt.tight_layout()
    plt.show()

# Main execution
stars_limit = 10000
stars = query_gaia_exoplanets(stars_limit)
create_2d_starmap(stars)
