import os
import sys
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command

# Load environment variables from .env
load_dotenv()

def get_alembic_config() -> Config:
    """Load Alembic configuration and set the DB URL from .env."""
    alembic_cfg = Config("alembic.ini")

    return alembic_cfg


def main():
    async_db_url = os.getenv("DATABASE_URL")
    sync_db_url = async_db_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
    os.environ["DATABASE_URL"] = sync_db_url

    """Handle Alembic commands."""
    alembic_cfg = get_alembic_config()

    if len(sys.argv) < 2:
        print("Usage: python manage.py [command] [options]")
        print("Commands: upgrade, downgrade, revision, history, current, heads")
        sys.exit(1)

    cmd = sys.argv[1]

    # Handle Alembic commands
    if cmd == "upgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "head"
        command.upgrade(alembic_cfg, revision)

    elif cmd == "downgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "-1"
        command.downgrade(alembic_cfg, revision)

    elif cmd == "revision":
        message = sys.argv[2] if len(sys.argv) > 2 else "New migration"
        autogenerate = "--autogenerate" in sys.argv
        command.revision(alembic_cfg, message=message, autogenerate=autogenerate)

    elif cmd == "history":
        command.history(alembic_cfg)

    elif cmd == "current":
        command.current(alembic_cfg)

    elif cmd == "heads":
        command.heads(alembic_cfg)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
