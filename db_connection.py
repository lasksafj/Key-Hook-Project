from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

"""Small utility function whose only job is to manage the connection to the database."""

# This is the URL to my local PostgresSql database.
"""The breakdown of the fields in the URL and what they signify follows:
postgresql -        The relational database dialect.  Note that 'postgres' is no longer 
                    supported by sqlalchemy as a name for this dialect.
psycopg2 -          The database API employed.  It turns out that the default is psycopg2,
                    but I prefer to be explicit.  One less chance of failure.
postgres            The ID used for logging into the database.  When you installed PostgreSQL you 
                    automatically created a postgres account, and the installer prompted you for
                    the password at that time.  Normally, you would create a separate user, with
                    far fewer privileges than the postgres account, and use that to log into the
                    database.  But I'm going to keep it simple for now.
<postgres pwd>      The password that you gave the PostgreSQL installer.  It's the same password that
                    you used when you set up DataGrip to access the PostgreSQL database.
@localhost          Designates that the PostgreSQL server is hosted on the same machine as this application.
<your port>         The default port # for PostgreSQL is 5432, so that is probably what you want to have
                    here.  But just in case you are using something else, I made this a "variable".
postgres            The name of the database."""
db_url = "postgresql+psycopg2://postgres:123qwe@localhost:5432/postgres"

# Create the database engine that we will use for all of our work.  This does not actually connect
# just yet, it is more like a connection prototype that we actually fire up when we create a session.
engine = create_engine(db_url, pool_size=5, pool_recycle=3600)

# Create a session factory using the engine that we just defined.
session_factory = sessionmaker(bind=engine)

# I am told that this next line contributes to making the code thread safe since the
# scoped_session returns the same Session every time it's called for any given thread.
# I personally don't expect to try to run concurrent threads from Python using
# SQLAlchemy anytime soon, but if I do, I'll be ready!
Session = scoped_session(session_factory)
