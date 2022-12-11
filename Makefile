
PYTHON ?= /usr/bin/python
CENTRAL ?= central
CENTRAL_CONFIG_JSON_FILE ?= "configuracao_central.json"
CONFIG_SEPARATOR ?= :
CONFIG_ROOM_JSON_FILES ?= "configuracao_sala_04.json$(CONFIG_SEPARATOR)configuracao_sala_03.json"


run-central:
		$(PYTHON) $(CENTRAL) $(CENTRAL_CONFIG_JSON_FILE) $(CONFIG_SEPARATOR) $(CONFIG_ROOM_JSON_FILES)
