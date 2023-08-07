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


```

    def setup(self):
        print("setup")
        self.start_time = time.time()

    def teardown(self):
        print("teardown")
        print("{}".format(time.time() - self.start_time))

    # decorator application example
    print("=============== Decorator Usage ===================")

    @SetupTeardown(setup=setup, teardown=teardown)
    def foo():
        print("inner")

    foo()

    print("=============== Context Manager Usage ===================")
    # contest manager application example
    with SetupTeardown(setup=setup, teardown=teardown):
        print("inner")
```
