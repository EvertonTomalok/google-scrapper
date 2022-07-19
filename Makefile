start-product-crawl-worker:
	pipenv run python -m src.ports.cli.main crawl-products-daemon -w $(workers)

start-ean-extractor:
	pipenv run python -m src.domain.commands.ean_extractor $(ean)

start-ean-extractor-and-update-table:
	pipenv run python -m src.ports.cli.main crawl-ean -d $(data) -e $(ean)

up:
	docker-compose up -d

install-lib:
	pipenv install -e .

prepare-pipenv:
	pipenv install --deploy --dev

.PHONY: setup
setup: prepare-pipenv
setup: install-lib

postgres-migrate:
	pipenv run python -m scripts.postgres_migrate

create-mongodb-indexes:
	pipenv run python -m scripts.create_indexes_mongodb

web:
	uvicorn src.ports.web.server:app --port=3000 --workers 5 --reload

.PHONY: autoflake
autoflake:
	pipenv run autoflake -r $(AUTOFLAKE_OPTIONS) --exclude */snapshots --remove-unused-variables --remove-all-unused-imports  **/ | tee autoflake.log
	echo "$(AUTOFLAKE_OPTIONS)" | grep -q -- '--in-place' || ! [ -s autoflake.log ]

.PHONY: isort
isort:
	pipenv run isort ./src --multi-line 3 --trailing-comma --line-width 88 --skip */snapshots $(ISORT_OPTIONS)

.PHONY: black
black:
	pipenv run black ./src --exclude '.*/snapshots' $(BLACK_OPTIONS)

.PHONY: lint
lint: ISORT_OPTIONS := --check-only
lint: BLACK_OPTIONS := --check
lint: autoflake isort black
	pipenv run mypy ./src --ignore-missing-imports
	pipenv run flake8 ./src

.PHONY: format
format: AUTOFLAKE_OPTIONS := --in-place
format: autoflake isort black

test:
	python -m pytest tests/ $(SNAPSHOT_UPDATE) $(VV)

.PHONY: test-vv
test-vv: VV := -vv
test-vv: test

.PHONY: snapshot-update
snapshot-update: SNAPSHOT_UPDATE := --snapshot-update
snapshot-update: test
