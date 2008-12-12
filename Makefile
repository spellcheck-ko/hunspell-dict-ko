PYTHON = python

LANG = ko

AFFIX = $(LANG).aff
DICT = $(LANG).dic

DICT_SOURCES = dict-$(LANG)/dict-*.dic

CLEANFILES = $(AFFIX) $(DICT) flaginfo.py

COLLECT = 

all: $(AFFIX) $(DICT)

$(AFFIX) flaginfo.py: make-aff.py config.py
	$(PYTHON) make-aff.py flaginfo.py > $(AFFIX) || (rm -f $@; false)

$(DICT): make-dic.py $(DICT_SOURCES) flaginfo.py 
	$(PYTHON) make-dic.py $(DICT_SOURCES) > $@ || (rm -f $@; false)

clean: 
	rm -f $(CLEANFILES)

.PHONY: all clean
