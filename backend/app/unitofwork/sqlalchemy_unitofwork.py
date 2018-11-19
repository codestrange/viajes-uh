from flask import current_app
from . import UnitOfWork


class UnitOfWorkSQLAlchemy(UnitOfWork):

    def commit(self):
        current_app.db.session.commit()
