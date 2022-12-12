
PYTHON ?= /usr/bin/python
CENTRAL ?= central
CENTRAL_CONFIG_JSON_FILE ?= "configuracao_central.json"


run-central:
		$(PYTHON) -m $(CENTRAL) $(CENTRAL_CONFIG_JSON_FILE)
