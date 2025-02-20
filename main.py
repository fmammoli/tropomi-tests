#platform for data exploring
# https://www.wekeo.eu/data?view=viewer

from hda import Client, Configuration
import xarray as xr

my_api_token = "c1819583-5f19-403f-a003-57ebcbb7b1d3"
# Configure user's credentials without a .hdarc

conf = Configuration(user = "fmammoli", password = "GaiaSenses10*")
hda_client = Client(config = conf)

query = {
  "dataset_id": "EO:ESA:DAT:SENTINEL-5P",
  "bbox": [
    -47.12915212179717,
    -22.853746447093542,
    -47.12685982127929,
    -22.851179800188994
  ],
  "productType": "L2__AER_AI",
  "processingLevel": "L2",
  "instrument": "TROPOMI",
  "status": "ALL",
  "startdate": "2025-02-06T00:00:00.000Z",
  "enddate": "2025-02-13T23:59:59.999Z",
  "itemsPerPage": 200,
  "startIndex": 0
}

# Ask the result for the query passed in parameter
matches = hda_client.search(query)

# List the results
print(matches)

# Download results in a directory (e.g. '/tmp')
matches.download(download_dir=".")

