from functools import wraps


def strict(func):
    @wraps(func)
    def wrapper(*args):
        annotations = func.__annotations__
        param_names = [name for name in annotations if name != "return"]
        for arg, name in zip(args, param_names):
            if type(arg) is not annotations[name]:
                raise TypeError

        return func(*args)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


# Тесты с assert (можно было бы использовать pytest.raises из сторонней библиотеки)
assert sum_two(1, 2) == 3

try:
    sum_two(1, 2.0)
except TypeError:
    print("TypeError was handled")

try:
    sum_two("1", 2)
except TypeError:
    print("TypeError was handled")

try:
    sum_two(True, 2)
except TypeError:
    print("TypeError was handled")
