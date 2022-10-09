import click
from behaveExp import app, db
from behaveExp.models import Stock, User


@app.cli.command()
def init():
    db.drop_all()
    db.create_all()
    # db.session.add(Stock(name='A', value=100, date=0))
    # db.session.add(Stock(name='B', value=100, date=0))
    # db.session.add(Stock(name='C', value=100, date=0))
    #
    # db.session.add(User(value=1000, n_A=0, n_B=0, n_C=0, remain=1000, date=0))
    #
    # db.session.commit()
    click.echo("done!")