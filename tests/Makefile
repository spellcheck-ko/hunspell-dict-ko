TESTS = $(sort $(wildcard *.test))

all: test

test:
	@for T in $(TESTS); do \
		echo "Testing $$T..."; \
		python3 runtest.py ../ko $$T; \
	done

autopkgtest:
	@for T in $(TESTS); do \
		echo "Testing $$T..."; \
		python3 runtest.py ko $$T; \
	done

.PHONY: all clean test
