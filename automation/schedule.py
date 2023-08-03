"""
schedule.py

Initializes satellite states and parameters for automation, and provides functions for scheduling
help.

Author(s): Adyn Miles
"""

from datetime import datetime

class Scheduler(set):
    def __getattr__(self, name):
        """
        Initializes the states for the automation program.

        Args:
            None

        Returns:
            None
        """
        if name in self:
            return name
        raise AttributeError

    def curr_time(self):
        """
        Gathers current time, converts to epoch time format.

        Args:
            None

        Returns:
            curr_time: Time formatted in epoch structure (YYDDD.DDDDDDDDD)
        """

        now = datetime.now()
        curr_year = int(str(now.year)[-2:])
        curr_dayofyear = now.timetuple().tm_yday
        if curr_dayofyear < 100:
            curr_dayofyear = "0" + str(curr_dayofyear)
        else:
            curr_dayofyear = str(curr_dayofyear)
        fractional_time = (now.hour + (now.minute/60))/24
        epoch_time = str(curr_year) + curr_dayofyear + "." + str(fractional_time)[2:]
        return epoch_time

    def epoch_time(self, time):
        """
        Converts input time to epoch time format.

        Args:
            None

        Returns:
            curr_time: Time formatted in epoch structure (YYDDD.DDDDDDDDD)
        """

        curr_year = int(str(time.year)[-2:])
        curr_dayofyear = time.timetuple().tm_yday
        if curr_dayofyear < 100:
            curr_dayofyear = "0" + str(curr_dayofyear)
        else:
            curr_dayofyear = str(curr_dayofyear)
        fractional_time = (time.hour + (time.minute/60))/24
        epoch_time = str(curr_year) + curr_dayofyear + "." + str(fractional_time)[2:]
        return epoch_time


    