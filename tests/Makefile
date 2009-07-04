TESTS = $(wildcard *.test)

all: test

test:
	@for T in $(TESTS); do \
		echo "Testing $$T..."; \
		perl runtest.py $$T || exit 1; \
	done

.PHONY: all clean test
