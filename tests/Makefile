TESTS = $(sort $(wildcard *.test))

all: test

test:
	python3 checkhunspellversion.py
	@RESULT=0; for T in $(TESTS); do \
		echo "Testing $$T..."; \
		python3 runtest.py ../ko $$T || RESULT=1; \
	done; exit $$RESULT

autopkgtest:
	python3 checkhunspellversion.py
	@RESULT=0; for T in $(TESTS); do \
		echo "Testing $$T..."; \
		python3 runtest.py ko $$T || RESULT=1; \
	done; exit $$RESULT

.PHONY: all clean test
