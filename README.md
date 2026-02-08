See if docker exists 
docker --version
docker compose version



then go to infra file 
run this - `docker compose up`

it should run without errors and should say it is ready to accpet connections 

then on another terminal tab run 
`curl -I http://localhost:7880`

it should recieve a connection that means the server is running.



My next step would be to see if i can send packets of any kind like a movie or something through UDP.
