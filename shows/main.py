import argparse
import sys

from rich.live import Live
from time import sleep

from .core import machine
from .component import header, layout, table


def parse_args(args):
    parser = argparse.ArgumentParser()
    input_arg, others_arg = parser.parse_known_args(args)
    input_arg = {k: v for k, v in vars(input_arg).items() if v is not None}
    return input_arg, others_arg


def main(arg=None):
    arg, others_arg = parse_args(sys.argv[1:]) if arg is None else parse_args(arg)
    mac = machine()
    console_layout = layout()
    console_layout["header"].update(header())
    console_layout["body"].update(table(mac.get_state()))
    try:
        with Live(console_layout, refresh_per_second=10, screen=True, transient=True):
            while True:
                console_layout["body"].update(table(mac.get_state()))
                sleep(0.1)
    except:
        mac.close()


if __name__ == "__main__":
    main()
