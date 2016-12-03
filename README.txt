ausabavalidator is a validator for Australian Banker Association (ABA) files.

Requires Python 3 and pytest for tests.  All tests currently pass.

At this point the ABA filename is hardcoded in validator.py, this will change.

There are plans to add a graphical user interface once file validation is done.


To run the validator: python3 validator.py

To run the tests: pytest testall.py


To install pytest: pip install pytest
