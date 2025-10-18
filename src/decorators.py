import functools
import time

from src.database import log_function_metrics


def performance_monitor(func):
    """
    A decorator that monitors function execution performance.

    Tracks execution time and status (completed/failed) of the decorated function,
    logging the metrics to the database for performance analysis and monitoring.

    Args:
        func (Callable): The function to be monitored

    Returns:
        Callable: The wrapped function with performance monitoring

    Example:
        >>> @performance_monitor
        ... def my_function():
        ...     # function logic
        ...     pass
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        error_message = None
        try:
            result = func(*args, **kwargs)
            status = "completed"
        except Exception as e:
            status = "failed"
            error_message = str(e)
            raise
        finally:
            end_time = time.time()
            execution_time = end_time - start_time

            # Log to database
            log_function_metrics(
                function_name=func.__name__,
                execution_time=execution_time,
                status=status,
                error_message=error_message,
            )

        return result

    return wrapper
