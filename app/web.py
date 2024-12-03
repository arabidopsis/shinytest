from __future__ import annotations

import os

import subprocess
from dataclasses import dataclass


import click


@dataclass
class Runner:
    name: str
    cmd: list[str]
    directory: str = "."
    env: dict[str, str] | None = None
    showcmd: bool = False
    shell: bool = False

    def getenv(self) -> dict[str, str] | None:
        if not self.env:
            return None
        return {**os.environ, **self.env}

    def start(self) -> subprocess.Popen[bytes]:
        if self.showcmd:
            click.secho(" ".join(str(s) for s in self.cmd), fg="blue")

        return subprocess.Popen(  # type: ignore
            self.cmd,
            cwd=self.directory,
            env=self.getenv(),
            shell=self.shell,
        )


@click.command()
@click.option("-w", "--workers", default=4)
def run(workers: int):
    procs = [
        Runner(f"app{i}", ["uvicorn", "--uds", f"app{i}.sock", "app.asgi:app"])
        for i in range(1, workers + 1)
    ]

    todo = [p.start() for p in procs]

    try:
        for t in todo:
            t.wait()

    except KeyboardInterrupt:
        return


run()
