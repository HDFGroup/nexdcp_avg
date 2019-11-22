import sys
import os
import time
import h5pyd
import numpy as np

# CONUS bounding box
conus_bounds = [24.0, 50.0, 235.0, 293.5]
# climage models
climate_models = ("historical", "rcp26", "rcp45", "rcp60", "rcp85")

def get_region_avg(domain, bounds):
    f = h5pyd.File(domain, "r")
    tasmin_dset = f["tasmin"]

    # get start/end index for latitude bounds
    lat_dset = f["lat"]
    lat_arr = lat_dset[:]
    lat_index_range = [None,None]

    for i in range(lat_arr.shape[0]):
        if lat_index_range[0] is None and lat_arr[i] >= bounds[0]:
            lat_index_range[0] = i
        if lat_index_range[1] is None or lat_arr[i] < bounds[1]:
            lat_index_range[1] = i
    # make sure there is at least one element to select
    if lat_index_range[1] == lat_index_range[0]:
        lat_index_range[1] = lat_index_range[0] + 1

    print("lat_index_range:", lat_index_range)

    # get start/end index for longitude bounds
    lon_index_range = [None,None]
    lon_dset = f["lon"]
    lon_arr = lon_dset[:]
    for i in range(lon_arr.shape[0]):
        if lon_index_range[0] is None and lon_arr[i] >= bounds[2]:
            lon_index_range[0] = i
        if lon_index_range[1] is None or lon_arr[i] < bounds[3]:
            lon_index_range[1] = i
    # make sure there is at least one element to select
    if lon_index_range[1] == lon_index_range[0]:
        lon_index_range[1] = lon_index_range[0] + 1

    print("lon_index_range:", lon_index_range)

    # compute time index
    time_dset = f["time"]
    num_slices = time_dset.shape[0]
    time_index = int(time_dset[0] // 30)

    avg_arr = np.zeros((num_slices,), dtype="f4")
    for i in range(num_slices):
        arr = tasmin_dset[i, lat_index_range[0]:lat_index_range[1], lon_index_range[0]:lon_index_range[1]]
        count = 0
        sum = 0.0
        for j in range(arr.shape[0]):
            for k in range(arr.shape[1]):
                if arr[j,k] < 999.0:
                    sum += arr[j,k]
                    count += 1
        if count > 0:
            avg = sum / count
            avg_arr[i] = avg

    return (time_index, avg_arr)

def get_model(filename):
    for model in climate_models:
        if filename.find(model) >= 0:
            return model
    return None

if "SUMMARY_DOMAIN" not in os.environ:
    print("SUMMARY_DOMAIN env not set")
    sys.exit(1)

# summary_domain = "/home/jreadey/nexdcp/summary.h5"
summary_domain = os.environ["SUMMARY_DOMAIN"]

print(f"Opening domain: {summary_domain}")
f = h5pyd.File(summary_domain, "r+")

folder = f.attrs["folder"]   # "/shared/NASA/NEX-DCP30/"
start_year = f.attrs["start_year"]  # 1950
end_year = f.attrs["end_year"]  # 2100
bounds = [0.0,0.0,0.0,0.0]
bounds[0] = f.attrs["lat_min"]
bounds[1] = f.attrs["lat_max"]
bounds[2] = f.attrs["lon_min"]
bounds[3] = f.attrs["lon_max"]

table = f["inventory"]
condition = f"start == 0"  # query for files that haven't been proccessed

while True:
    now = int(time.time())
    update_val = {"start": now}
    # query for row with 0 start value and update it to now
    indices = table.update_where(condition, update_val, limit=1)
    if not indices:
        print("no more work to be done")
        break
    job_index = indices[0]
    print(f"updated job index: {job_index} as in progress")
    row = table[job_index]
    filename = row[0].decode("utf-8")
    print("got filename:", filename)
    model = get_model(filename)
    (index, avgarr) = get_region_avg(folder + filename, bounds)
    print(f"got avg index: {index} avg: {avgarr}")
    numrows = avgarr.shape[0]
    dset = f[model]
    dset[index:(index+numrows)] = avgarr
    row[2] = int(time.time())
    table[job_index] = row # mark the file as done
    print(f"updated job index: {job_index} as complete")

print("exiting")
