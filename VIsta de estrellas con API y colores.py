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

# Procesar espectros simulados
def mock_process_spectra(num_stars=500, num_wavelengths=600):
    return np.random.rand(num_stars, num_wavelengths)

# Calcular la temperatura de color
def calculate_color_temperature(spectra):
    blue_flux = np.mean(spectra[:, 100:150], axis=1)
    red_flux = np.mean(spectra[:, 450:500], axis=1)
    return blue_flux / red_flux

# Crear mapa estelar con colores reales
def create_2d_starmap(stars, spectra):
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
    
    # Usar RA y Dec directamente para las coordenadas x e y
    x = stars['ra']
    y = stars['dec']

    # Tamaños y temperaturas de color de las estrellas
    sizes = .1 * 10**(-stars['phot_g_mean_mag']/5)
    color_temp = calculate_color_temperature(spectra)

    # Paleta de colores realista para las temperaturas de color
    colors = ['blue', 'white', 'yellow', 'orange', 'red']
    cmap = LinearSegmentedColormap.from_list('star_cmap', colors, N=100)

    scatter = ax.scatter(x, y, s=sizes, c=color_temp, cmap=cmap, alpha=0.8)

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

    plt.tight_layout()
    plt.show()

# Main execution
stars_limit = 10000
stars = query_gaia_exoplanets(stars_limit)
spectra = mock_process_spectra(len(stars))
create_2d_starmap(stars, spectra)
