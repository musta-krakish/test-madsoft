init:
		docker compose stop
		docker compose pull
		docker compose build
		docker compose up -d 

down:
		docker compose down