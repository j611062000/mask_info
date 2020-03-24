target="/var/data.json"
url="https://raw.githubusercontent.com/kiang/pharmacies/master/json/points.json"
curl -o ${target} ${url}
python /app/data_filter.py