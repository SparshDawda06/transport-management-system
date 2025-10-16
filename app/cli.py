import os
import pymysql
from flask import current_app
from flask.cli import with_appcontext
import click


@click.command("create-db")
@with_appcontext
def create_db():
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    db_name = os.getenv("MYSQL_DB", "transport_mgmt")

    click.echo(f"Connecting to MySQL at {host}:{port} as {user}...")
    conn = pymysql.connect(host=host, port=port, user=user, password=password)
    conn.autocommit(True)
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            click.echo(f"Database `{db_name}` ensured.")
    finally:
        conn.close()

    uri = current_app.config.get("SQLALCHEMY_DATABASE_URI")
    click.echo(f"SQLAlchemy URI set to: {uri}")


@click.command("seed-data")
@with_appcontext
def seed_data():
    """Populate the database with sample data for all entities."""
    from app.sample_data import create_sample_data
    
    click.echo("🌱 Seeding database with sample data...")
    create_sample_data()
    click.echo("✅ Sample data seeding completed!")
