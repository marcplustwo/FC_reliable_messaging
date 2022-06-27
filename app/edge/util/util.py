from datetime import datetime

def get_ts() -> float:
  return datetime.timestamp(datetime.now())
