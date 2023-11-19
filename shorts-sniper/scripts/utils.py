import sys
import inspect
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def get_size_in_mb(variable):
    size_in_bytes = sys.getsizeof(variable)
    size_in_kb = size_in_bytes / 1024
    size_in_mb = size_in_kb / 1024
    return size_in_mb
