TESTS = $(sort $(wildcard *.test))

all: test

test:
	python3 checkhunspellversion.py
	@for T in $(TESTS); do \
		echo "Testing $$T..."; \
		python3 runtest.py ../ko $$T; \
	done

autopkgtest:
	python3 checkhunspellversion.py
	@for T in $(TESTS); do \
		echo "Testing $$T..."; \
		python3 runtest.py ko $$T; \
	done

.PHONY: all clean test
