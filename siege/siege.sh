# Wait for db to initialize
echo "Waiting for db to initialize"
sleep 15

# 100 concurrent users
echo "25 concurrent users for 1 minute"
echo "Pushing timestamps in the app"
siege --internet --time=1m --concurrent=25 -f urls.txt
