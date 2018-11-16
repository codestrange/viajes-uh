from os import getenv
from os.path import abspath, dirname, join
from coverage import coverage
from flask_script import Manager, Shell

# Coverage debe empezar antes de las importaciones
# de los módulos de las aplicación
COV = coverage(branch=True, include='app/*')
COV.start()

from app import create_app
from app import db
from app.models.user import User

app = create_app(getenv('FLASK_CONFIG') or 'default')


@app.cli.command()
def test():
    """Run the unit tests."""
    from unittest import TestLoader, TextTestRunner
    tests = TestLoader().discover('tests')
    TextTestRunner(verbosity=2).run(tests)
    COV.stop()
    COV.save()
    print('\nCoverage Summary:')
    COV.report()
    basedir = abspath(dirname(__file__))
    covdir = join(basedir, 'tmp/coverage')
    COV.html_report(directory=covdir)
    print(f'HTML version: file://{covdir}/index.html')
    COV.erase()


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User)


# Shell de flask_script con IPython
manager = Manager(app)
manager.add_command(Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
