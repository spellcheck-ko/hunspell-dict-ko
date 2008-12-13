PYTHON = python

LANG = ko

AFFIX = $(LANG).aff
DICT = $(LANG).dic

DICT_SOURCES = dict-$(LANG)/dict-*.dic

CLEANFILES = $(AFFIX) $(DICT) flaginfo.py

COLLECT = 

PACKAGE = hunspell-dict-ko
VERSION = $(shell python -c 'import config;print(config.version)')
DISTNAME = $(PACKAGE)-$(VERSION)
RELEASETAG = HEAD


all: $(AFFIX) $(DICT)

$(AFFIX) flaginfo.py: make-aff.py config.py
	$(PYTHON) make-aff.py flaginfo.py > $(AFFIX) || (rm -f $@; false)

$(DICT): make-dic.py $(DICT_SOURCES) flaginfo.py 
	$(PYTHON) make-dic.py $(DICT_SOURCES) > $@ || (rm -f $@; false)

clean: 
	rm -f $(CLEANFILES)

dist:
	git-archive --format=tar --prefix=$(DISTNAME)/ $(RELEASETAG) | gzip -9 -c > $(DISTNAME).tar.gz

.PHONY: all clean dist
