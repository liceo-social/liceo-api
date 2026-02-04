import functools
import inspect
from logging import getLogger
from typing import Any, Callable, TypeVar

from liceo.labs.db.core import Repository

A = TypeVar("A", bound=Any)

logger = getLogger("poirot.core")


def sql(mapper: Callable[..., A] = lambda row: row):
    def decorator(func: Callable[..., Any]) -> Callable[..., A]:
        @functools.wraps(func)
        def wrapper(self: Repository, *args: Any, **kwargs: Any) -> A:
            sql_file = self.resolve_sql_file(func)
            sql_content = ""

            if not sql_file.exists():
                raise Exception("SQL file not found!")

            with sql_file.open() as file_content:
                sql_content = "\n".join(file_content.readlines())

            if not sql_content:
                raise Exception("No SQL content found in file!")

            if kwargs and len(args) > 0:
                raise Exception("Can't decide whether we should use args or kwargs!")

            if kwargs:
                logger.debug("kwargs {}".format(str(kwargs)))

            if len(args) > 0:
                sql_args = inspect.getfullargspec(func).args
                sql_args.remove("self")
                kwargs = {next[0]: next[1] for next in zip(sql_args, args)}

            if func.__name__.startswith("find_all_"):
                logger.debug("executing find_all___ query")
                all = self._get_connection().all(sql=sql_content, params=kwargs)
                return mapper([next for next in all])

            if func.__name__.startswith("find_") or func.__name__.startswith("insert_"):
                logger.debug("executing find___ query")
                one = self._get_connection().one(sql=sql_content, params=kwargs)
                return mapper(one)

            if func.__name__.startswith("is_"):
                logger.debug("executing is___ query")
                one = self._get_connection().one(sql=sql_content, params=kwargs)
                return mapper(one)

            logger.debug("executing execute___ query")
            return self._get_connection().execute(sql=sql_content, params=kwargs)

        return wrapper

    return decorator
