import threading
from typing import Callable, List, TypeVar

X = TypeVar("X")
Y = TypeVar("Y")


def if_not_none(p: X | None, fn: Callable[[X], Y]) -> Y | None:
    if p is not None:
        return fn(p)
    return None


def flatten(xss: List[List[X]]) -> List[X]:
    return [x for xs in xss for x in xs]


def singleton(cls):
    """
    A thread-safe decorator to ensure a class follows the Singleton
    design pattern.

    This decorator allows a class to have only one instance throughout
    the application. If the instance does not exist, it will create one;
    otherwise, it will return the existing instance. This implementation
    is thread-safe, ensuring that only one instance is created even in
    multithreaded environments.

    https://medium.com/@rspatel031/a-comprehensive-guide-to-the-thread-safe-singleton-pattern-in-python-e47682e300da

    :param: cls (type): The class to be decorated as a Singleton.
    :return: function: A function that returns the single instance of the
             class.
    """
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs) -> object:
        """
        Return a single instance of the decorated class, creating it
        if necessary.

        This function ensures that only one instance of the class exists.
        It uses a thread-safe approach to check if an instance of the class
        already exists in the `instances` dictionary. If it does not exist,
        it creates a new instance with the provided arguments. If it does
        exist, it returns the existing instance.

        :param: *args: Variable length argument list for the class constructor.
        :param: **kwargs: Arbitrary keyword arguments for the class constructor.
        :return: object: The single instance of the class.
        """
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]

    return get_instance
