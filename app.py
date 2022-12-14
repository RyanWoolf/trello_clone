from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:password123@127.0.0.1:5432/trello'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    status = db.Column(db.String)
    priority = db.Column(db.String)

class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'status', 'priority', 'date')
        ordered = True


# Define a custom CLI (terminal) command
@app.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@app.cli.command('seed')
def seed_db():
    cards = [
        Card(
            title = 'Start the project',
            description = 'Stage 1 - Create the database',
            status = 'To Do',
            priority = 'High',
            date = date.today()
        ),
        Card(
            title = "SQLAlchemy",
            description = "Stage 2 - Integrate ORM",
            status = "Ongoing",
            priority = "High",
            date = date.today()
        ),
        Card(
            title = "ORM Queries",
            description = "Stage 3 - Implement several queries",
            status = "Ongoing",
            priority = "Medium",
            date = date.today()
        ),
        Card(
            title = "Marshmallow",
            description = "Stage 4 - Implement Marshmallow to jsonify models",
            status = "Ongoing",
            priority = "Medium",
            date = date.today()
        )
    ]

    db.session.add_all(cards)
    db.session.commit()
    print('Tables seeded')


@app.cli.command('all_cards')
def all_cards():
    # Legacy way
    # select * from cards;
    cards = Card.query.all()
    print(cards[0].__dict__)

@app.cli.command('all_cards_new')
def all_cards():
    # select * from cards;
    # stmt = db.select(Card).where(Card.status == 'To Do')
    stmt = db.select(Card).filter_by(status='Ongoing').order_by(Card.title)
    print(stmt)
    cards = db.session.scalars(stmt)
    for card in cards:
        print(card.status, card.title)

@app.cli.command('all_cards2')
def all_cards():
    # Legacy way
    # select * from cards limit 1;
    cards = Card.query.first()
    print(cards.__dict__)

@app.cli.command('first_card')
def first_card():
    stmt = db.select(Card).limit(1)
    print(stmt)
    card = db.session.scalar(stmt)
    print(card.__dict__)

@app.cli.command('count_ongoing')
def count_ongoing():
    stmt = db.select(db.func.count()).select_from()
    cards = db.session.scalars(stmt)



@app.route('/')
def index():
    return "Hello World!"


@app.route('/cards/')
def all_cards():
    stmt = db.select(Card).order_by(Card.priority.desc(), Card.title)
    cards = db.session.scalars(stmt)
    return CardSchema(many=True).dump(cards)
