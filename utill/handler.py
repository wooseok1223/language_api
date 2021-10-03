import time
from functools import wraps
from flask import jsonify
from app.exceptions import (
    Exception
)


def api_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        payloads = {}
        status_code = 200
        try:
            result = func(*args, **kwargs)
            payloads.update({"success": 1, "result": result})
        except Exception as e:
            payloads.update(
                {
                    "success": 0,
                    "errorCode": e.error_code,
                    "errorMessage": e.error_message
                }
            )
            status_code = e.status_code

        if kwargs:
            payloads.update(kwargs)

        elapsed_time = round((time.time() - start_time) * 1000, 1)
        payloads["elapsed_time"] = f"{elapsed_time}ms"

        return jsonify(payloads), status_code

    return wrapper
