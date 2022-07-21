import datetime
import traceback
import os

jwt_secret = os.getenv("JWT_SECRET")

# For writing logs into a log file. Makes it easy to debug api
def logs(endpoint: str) -> None:
    with open("log.tx", "a") as f:
        f.write(
            f"{'='*50} \n{datetime.datetime.now()} ERROR:: {endpoint} \n {traceback.format_exc()} \n"
        )
