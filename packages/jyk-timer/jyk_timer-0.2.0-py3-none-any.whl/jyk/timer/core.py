import datetime
import logging
from functools import wraps

log = logging.getLogger(__name__)


class TimeFormat:
    YmdHMS = "%Y%m%d%H%M%S"
    YmdHMSDash = "%Y-%m-%d-%H-%M-%S"


class TimeUnit:
    H = 'h'
    M = 'm'
    S = 's'


class Timer(object):
    def __init__(self, ft=TimeFormat.YmdHMS):
        self.format = ft
        self.time_0 = None
        self.start_time = None
        self.end_time = None

    def start(self):
        now = datetime.datetime.now()
        if self.time_0 is None:
            self.time_0 = now

        self.start_time = now

    def end(self):
        self.end_time = datetime.datetime.now()

    def elapse(self, unit=TimeUnit.S, precision=4, from_origin=False):
        if self.start_time is None:
            raise Exception('call Timer().start() first')
        if self.end_time is None:
            raise Exception('call Timer().end() first')

        end_time = self.end_time
        if from_origin:
            start_time = self.time_0
        else:
            start_time = self.start_time

        dt = (end_time - start_time).total_seconds()

        if unit == TimeUnit.S:
            return round(dt, precision)

        if unit == TimeUnit.M:
            return round(dt / 60, precision)

        if unit == TimeUnit.H:
            return round(dt / 3600, precision)

    def now(self):
        return datetime.datetime.now().strftime(self.format)


def timer(fn, name=None, unit=TimeUnit.S, precision=4):
    if name is None:
        name = fn.__name__
        
    @wraps(fn)
    def measure_cost(*args, **kwargs):
        start = datetime.datetime.now()
        result = fn(*args, **kwargs)
        end = datetime.datetime.now()

        dt = (end - start).total_seconds()
        if unit == TimeUnit.S:
            udt = round(dt, precision)
        elif unit == TimeUnit.M:
            udt = round(dt / 60, precision)
        else:
            udt = round(dt / 3600, precision)
        log.warning(
            f"[+]: {name} took {udt}{unit}")
        return result

    return measure_cost