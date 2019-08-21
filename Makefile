PYTHON := python3
ZIP := zip -r

KO_AFF := ko.aff
KO_DIC := ko.dic

CLEANFILES := $(KO_AFF) $(KO_DIC)

SOURCES := make-aff-dic.py config.py suffix.py suffixdata.py jamo.py	\
	flags.py aff.py josa.py template.aff
DICT_DATA = dict-ko-builtins.yaml dict-ko-data.yaml

DISTDIR := dist

HOST_DICT_PATH := /usr/share/hunspell/ko

PACKAGE := hunspell-dict-ko
VERSION := $(shell $(PYTHON) -c 'import config;print(config.version)')
RELEASETAG := HEAD

SRC_DISTNAME := hunspell-dict-ko-$(VERSION)
SRC_DISTFILE := $(DISTDIR)/$(SRC_DISTNAME).tar.xz
BIN_DISTNAME := ko-aff-dic-$(VERSION)
BIN_DISTFILE := $(DISTDIR)/$(BIN_DISTNAME).zip
BIN_DISTCONTENT = LICENSE.md LICENSE.GPL-3 $(KO_AFF) $(KO_DIC)

all: build

build: $(KO_AFF) $(KO_DIC)

$(KO_AFF) $(KO_DIC): $(DICT_DATA) $(SOURCES)
	$(PYTHON) make-aff-dic.py $(KO_AFF) $(KO_DIC) $(DICT_DATA) 

distdir:
	if ! [ -d $(DISTDIR) ]; then mkdir $(DISTDIR); fi

clean: 
	rm -f $(CLEANFILES)
	rm -rf $(DISTDIR)

dist:: distdir $(BIN_DISTCONTENT)
	git -c 'tar.tar.xz.command=xz -c' archive --format=tar.xz --prefix=$(SRC_DISTNAME)/ -o $(SRC_DISTFILE) $(RELEASETAG)
	rm -f $(BIN_DISTFILE)
	mkdir -p $(BIN_DISTNAME)
	install -m644 $(BIN_DISTCONTENT) $(BIN_DISTNAME)/
	$(ZIP) $(BIN_DISTFILE) $(BIN_DISTNAME)
	rm -rf $(BIN_DISTNAME)

test: build
	$(MAKE) -C tests test

hosttest:
	$(MAKE) -C tests test DICT=$(HOST_DICT_PATH)

.PHONY: all build clean dist distdir test autopkgtest
