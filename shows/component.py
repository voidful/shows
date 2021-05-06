from datetime import datetime
from rich import box
from rich.align import Align
from rich.layout import Layout
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def layout() -> Layout:
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body"),
    )
    return layout


def header():
    message = Text.from_markup(
        "Machine states", justify='center'
    )
    return Panel(message, style="white bright_blue")


def footer():
    message = Text.from_markup(
        datetime.now().ctime().replace(":", "[blink]:[/]"), justify='right'
    )
    return Panel(message)


def table(info):
    table = Table.grid(expand=False)

    table.add_column("Hardware", justify="left", style="cyan")
    table.add_column("product", justify="right", style="magenta")
    table.add_column("Status", justify="left", style="green")
    table.add_column("Num", justify="right", style="magenta", width=3)
    for i, cpu in enumerate(info['cpus']):
        usage = str(cpu.get('usage', '0')) + '%'
        table.add_row("CPU", Padding(cpu.get('name', ''), (0, 1)), usage, str(i))

    for i, gpu in enumerate(info['gpus']):
        usage = str(gpu.get('usage', '0')) + '%'
        memory = str(gpu.get('men_used', '0')) + '/' + str(gpu.get('men_total', '0'))
        temp = str(gpu.get('temp', '0')) + '°'
        table.add_row("GPU", Padding(gpu.get('name', ''), (0, 1)), usage, str(i))
        table.add_row("GPU", "", memory, str(i))
        table.add_row("GPU", "", temp, str(i))

    for i, disk in enumerate(info['disk']):
        usage = int(disk.get('used', 0) / disk.get('total', 1) * 100)
        usage = str(usage) + '%'
        table.add_row("DISK", Padding("disk " + str(i), (0, 1)), usage, "")

    ram_usage = int(info['mem'].get('used', 0) / info['mem'].get('total', 1) * 100)
    ram_usage = str(ram_usage) + '%'
    table.add_row("RAM", Padding("ram", (0, 1)), ram_usage, "")

    table.add_row("NET", Padding("received", (0, 1)), str(info['net'].get('in', '0')) + "MB", "")
    table.add_row("NET", Padding("sent", (0, 1)), str(info['net'].get('out', '0')) + "MB", "")

    return Panel(
        Align.center(table),
        box=box.ROUNDED,
        border_style="bright_blue",
    )
