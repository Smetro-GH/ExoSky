import matplotlib.pyplot as plt
import numpy as np
from astroquery.gaia import Gaia
from astropy import units as u
from astropy.coordinates import SkyCoord
from gaiaxpy import calibrate
from matplotlib.colors import LinearSegmentedColormap

exoplanet = 'planeta X'

# Expanded list of stars (name, RA, Dec, G mag, BP-RP color index)
stars = [
    ('Sirius', 101.28715533, -16.71611586, -1.46, 0.00),
    ('Canopus', 95.98747, -52.69566, -0.74, 0.15),
    ('Rigil Kentaurus', 219.90085, -60.83399, -0.01, 0.69),
    ('Arcturus', 213.91530, 19.18222, -0.05, 1.33),
    ('Vega', 279.23473479, 38.78368896, 0.03, -0.12),
    ('Capella', 79.17232, 45.99799, 0.08, 0.79),
    ('Rigel', 78.63446707, -8.20163990, 0.13, -0.31),
    ('Procyon', 114.82548, 5.22496, 0.38, 0.44),
    ('Achernar', 24.42848, -57.23667, 0.46, -0.16),
    ('Betelgeuse', 88.79293899, 7.40706275, 0.42, 1.85),
    ('Hadar', 210.95615, -60.37303, 0.61, -0.17),
    ('Altair', 297.69582, 8.86832, 0.76, 0.23),
    ('Acrux', 186.64996, -63.09909, 0.77, -0.25),
    ('Aldebaran', 68.98016, 16.50930, 0.86, 1.54),
    ('Antares', 247.35166, -26.43203, 0.96, 1.86),
    ('Spica', 201.29824, -11.16132, 0.97, -0.23),
    ('Pollux', 116.32894, 28.02619, 1.14, 1.01),
    ('Fomalhaut', 344.41269, -29.62224, 1.16, 0.10),
    ('Deneb', 310.35797, 45.28033, 1.25, 0.02),
    ('Mimosa', 191.93012, -59.68868, 1.26, -0.22),
    ('Regulus', 152.09293, 11.96721, 1.36, -0.12),
    ('Adhara', 104.65646, -28.97208, 1.50, -0.21),
    ('Castor', 113.64946, 31.88863, 1.58, 0.04),
    ('Gacrux', 187.79184, -57.11325, 1.63, 1.61),
    ('Shaula', 263.40203, -37.10374, 1.62, -0.18),
    ('Bellatrix', 81.28225, 6.34970, 1.64, -0.20),
    ('Elnath', 81.57297, 28.60745, 1.65, -0.10),
    ('Miaplacidus', 138.30064, -69.71719, 1.69, 0.01),
    ('Alnilam', 84.05340, -1.20194, 1.69, -0.19),
    ('Alnair', 332.05826, -46.88095, 1.74, -0.11),
    ('Alnitak', 85.18963, -1.94257, 1.77, -0.18),
]

def create_starmap(stars):
    fig, ax = plt.subplots(figsize=(15, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # Create custom colormap
    colors = ['blue', 'white', 'yellow', 'orange', 'red']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('star_cmap', colors, N=n_bins)
    
    for name, ra, dec, g_mag, bp_rp in stars:
        x = ra
        y = dec
        
        # Calculate star size based on apparent magnitude
        size = 20 * 10**(-g_mag/5)  # Adjusted for better visibility
        
        # Plot the star
        scatter = ax.scatter(x, y, s=size, c=[bp_rp], cmap=cmap, 
                             vmin=-0.5, vmax=2, edgecolors='none', alpha=0.8)
        
        # Add star name
        #ax.annotate(name, (x, y), xytext=(5, 5), textcoords='offset points', 
         #           color='white', fontsize=8)

    ax.set_xlabel('Right Ascension', color='white')
    ax.set_ylabel('Declination', color='white')
    ax.set_title(f'View From {exoplanet}', color='white')

    ax.invert_xaxis()
    ax.set_xlim(360, 0)  # Set RA limits
    ax.set_ylim(-90, 90)  # Set Dec limits

    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('BP-RP Color Index', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.grid(color='gray', linestyle=':', alpha=0.3)
    plt.tight_layout()
    plt.show()

# Create the enhanced star map
create_starmap(stars)