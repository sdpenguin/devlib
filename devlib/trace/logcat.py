import os
import re
import shutil

from devlib.trace import TraceCollector
from devlib.utils.android import LogcatMonitor

class LogcatCollector(TraceCollector):

    def __init__(self, target, regexps=None):
        super(LogcatCollector, self).__init__(target)
        self.regexps = regexps
        self._collecting = False
        self._prev_log = None

    def reset(self):
        """
        Clear Collector data but do not interrupt collection
        """
        if not self._monitor:
            return

        if self._collecting:
            self._monitor.clear_log()
        elif self._prev_log:
            os.remove(self._prev_log)
            self._prev_log = None

    def start(self):
        """
        Start collecting logcat lines
        """
        self._monitor = LogcatMonitor(self.target, self.regexps)
        if self._prev_log:
            # Append new data collection to previous collection
            self._monitor.start(self._prev_log)
        else:
            self._monitor.start()

        self._collecting = True

    def stop(self):
        """
        Stop collecting logcat lines
        """
        if not self._collecting:
            raise RuntimeError('Logcat monitor not running, nothing to stop')

        self._monitor.stop()
        self._collecting = False
        self._prev_log = self._monitor.logfile

    def get_trace(self, outfile):
        """
        Output collected logcat lines to designated file
        """
        # copy self._monitor.logfile to outfile
        shutil.copy(self._monitor.logfile, outfile)
