import time

from fastapi import Request


async def request_time_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    print(f"{process_time:.2f} ms")
    response.headers["X-Process-Time-ms"] = str(process_time)
    return response
