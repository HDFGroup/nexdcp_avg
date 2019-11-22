FROM conda/miniconda3
LABEL MAINTAINER="John Readey, HDF Group"
ENV AWS_REGION=us-west-2
ENV HS_ENDPOINT=http://100.66.25.138
ENV HS_USERNAME=jreadey@hdfgroup.org
ENV HS_PASSWORD=SupplyCorrectValue

RUN apt-get update
RUN apt-get install git -y
RUN pip --no-cache-dir install git+https://github.com/HDFGroup/h5pyd.git --upgrade
RUN mkdir /app
COPY compute_region_avg.py /app
COPY entrypoint.sh  /

ENTRYPOINT ["/entrypoint.sh"]
