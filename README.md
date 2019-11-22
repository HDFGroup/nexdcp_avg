nexdcp_avg
==========

Cluster compute to determine temperature changes over given region

Description
-----------

This repository demonstrates how to use Kubernetes jobs to speed up computations over a large data collection.

Dataset
-------

The source data is 8195 NetCDF4 files stored on AWS.  These datasets contain historical and projected climate data for the years 1950-2100 covereing the continental US.  See: <https://aws.amazon.com/about-aws/whats-new/2013/11/12/nasa-nex-public-datasets/> for more details.

These files are stored in the KitaLab server under the path: /shared/NASA/NEX-DCP30/.

Computation
-----------

For a given geographic region, we'll calculate the per month average for "tasmin" using historical data and the four included climate models ("rcp26", "rcp45", "rcp60", "rcp85").  This covers about 3.2TB of files stored in S3 that will need to be examined.  To speed up the process will will run multiple workers using Kubernetes pods to sub-divide the work.

Requirements
------------

You will need an account for KitaLab and access to a Kubernetes cluster to run the pods.

Running the code
----------------

Build the Docker image (`docker build -t nexdcp .`), tag, and push to AWS ECR.

Run "make_summary_file.py" to initialize a HSDS file that will be used to coordinate the workers and store the final results.  Arguments are path to summary file, lat_min, lat_max, lon_min, and lon_max.

Modify nexdcp.yml giving the Kita username, password, and path to the summary file created above.

Launch the worker pods using: `kubectl -f nexdcp.yml`.

Verify the pods are running: `kubectl get pods`.

Track the number of files processed using: `python get_job_stats.py`.

By default only one worker pod is launched.  To speed up the computation, scale up the number of worker pods: `kubectl scale --replicas=n replicasets/nexdcp` where n is the number of pods desired.

Once the remaining count goes to zero (as reported by get_job_stats), the computation is complete and results will be stored as datasets in the summary_file.
