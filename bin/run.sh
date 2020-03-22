project_name=mask_info
export_port=8081

docker build -t $project_name .
docker stop $project_name
docker rm $project_name
docker run -d \
--name $project_name \
--restart=always \
-p ${export_port}:5000 \
-v /home/sidlin/secret:/root/secret \
-v /etc/timezone:/etc/timezone:ro \
$project_name