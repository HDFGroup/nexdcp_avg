[ -z ${SUMMARY_DOMAIN}  ] && echo "Need to set SUMMARY_DOMAIN" && exit 1
[ -z ${HS_USERNAME}  ] && echo "Need to set HS_USERNAME" && exit 1
[ -z ${HS_PASSWORD}  ] && echo "Need to set HS_PASSWORD" && exit 1
[ -z ${HS_ENDPOINT}  ] && echo "Need to set HS_ENDPOINT" && exit 1

docker run --name nexdcp \
 -e SUMMARY_DOMAIN=${SUMMARY_DOMAIN} \
-e HS_USERNAME=${HS_USERNAME} \
-e HS_PASSWORD=${HS_PASSWORD} \
-e HS_ENDPOINT=${HS_ENDPOINT} \
-d hdfgroup/nexdcp
