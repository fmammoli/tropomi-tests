import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import h5py
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt
import xyzservices.providers as xyz
import pandas as pd
import pytz
from datetime import datetime

folder_path = "./aer_ai_data/nrti/*.nc.zip"
file1 = "./aer_ai_data/nrti/S5P_NRTI_L2__AER_AI_20250206T162119_20250206T162619_37927_03_020800_20250206T170430.nc.zip"
file2="./aer_ai_data/nrti/S5P_NRTI_L2__AER_AI_20250207T160619_20250207T161119_37941_03_020800_20250207T164634.nc.zip"
file3= "./aer_ai_data/nrti/S5P_NRTI_L2__AER_AI_20250212T161119_20250212T161619_38012_03_020800_20250212T165210.nc.zip"

#ds = xr.open_mfdataset(folder_path, engine='h5netcdf', combine="nested", concat_dim="time")
#d = xr.open_dataset(file1, group="Product", engine='h5netcdf')

with h5py.File(file1, "r") as f:
    def print_structure(name, obj):
        if isinstance(obj, h5py.Group):
            print(f"Group: {name}")

    f.visititems(print_structure)  

ds_product = xr.open_dataset(file1, group="PRODUCT", engine='h5netcdf')


print(ds_product)

aerosol_index = ds_product["aerosol_index_354_388"]

# Obter a data e hora da medição
measurement_time = ds_product["time"].values[0].astype('datetime64[s]')  # Converte para formato de data e hora

aerosol_index = ds_product["aerosol_index_354_388"]
lat = ds_product["latitude"]
lon = ds_product["longitude"]

# Print shapes
print(f"Aerosol Index shape: {aerosol_index.shape}")
print(f"Latitude shape: {lat.shape}")
print(f"Longitude shape: {lon.shape}")

print(aerosol_index)

# Point of interest
point_lat = -22.851612120612987
point_lon = -47.127141566554286

#finding the index of the latitute closer to CTI latitude

# Getting the values without the extra dimension
lat_values = lat.values.squeeze()
lon_values = lon.values.squeeze()
aerosol_values = aerosol_index.values.squeeze()

# Get absolute diferences in lat and lon
lat_diff = np.abs(lat_values - point_lat)
lon_diff = np.abs(lon_values - point_lon)

#Calculate the eucledian distance
dist = np.sqrt(lat_diff**2 + lon_diff**2)

# Find the indices of the minimum distance
min_idx = np.unravel_index(np.argmin(dist), lat_values.shape)

# Unpack the indices, scanline is rows and ground_pixel is columns
scanline_idx, ground_pixel_idx = min_idx

# Get the closest values
closest_lat = lat_values[scanline_idx, ground_pixel_idx]
closest_lon = lon_values[scanline_idx, ground_pixel_idx]
closest_aerosol = aerosol_values[scanline_idx, ground_pixel_idx]

# Print results
print(f"Closest Latitude: {closest_lat}")
print(f"Closest Longitude: {closest_lon}")
print(f"Closest Aerosol Index: {closest_aerosol}")
print(f"Indices (scanline, ground_pixel): {min_idx}")

#Results
#Closest Latitude: -22.83367156982422
#Closest Longitude: -47.100894927978516
#Closest Aerosol Index: -0.782738208770752
#Indices (scanline, ground_pixel): (np.int64(318), np.int64(70))

#Get the neighborhood 
bounding_size = 1 #3x3 around index that has our point of interest, use 2 for 5x5 neighborhood
scanline_idx_min = max(scanline_idx - bounding_size, 0)
scanline_idx_max = min(scanline_idx + bounding_size + 1, lat_values.shape[0])

ground_pixel_idx_min = max(ground_pixel_idx - bounding_size, 0)
ground_pixel_idx_max = min(ground_pixel_idx + bounding_size + 1, lat_values.shape[1])

# Extract the neighborhood
lat_neighbors = lat_values[scanline_idx_min:scanline_idx_max, ground_pixel_idx_min:ground_pixel_idx_max]
lon_neighbors = lon_values[scanline_idx_min:scanline_idx_max, ground_pixel_idx_min:ground_pixel_idx_max]
aerosol_neighbors = aerosol_values[scanline_idx_min:scanline_idx_max, ground_pixel_idx_min:ground_pixel_idx_max]


# Print results
print("Latitude neighbors:\n", lat_neighbors)
print("Longitude neighbors:\n", lon_neighbors)
print("Aerosol Index neighbors:\n", aerosol_neighbors)

# Plot the neighborhood
# Create figure
fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': ccrs.PlateCarree()})
 
#Plot pcolormesh
mesh = ax.pcolormesh(lon_neighbors, lat_neighbors, aerosol_neighbors, cmap='coolwarm', alpha=0.8, shading='auto', vmin=-2, vmax=2, transform=ccrs.PlateCarree())

# Add colorbar
cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', label='Aerosol Index')

# Use a satellite imagery basemap (ESRI Satellite)
tiler = cimgt.GoogleTiles(style="satellite")  # Alternative: cimgt.GoogleTiles(style="satellite")
ax.add_image(tiler, 16)  # Zoom level 8 (adjust as needed)

# Add geographic features
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')

# Plot the original point of interest
ax.scatter(point_lon, point_lat, color='red', marker='X', s=50, label="CTI - Renato Archer")

# Labels and title
first_time_utc = ds_product["time_utc"].values.flatten()[0]
sp_time = pytz.timezone('America/Sao_Paulo')

time_title = pd.to_datetime(first_time_utc).astimezone(sp_time).strftime('%d/%m/%Y %H:%M:%S GMT%Z')

ax.set_title(f"Aerosol Index Around CTI Renato Archer at {time_title}")
ax.legend()

# Show plot
plt.show()

print("end")