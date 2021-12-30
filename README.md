# receiptify-flask

## Steps to getting spotify credentials 
1. go to https://developer.spotify.com/dashboard/login and make an account and a project 
2. go to your project and click "EDIT SETTINGS" and add your "Redirect URIs" (with ports)

After you get credentials... 

## Steps to run locally 
1. python3 setup.py install 
2. flask run 

## Steps to run with Docker
1. docker build -t receiptify-flask:1.0.1 . 
2. docker run -p 1000:5000 {CONTAINER_ID}

## Steps to run with Docker Swarm 
*** not complete
1. docker-compose build
2. docker swarm init
3. docker stack deploy -c docker-compose.yml swarmapp
4. docker service ls 

