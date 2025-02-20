import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import h5py
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt
import xyzservices.providers as xyz

folder_path = "./aer_ai_data/nrti/*.nc.zip"
file1 = "./aer_ai_data/nrti/S5P_NRTI_L2__AER_AI_20250206T162119_20250206T162619_37927_03_020800_20250206T170430.nc.zip"
file2="./aer_ai_data/nrti/S5P_NRTI_L2__AER_AI_20250207T160619_20250207T161119_37941_03_020800_20250207T164634.nc.zip"


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

# Extract data
aerosol_index = ds_product["aerosol_index_354_388"].squeeze()  # Remove time dim (1,)
lat = ds_product["latitude"].squeeze()
lon = ds_product["longitude"].squeeze()

# Obter a data e hora da medição
measurement_time = ds_product["time"].values[0].astype('datetime64[s]')  # Converte para formato de data e hora


# Print shapes
print(f"Aerosol Index shape: {aerosol_index.shape}")
print(f"Latitude shape: {lat.shape}")
print(f"Longitude shape: {lon.shape}")

# Create figure and map projection
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()})

# Use a satellite imagery basemap (ESRI Satellite)

tiler = cimgt.GoogleTiles(style="satellite")  # Alternative: cimgt.GoogleTiles(style="satellite")
ax.add_image(tiler, 8)  # Zoom level 8 (adjust as needed)

# Add map features
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.add_feature(cfeature.LAND, facecolor="lightgray")

# Plot the aerosol index as a colormap
mesh = ax.pcolormesh(lon, lat, aerosol_index, cmap="plasma", shading="auto", alpha=0.7, transform=ccrs.PlateCarree())

point_lat = -22.851612120612987
point_lon = -47.127141566554286

# Add point of interest
ax.scatter(point_lon, point_lat, color='cyan', s=50, label="Point of Interest", transform=ccrs.PlateCarree(), zorder=5)

# Add colorbar
cbar = plt.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02)
cbar.set_label("Aerosol Index (354-388 nm)")

# Set title
plt.title(f"TROPOMI Índice de Aerossol - Medição: {measurement_time}")

# Show plot
plt.show()

print("end")

