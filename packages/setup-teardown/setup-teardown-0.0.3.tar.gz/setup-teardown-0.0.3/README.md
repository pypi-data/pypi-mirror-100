# Setup Teardown Content Decorator

This is a simple package that aims to make adding setup and teardown to pytest flavored tests quick and painless.

# Installation
```
python3 -m pip install setup-teardown
```

# Decorator Usage

## Custom Database Class
```
from setup_teardown import SetupTeardown

class PgSetupTeardown(SetupTeardown):
    def __init__(self, table, **kwargs):
        self.table = table
        self.__dict__.update(kwargs)

    def __enter__(self):
        # Perform test setup
        self.session = db.session.new_session()
        self.session.query(self.table).delete()
        self.session.commit()
        return self

    def __exit__(self, typ, val, traceback):
        # Perform test teardown
        self.session.query(self.table).delete()
        self.session.commit()
```

## Actual test
```
class TestHandlerDatabaseRequired:
    @SetupTeardown(table="table_name")
    def test_handler_success(self, mock_datetime):
        """
        Example of using the SetupTeardown ContextDecorator with arbitrary setup and teardown
        """
        # execute the test
        pass
```

# Context manager usage

```

    def setup(self):
        session = db.session.new_session()
        session.query(self.table).delete()
        session.commit()

    def teardown(self):
        session = db.session.new_session()
        session.query(self.table).delete()
        session.commit()

    # contest manager application example
    with SetupTeardown(setup=setup, teardown=teardown):
        print("inner")
```
