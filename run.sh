project_name=mask
docker build -t $project_name .
docker stop $project_name
docker rm $project_name
docker run -d \
--name $project_name \
--restart=always \
-p 8081:80 \
$project_name