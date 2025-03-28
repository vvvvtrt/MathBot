# For local use
.PHONY: local-run
local-run:
	python3 main.py

# For Docker
.PHONY: docker-db-up
docker-db-up:
	docker compose up -d postgresql

.PHONY: docker-db-stop
docker-db-stop:
	docker stop postgresql


.PHONY: docker-adminer-up
docker-adminer-up:
	docker compose up -d adminer

.PHONY: docker-adminer-stop
docker-adminer-stop:
	docker stop adminer

.PHONY: docker-down
docker-down:
	docker compose down