#!/usr/bin/env python3
# -*- encoding: utf8 -*-

import sys
import os
import math
from collections import defaultdict
from time import sleep, time, ctime
from dataclasses import dataclass
from string import Formatter


def get_format_args(s):
    formatter = Formatter()
    res = [(format_arg, format_typ) for _, format_arg, format_typ, _ in
           formatter.parse(s) if format_arg is not None]
    return res


def apply_format(value, format_typ=''):
    complete_str = "{0:" + format_typ + "}" if format_typ else "{0}"
    complete_str = complete_str.format(value)
    return complete_str


@dataclass
class ProgressBar:
    """
    :param length: The length of the process.
    :param bins:   The number of bins will be displayed.
    :param format: The string format of the progress bar.
    :param bchr:   The basic character used to indicate
                   that the progression is passed.
    :param lchr:   The character used to open bins.
    :param rchr:   The character used to close bins.
    :param pchr:   The character used for progression indication.
    :param empt:   The character used to indication
                   that the progression not passed yet.

    :type length: `int`
    :type bins:   `int`
    :type format: `str`
    :type bchr:   `str`
    :type lchr:   `str`
    :type rchr:   `str`
    :type pchr:   `str`
    :type empt:   `str`
    """
    COUNTER = 0

    name: str = ''
    length: int = 0
    progress: int = 0
    logger: str = ''
    state: dict = None

    show_remaining_time: bool = False
    show_duration: bool = False
    start_time: float = None

    bchr: str = '='
    lchr: str = '['
    rchr: str = ']'
    pchr: str = '>'
    empt: str = '.'
    bins: int = 10
    format: str = ("{logger} {progressbar}"
                   " {percent:6.2f}% -"
                   " {progress}/{length} -"
                   " [{duration} < {remaining} |"
                   " {iter_rate:.2f}its/sec] ")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._log_format = kwargs.get('log_format')
        self._log_args = kwargs.get('log_args', {})
        self._log_type = {}
        self.state = {}

        self._pbm: PBM = None
        self.reset()

        self.name = kwargs.get('name')
        if not self.name:
            self.name = f'pb{self.__class__.COUNTER}'
            self.__class__.COUNTER += 1

    @property
    def pbm(self):
        return self._pbm

    @pbm.setter
    def pbm(self, instance):
        if not isinstance(instance, PBM):
            raise TypeError("The instance must be a PBM instance.")
        self._pbm = instance

    def get_progress_percent(self):
        """Function to compute and returns progress percent

        :rtype: float
        """
        return self.progress * 100 / self.length if self.length > 0 \
            else float('inf')

    def step(self, value):
        """Function to make a step, update and print state

        :type value: `int`
        """
        self.progress += value
        self._pbm.update()
        self._pbm.print_states()

    def log_format(self, string, **kwargs):
        formatters = get_format_args(string)
        for name, format_typ in formatters:
            if name not in kwargs:
                raise AttributeError(f"Value of `{name}` missing.")
            self._log_args[name] = kwargs[name]
            self._log_type[name] = format_typ
        self._log_format = string

    def log(self, *message, **kwargs):
        if self._log_args:
            self._log_args.update(**kwargs)
            new_message: str = self._log_format
            for name, value in self._log_args.items():
                typ = self._log_type[name]
                formatted_value = apply_format(value, typ)
                old = "{" + f"{name}"
                old += (":" + typ if typ else "") + "}"
                new_message = new_message.replace(old, formatted_value)
            self.logger = new_message
        else:
            self.logger = " ".join(message) if message else ''

        self._pbm.update()
        self._pbm.print_states()

    def full(self):
        return self.progress > self.length

    def reset(self):
        """Function to reset the progress counter"""
        self.start_time = time()
        self.progress = 0
        self.state["logger"] = self.logger
        self.state["progressbar"] = ''
        self.state["percent"] =  0.0
        self.state["progress"] = "--"
        self.state["length"] = "--"
        self.state["elapsed"] = "--:--:--"
        self.state["remaining"] = "--:--:--"
        self.state["iter_rate"] = 0.0


def _format_time(timestamps, str_format=None):
    """Function to convert milliseconds to hh:mm:ss:millis

    :type timestamps: `float`
    :type str_format: `str`

    :rtype: `str`
    """
    if not str_format:
        str_format = (
            "{days:03d}:{hours:02d}:{mins:02d}:{secs:02d}.{millis:03d}")

    sec = int(timestamps)
    millis = int((timestamps - sec) * 1000)

    mins = sec // 60
    sec = sec % 60

    hours = mins // 60
    mins = mins % 60

    days = hours // 24
    hours = hours % 24
    res = str_format.format(
        days=days, hours=hours, mins=mins, secs=sec, millis=millis)
    return res


