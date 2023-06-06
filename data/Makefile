MAKEFLAGS += -j$(shell nproc)

PYTHON=python3
SCRIPTSDIR=scripts
ENTRIESDIR=entries

.PHONY:
.PHONY: all build help

all: help

help:
	@echo "Targets: "
	@echo "    make build"
	@echo "      - build hunspell-dict-ko word files from raw files"

build::
	$(PYTHON) $(SCRIPTSDIR)/build.py

process:: $(ENTRIESDIR)/*.yaml

$(ENTRIESDIR)/*.yaml::
	$(PYTHON) $(SCRIPTSDIR)/process.py $@
