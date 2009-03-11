PYTHON = python
ZIP = zip -r

AFFIX = ko.aff
DICT = ko.dic

CLEANFILES = $(AFFIX) $(DICT)

SOURCES = make-aff-dic.py config.py suffix.py suffixdata.py jamo.py	\
	flags.py aff.py template.aff
DICT_DATA = dict-ko-builtins.xml dict-ko-galkwi.xml

DISTDIR = dist

PACKAGE = hunspell-dict-ko
VERSION = $(shell $(PYTHON) -c 'import config;print(config.version)')
RELEASETAG = HEAD

SRC_DISTNAME = hunspell-dict-ko-$(VERSION)
SRC_DISTFILE = $(DISTDIR)/$(SRC_DISTNAME).tar.gz
BIN_DISTNAME = ko-aff-dic-$(VERSION)
BIN_DISTFILE = $(DISTDIR)/$(BIN_DISTNAME).zip
BIN_DISTCONTENT = LICENSE LICENSE.GPL LICENSE.LGPL LICENSE.MPL $(AFFIX) $(DICT)

all: $(AFFIX) $(DICT)

$(AFFIX) $(DICT): $(DICT_DATA) $(SOURCES)
	$(PYTHON) make-aff-dic.py $(AFFIX) $(DICT) $(DICT_DATA) 

distdir:
	if ! [ -d $(DISTDIR) ]; then mkdir $(DISTDIR); fi

clean: 
	rm -f $(CLEANFILES)
	rm -rf $(DISTDIR)

dist:: distdir $(BIN_DISTCONTENT)
	git archive --format=tar --prefix=$(SRC_DISTNAME)/ $(RELEASETAG) | gzip -9 -c > $(SRC_DISTFILE)
	rm -f $(BIN_DISTFILE)
	mkdir -p $(BIN_DISTNAME)
	install -m644 $(BIN_DISTCONTENT) $(BIN_DISTNAME)/
	$(ZIP) $(BIN_DISTFILE) $(BIN_DISTNAME)
	rm -rf $(BIN_DISTNAME)

test:
	$(MAKE) -C tests test

.PHONY: all clean dist distdir test
