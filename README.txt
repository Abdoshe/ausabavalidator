ausabavalidator is a validator for Australian Banker Association (ABA) files released under the GPLv3.


Dependencies
------------
Requires Python 3 and bitarray.

Tests requires pytest.  No tests exist in this branch, they'll be added before merging back to master.

To install bitarray: pip install bitarray
To install pytest: pip install pytest


Usage
-----
At this point the ABA filename is hardcoded in validator.py, this will change.

There are plans to add a graphical user interface once file validation is done.


To run the validator: python3 validator.py

To run the tests: pytest testall.py
