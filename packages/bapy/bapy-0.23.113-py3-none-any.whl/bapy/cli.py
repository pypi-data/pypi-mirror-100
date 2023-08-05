# -*- coding: utf-8 -*-
"""CLI Module."""
__all__ = (
    'package',
)

import typer
from typer import Argument
from typer import Option

from .core import CMD_INSTALL_POST_DEFAULT
from .core import GIT_VERSIONS
from .core import STDOUT
from .core import VENV_CLEAR
from .core import VENV_DEPS
from .core import Bump
from .core import Git
from .core import Line
from .core import ic
from .core import package
from .echo import green


@package.app.command(name='all')
def _all(
        ctx: typer.Context,
        bump: Bump = Option(Bump.PATCH, autocompletion=Git.bump_values, case_sensitive=False,
                            help='Version part to raise.'),
        clear: bool = Option(VENV_CLEAR, help='Upgrade an existing environment with the running Python.'),
        deps: bool = Option(VENV_DEPS, help='Update the base venv modules to the latest on PyPI.'),
        keep: int = Argument(GIT_VERSIONS, help='Tags to keep.'),
        message: str = Option(str, help='Commit message.'),
        stdout: bool = Option(STDOUT, help='Print progress messages.'),
):
    """Clean, build, upload to pypi/github and install it in site."""
    getattr(package, ctx.command.name)(bump=bump, clear=clear, deps=deps, keep=keep, message=message, stdout=stdout)


@package.app.command(name='version_delete')
def _delete(
        ctx: typer.Context,
        keep: int = Argument(GIT_VERSIONS, help='Tags to keep.'),
        stdout: bool = Option(STDOUT, help='Print progress messages.'),
):
    """Delete git tags."""
    getattr(package, ctx.command.name)(keep=keep, stdout=stdout)


@package.app.command(name='deps')
def _deps(ctx: typer.Context, stdout: bool = Option(STDOUT, help='Print progress messages.')):
    """Versions: installed and latest."""
    getattr(package, ctx.command.name)(stdout=stdout)


@package.app.command()
def install(post: bool = Option(CMD_INSTALL_POST_DEFAULT, help='Execute post install commands.')):
    """Install packages on site packages."""
    print(post)


@package.app.command()
def tests():
    print(package.file)


@package.app.command()
def v():
    """Version."""
    green(package.version.installed)


@package.app.command()
def venv(
        ctx: typer.Context,
        clear: bool = Option(VENV_CLEAR, help='Upgrade an existing environment with the running Python.'),
        deps: bool = Option(VENV_DEPS, help='Update the base venv modules to the latest on PyPI.'),
        stdout: bool = Option(STDOUT, help='Print progress messages.'),
):
    """Versions: installed and latest."""
    getattr(package, ctx.command.name)(clear=clear, deps=deps, stdout=stdout)


@package.app.command()
def versions():
    """Versions: installed and latest."""
    installed = package.version.installed
    latest = package.version.latest
    Line.alt(repo=package.repo, version=f'{installed=}, {latest=}')
