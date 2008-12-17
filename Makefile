PYTHON = python

LANG = ko

AFFIX = $(LANG).aff
DICT = $(LANG).dic

DICT_SOURCES = dict-$(LANG)/dict-*.dic

CLEANFILES = $(AFFIX) $(DICT)

COLLECT = 

PACKAGE = hunspell-dict-ko
VERSION = $(shell python -c 'import config;print(config.version)')
DISTNAME = $(PACKAGE)-$(VERSION)
RELEASETAG = HEAD


all: $(AFFIX) $(DICT)

$(AFFIX): make-aff.py config.py suffix.py suffixdata.py
	$(PYTHON) make-aff.py > $(AFFIX) || (rm -f $@; false)

$(DICT): make-dic.py $(DICT_SOURCES) config.py  suffix.py suffixdata.py
	$(PYTHON) make-dic.py $(DICT_SOURCES) > $@ || (rm -f $@; false)

clean: 
	rm -f $(CLEANFILES)

dist:
	git-archive --format=tar --prefix=$(DISTNAME)/ $(RELEASETAG) | gzip -9 -c > $(DISTNAME).tar.gz

.PHONY: all clean dist
