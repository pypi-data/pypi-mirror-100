# Setup Teardown Content Decorator

This is a simple package that aims to make adding setup and teardown to pytest flavored tests quick and painless.

# Usage
```
class PgSetupTeardown(ContextDecorator):
    def __init__(self, table, **kwargs):
        self.table = table
        self.__dict__.update(kwargs)

    def __enter__(self):
        self.session = db.session.new_session()

        self.session.query(self.table).delete()
        self.session.commit()
        return self

    def __exit__(self, typ, val, traceback):
        self.session = db.session.new_session()

        self.session.query(self.table).delete()
        self.session.commit()
```

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
