hxarc_lxp
========

cli for hxarc scripts


overview
==========

You will need uv and ruff. I've installed all of them with homebrew.

tldr;

    $> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ...
    $> brew install uv ruff

    # clone this report
    $> git clone https://github.com/harvardx/hxarc_lxp.git

    # use uv to install dependencies and run you cli and tests
    $> cd hxarc_lxp

    # install dependencies, creating a local .venv
    $> uv sync

    # activates the venv and runs your cli
    $> uv run hxarc_lxp --help

    # create your unit tests with pytest and run
    $> uv sync --extra test
    $> uv run pytest -v tests

    # lint and format using ruff
    $> ruff check
    $> ruff format --diff  # just display the changes
    $> ruff format         # changes your code for real


- https://brew.sh
- https://docs.astral.sh/uv/getting-started/installation/
- https://docs.astral.sh/ruff/installation/
- https://click.palletsprojects.com/en/stable/


---eop

