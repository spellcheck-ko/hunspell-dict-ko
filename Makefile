PYTHON = python

LANG = ko

AFFIX = $(LANG).aff
DICT = $(LANG).dic

DICT_SOURCES = dict-$(LANG)/dict-*.dic

CLEANFILES = $(AFFIX) $(DICT) flaginfo.py

COLLECT = 

all: $(AFFIX) $(DICT)

$(AFFIX) flaginfo.py: make-aff.py config.py
	$(PYTHON) make-aff.py flaginfo.py > $(AFFIX)

$(DICT): make-dic.py $(DICT_SOURCES) flaginfo.py 
	$(PYTHON) make-dic.py $(DICT_SOURCES) > $@

clean: 
	rm -f $(CLEANFILES)

.PHONY: all clean
