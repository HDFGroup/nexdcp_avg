import time
import h5pyd
# change to the location used in "make_summary_file.py"
summary_file = "/home/jreadey/nexdcp/summary.h5"

f = h5pyd.File(summary_file, "r")

# get job stats
inventory = f["inventory"][:]
remaining = 0
failed = 0
inprogress = 0
complete = 0
recent = 0
now = int(time.time())
for i in range(inventory.shape[0]):
    row = inventory[i]
    if row[1] == 0:
        remaining += 1
    else:
        if row[2] > 0:
            complete += 1
            if now - row[2] < 60:
                recent += 1  # completed in the last minute
        else:
            if now - row[1] > 300:
                # started more than 5 minutes ago, mark as failed
                failed += 1
            else:
                inprogress += 1
print("remaining:", remaining)
print("failed:", failed)
print("inprogress:", inprogress)
print("complete:", complete)
print("completed less than one minute ago:", recent)
