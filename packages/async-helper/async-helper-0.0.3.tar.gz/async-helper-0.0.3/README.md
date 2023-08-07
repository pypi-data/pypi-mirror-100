# async-helper

*async-helper by [Sebastian Steins](https://seb.st/)*

Licence: MIT

## Usage
```
import time, random
from async_helper import first_parallel_result

def time_consuming_function(i):
    print("I consume a lot of time")
    time.sleep(random.randint(1, 10))
    return i

candidates = [
    lambda: time_consuming_function(1),
    lambda: time_consuming_function(2),
]

best_effort_result = first_parallel_result(candidates)

print(best_effort_result)
```

## Giving preference

```
import time, random
from async_helper import first_parallel_result

def time_consuming_function(i):
    print("I consume a lot of time")
    time.sleep(random.randint(1, 10))
    return i

candidates = [
    0, lambda: time_consuming_function(1),  # This callable will start immediately.
    1, lambda: time_consuming_function(2),  # This callable will start with `1` sec delay.
]

best_effort_result = first_parallel_result(candidates)

print(best_effort_result)
```

___

© 2021 [Sebastian Steins](https://seb.st/)