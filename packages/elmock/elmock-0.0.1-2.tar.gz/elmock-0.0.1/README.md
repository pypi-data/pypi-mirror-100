# elmock

A simple python package to help dynamic mock class creation.
This package is inspired by [golang testify/mock tool](https://github.com/stretchr/testify).

## How to use

You juste have to create a class to mock inheriting the `elmock.Mock` class. 
Then setup your test case using:

```python
def test_smtg():
    smtg_mock.on('some_method', return_value={'ok': True}, param1=198, some_date=datetime.now())
    some_test.use_smtg_some_method()
```
