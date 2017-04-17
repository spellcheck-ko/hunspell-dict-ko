TESTS = $(sort $(wildcard *.test))

all: test

test:
	@for T in $(TESTS); do \
		echo "Testing $$T..."; \
		python3 runtest.py $$T; \
	done

.PHONY: all clean test
