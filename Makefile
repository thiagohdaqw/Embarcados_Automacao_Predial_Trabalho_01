
PYTHON ?= python3
CENTRAL ?= central
CENTRAL_CONFIG_JSON_FILE ?= "configuracao_central.json"

DISTRIBUTED ?= distributed
DISTRIBUTED_CONFIG_JSON_FILE ?= "configuracao_sala_04.json"

run-central:
		$(PYTHON) -m $(CENTRAL) $(CENTRAL_CONFIG_JSON_FILE)

run-distributed:
		$(PYTHON) -m $(DISTRIBUTED) $(DISTRIBUTED_CONFIG_JSON_FILE) $(CENTRAL_CONFIG_JSON_FILE)

install:
		$(PYTHON) -m pip install -r requirements.txt
