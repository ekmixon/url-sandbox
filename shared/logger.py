'''
    __G__ = "(G)bd249ce4"
    shared -> logger
'''


from os import path, environ
from sys import stdout
from datetime import datetime
from tempfile import gettempdir
from contextlib import contextmanager
from logging import DEBUG, Handler, WARNING, getLogger
from shared.settings import json_settings, defaultdb
from shared.mongodbconn import add_item_fs, add_item, update_task, update_task_by_uuid


class TerminalColors:
    '''
    Colors (add more)
    '''
    Restore = '\033[0m'
    Black = "\033[030m"
    Red = "\033[91m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Purple = "\033[35m"
    Cyan = "\033[36m"
    White = "\033[37m"


GREEN_X = f'{TerminalColors.Green}X{TerminalColors.Restore}'
YELLOW_ARROW = f'{TerminalColors.Yellow}>{TerminalColors.Restore}'
EXCLAMATION_MARK = f'{TerminalColors.Yellow}!{TerminalColors.Restore}'
RED_ARROW = f'{TerminalColors.Red}>{TerminalColors.Restore}'


@contextmanager
def ignore_excpetion(*exceptions):
    '''
    catch excpetion
    '''
    try:
        yield
    except exceptions as error:
        #print("{} {} {}".format(datetime.utcnow(), EXCLAMATION_MARK, error))
        pass


def combine_2_dict(a, b):
    z = a.copy()
    return z.update(b)


def setup_task_logger(parsed):
    '''
    setup the dynamic logger for the task
    '''
    log_string(f"Setup task {parsed['task']} logger", "Yellow")
    temp_dict = parsed.copy()
    temp_dict.update({"start": datetime.utcnow(), "end": None, "logs": []})
    add_item(defaultdb["dbname"], defaultdb["taskdblogscoll"], temp_dict)


def cancel_task_logger(task):
    '''
    setup the dynamic logger for the task
    '''
    log_string(f"Closing task {task} logger", "Yellow")
    update_task_by_uuid(defaultdb["dbname"], defaultdb["taskdblogscoll"], task, {"end": datetime.utcnow()})


def log_string(_str, color=None, task=None):
    '''
    output str with color and symbol (they are all as info)
    '''
    ctime = datetime.utcnow()
    if _str.isspace() or len(_str) == 0:
        _str = "None"
    if task is None:
        add_item(defaultdb["dbname"], defaultdb["alllogscoll"], {'time': ctime, 'message': _str})
    else:
        update_task(
            defaultdb["dbname"],
            defaultdb["taskdblogscoll"],
            task,
            f"{ctime} > {_str}",
        )

    print(f"{_str} {task}")
    stdout.flush()
