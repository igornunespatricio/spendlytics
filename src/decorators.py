import functools
import time

from src.database import log_function_metrics


def performance_monitor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            status = "completed"
        except Exception as e:
            status = f"failed: {str(e)}"
            raise
        finally:
            end_time = time.time()
            execution_time = end_time - start_time

            # Log to database
            log_function_metrics(
                function_name=func.__name__,
                execution_time=execution_time,
                status=status,
            )

        return result

    return wrapper
