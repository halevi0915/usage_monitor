from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align

import readchar

class UI:
    def __init__(self, local_info):
        self.local_info = local_info
        self.layout = Layout()

        self.tabs = [
            "System",
            "Network",
            "Storage",
        ]

        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3),
        )

    def input_loop(self):
        while self.local_info.running:
            key = readchar.readkey()

            if key == "\x1b[C": self.local_info.current_tab = (self.local_info.current_tab + 1) % len(self.tabs)
            elif key == "\x1b[D": self.local_info.current_tab = (self.local_info.current_tab - 1) % len(self.tabs)
            elif key.lower() == "q":
                self.local_info.running = False
                break

#=============================================================#

    def build_header(self):
        text = Text()

        for i, tab in enumerate(self.tabs):
            if i == self.local_info.current_tab: style = "bold white on blue"
            else: style = "black on white"

            text.append(f" {tab} ", style=style)
            text.append(" ")

        return Panel(
            Align.center(text),
            title="Usage Monitor Client",
            border_style="cyan",
        )

#=============================================================#

    def general_panel(self):
        table = Table.grid(padding=(0, 2))

        table.add_column(style="cyan")
        table.add_column()

        if self.local_info.general_info is None:
            table.add_row("Not Connected")
        else:
            table.add_row("Hostname", self.local_info.general_info['hostname'])
            table.add_row("IP", self.local_info.general_info['ip_address'])
            table.add_row(f"OS", self.local_info.general_info['os'])
            table.add_row(f"Connected", style="green" if self.local_info.connected else "red")

        return Panel(
            table,
            title="General",
            border_style="green",
        )

    def system_panel(self):
        table = Table.grid(padding=(0, 2))

        table.add_column(style="cyan")
        table.add_column()

        if self.local_info.system_info is None:
            table.add_row("Not Connected")
        else:
            table.add_row("Core Count", f"{self.local_info.system_info['core_count']}")
            table.add_row("Uptime", f"{self.local_info.system_info['uptime']}")
            table.add_row("CPU Usage", f"{self.local_info.system_info['cpu_percent']}")
            table.add_row("CPU Freq", f"{self.local_info.system_info['cpu_freq']}")
            table.add_row("MEM Total", f"{self.local_info.system_info['virtual_memory_total']}")
            table.add_row("MEM Used", f"{self.local_info.system_info['virtual_memory_percent']}")

        return Panel(
            table,
            title="System",
            border_style="green",
        )

    def storage_panel(self):
        table = Table.grid(padding=(0, 2))

        table.add_column(style="cyan")
        table.add_column()

        if self.local_info.disk_info is None:
            table.add_row("Not Connected")
        else:
            for partition in self.local_info.disk_info['partitions']:
                table.add_row(f"{partition['device']}:", f"{partition['percent']}% - {partition['total']} GB")

        return Panel(
            table,
            title="Storage",
            border_style="green",
        )

#=============================================================#

    def build_body(self):
        pages = [
            self.general_panel(),
            self.system_panel(),
            self.storage_panel(),
        ]
        return pages[self.local_info.current_tab]

    def build_footer(self):
        return Panel(
            Align.center("[←] Previous Tab    [→] Next Tab    [Q] Quit"),
            border_style="cyan",
        )

    def update(self):
        self.layout["header"].update(self.build_header())
        self.layout["body"].update(self.build_body())
        self.layout["footer"].update(self.build_footer())