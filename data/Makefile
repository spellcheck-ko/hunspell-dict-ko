PYTHON=python3
SCRIPTSDIR=scripts

.PHONY:
.PHONY: all build help

all: help

help:
	@echo "Targets: "
	@echo "    make build"
	@echo "      - build hunspell-dict-ko word files from raw files"

build:
	$(PYTHON) $(SCRIPTSDIR)/build.py
