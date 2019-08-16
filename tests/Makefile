TESTS = $(sort $(wildcard *.test))
DICT = ../ko

all: test

test:
	-echo | hunspell -d $(DICT) | head -1
	python3 checkhunspellversion.py
	@RESULT=0; for T in $(TESTS); do \
		echo "Testing $$T..."; \
		python3 runtest.py $(DICT) $$T || RESULT=1; \
	done; exit $$RESULT

.PHONY: all clean test