class PBM(list):
    """Progress bar manager"""
    CIRCLE = ['-', '\\', '|', '/']

    def __init__(self, sep=None, time_format=None):
        super().__init__()
        self._time_format = time_format
        self._sep = sep

        if not self._sep:
            self._sep = '\t'

        self._crid = 0
        self._crate = 0.1
        self._circle_time = time()

    def append(self, __object):
        if not isinstance(__object, ProgressBar):
            raise TypeError(
                f"The object added is not instance of a progress bar.")
        __object.pbm = self
        super().append(__object)

    def add(self, pb_ins):
        self.append(pb_ins)

    def update(self):
        """Function to perform one step"""
        for i in range(self.__len__()):
            pbar: ProgressBar = self[i]
            if pbar.full():
                continue
            duration = time() - pbar.start_time
            if duration != 0.0:
                rate = pbar.progress / duration
            else:
                rate = float('inf')

            if rate != 0.0:
                remaining = (pbar.length - pbar.progress) / rate
                # convert to millisecond
                # remaining = int(remaining * 1000)
                str_rem = _format_time(remaining, self._time_format)
            else:
                str_rem = "--:--:--"

            n_bins = math.floor(pbar.progress * pbar.bins / pbar.length) \
                if pbar.length > 0 else 0
            done = (n_bins == pbar.bins)
            pchr = pbar.pchr if not done else pbar.bchr
            pbar.state['logger'] = pbar.logger
            pbar.state['percent'] = pbar.get_progress_percent()
            pbar.state['remaining'] = str_rem
            pbar.state['duration'] = _format_time(duration)
            pbar.state['progressbar'] = (
                f"{pbar.lchr}{pbar.bchr * n_bins}{pchr}"
                f"{pbar.empt * (pbar.bins - n_bins)}{pbar.rchr}")
            pbar.state['progress'] = pbar.progress
            pbar.state['length'] = pbar.length
            pbar.state['iter_rate'] = rate

    def _next_circle(self):
        curr_time = time()
        if curr_time - self._circle_time >= self._crate:
            self._crid = (self._crid + 1) % len(self.CIRCLE)
            self._circle_time = curr_time
        next_circle = self.CIRCLE[self._crid]
        return next_circle

    def print_states(self):
        pstrings = []
        for i in range(self.__len__()):
            pbar = self[i]
            if not pbar.state:
                continue
            string_f = pbar.format
            pstrings.append(string_f.format(**pbar.state))
        if not pstrings:
            return
        circle = self._next_circle()
        str_result = ' [' + circle + '] ' + self._sep.join(pstrings)

        print("\033[2K", end='\r')
        print(str_result, end=' ', flush=True)

    def resume(self, message):
        """ Function to finalise the progress counting with a message

        :param message: The resume messages.
        :type message: `str`
        """
        data = {}
        pbs = iter(self)
        for pb in pbs:
            for attr_name, value in pb.state.items():
                data[f"{pb.name}_{attr_name}"] = value
        message = message.format(**data)

        # Clear the progress bar,
        # and print the message received by argument.
        print("\033[2K", end='\r')
        print(message, flush=True)

    def reset(self):
        for i in range(self.__len__()):
            self[i].reset()


ERR = "\033[91mERR\033[0m: "


def file_names(dir_path):
    """
    Returns file name list.
    """
    results = list(os.walk(dir_path))
    files = []
    for res in results:
        r, _, f = res
        files_found = [os.path.join(r, x) for x in f]
        files.extend(files_found)
    returned_info = []
    for f in files:
        file_name = os.path.basename(f)
        file_path = f
        ti_c = os.path.getctime(f)
        ti_c = ctime(ti_c)  # convert time in second into timestamps;
        returned_info.append((file_name, file_path, ti_c))
    return returned_info


def main():
    dir_path = None
    remove = False
    if len(sys.argv) > 1:
        dir_path = sys.argv[1]
    if len(sys.argv) > 2:
        remove = (sys.argv[2] == '-r')

    if not dir_path:
        print(ERR + "No directory path provided.")
        exit(1)
    if not os.path.isdir(dir_path):
        print(ERR + f"No such directory provided at {dir_path}")
        exit(1)

    file_paths = file_names(dir_path)
    fp_length = len(file_paths)

    pbm = PBM()
    pb = ProgressBar()
    pb.name = "progress"
    pb.length = fp_length
    pb.bins = 32
    pb.log_format("{filename:32s}", filename="")
    pbm.add(pb)

    existing_files = {}
    files_duplicated = []
    for i, (file_name, file_path, c_ti) in enumerate(file_paths):
        pb.log(filename=file_name)
        if file_name not in existing_files:
            existing_files[file_name] = (file_path, c_ti)
            pb.step(1)
            continue
        path, ct = existing_files[file_name]
        if c_ti > ct:
            files_duplicated.append(file_path)
        else:
            files_duplicated.append(path)
            existing_files[file_name] = (file_path, c_ti)
        if remove:
            os.remove(file_path)
        pb.step(1)

    pbm.resume(
        f"+ \033[92m{fp_length}\033[0m files analysed, \n"
        f"- \033[91m{len(files_duplicated)}\033[0m duplications found"
        + (" and removed." if remove else "."))

    # Show files list duplicated
    if files_duplicated:
        print("\nHere is list of files duplicated:")
        for file_path in files_duplicated:
            print("  \033[91m-*-\033[0m", file_path)


if __name__ == '__main__':
    try:
        main()
        exit(0)
    except KeyboardInterrupt:
        print("Bye!")
        exit(125)
