# North Star ---  A lookup service for forged fed ecosystem
# Copyright © 2021 Aravinth Manivannan <realaravinth@batsense.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sqlite3
import os

import click
from flask import current_app, g
from flask.cli import with_appcontext
from yoyo import read_migrations
from yoyo import get_backend


def get_db() -> sqlite3.Connection:
    """Get database connection"""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Apply database migrations"""
    db = str.format("sqlite:///%s" % (current_app.config["DATABASE"]))
    backend = get_backend(db)
    migrations = read_migrations("./migrations/")
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
        backend.commit()


@click.command("migrate")
@with_appcontext
def migrate_db_command():
    """Apply database migrations CLI handler"""
    init_db()
    click.echo("Migrations applied")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(migrate_db_command)
