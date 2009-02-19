PYTHON = python

LANG = ko

AFFIX = $(LANG).aff
DICT = $(LANG).dic

DICT_SOURCES = dict-$(LANG).xml

CLEANFILES = $(AFFIX) $(DICT)

DISTDIR = dist

PACKAGE = hunspell-dict-ko
VERSION = $(shell $(PYTHON) -c 'import config;print(config.version)')
RELEASETAG = HEAD

SRC_DISTNAME = hunspell-dict-ko-$(VERSION)
SRC_DISTFILE = $(DISTDIR)/$(SRC_DISTNAME).tar.gz

all: $(AFFIX) $(DICT)

$(AFFIX): make-aff.py config.py suffix.py suffixdata.py
	$(PYTHON) make-aff.py > $(AFFIX) || (rm -f $@; false)

$(DICT): $(DICT_SOURCES) make-dic.py config.py  suffix.py suffixdata.py
	$(PYTHON) make-dic.py $< > $@ || (rm -f $@; false)

distdir:
	if ! [ -d $(DISTDIR) ]; then mkdir $(DISTDIR); fi

clean: 
	rm -f $(CLEANFILES)
	rm -f $(DISTDIR)

dist:: distdir
	git archive --format=tar --prefix=$(SRC_DISTNAME)/ $(RELEASETAG) | gzip -9 -c > $(SRC_DISTFILE)

.PHONY: all clean dist distdir
