from flask import Blueprint, request, jsonify
from twilio.rest import Client
import random
from .models import db, User, Game

routes = Blueprint('routes', __name__)

# Twilio configuration
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_client = Client(account_sid, auth_token)
verification_codes = {}

@routes.route('/register', methods=['POST'])
def register():
    mobile_number = request.json['mobile_number']
    verification_code = random.randint(100000, 999999)
    verification_codes[mobile_number] = verification_code
    message = twilio_client.messages.create(
        body=f"Your verification code is {verification_code}",
        from_='+1234567890',
        to=mobile_number
    )
    return jsonify({"message": "Verification code sent"}), 200

@routes.route('/verify', methods=['POST'])
def verify():
    mobile_number = request.json['mobile_number']
    code = request.json['code']
    if verification_codes.get(mobile_number) == int(code):
        user = User.query.filter_by(mobile_number=mobile_number).first()
        if not user:
            user = User(mobile_number=mobile_number, is_verified=True)
            db.session.add(user)
        else:
            user.is_verified = True
        db.session.commit()
        return jsonify({"message": "Verification successful"}), 200
    else:
        return jsonify({"message": "Invalid verification code"}), 400

@routes.route('/create_game', methods=['POST'])
def create_game():
    data = request.json
    user_id = data['user_id']
    amount = data['amount']
    user = User.query.get(user_id)
    if user.balance >= amount:
        game = Game(player1_id=user_id, amount=amount)
        db.session.add(game)
        db.session.commit()
        return jsonify({"message": "Game created", "game_id": game.id}), 200
    else:
        return jsonify({"message": "Insufficient balance"}), 400

@routes.route('/join_game', methods=['POST'])
def join_game():
    data = request.json
    user_id = data['user_id']
    game_id = data['game_id']
    user = User.query.get(user_id)
    game = Game.query.get(game_id)
    if user.balance >= game.amount and game.status == 'waiting':
        game.player2_id = user_id
        game.status = 'ongoing'
        db.session.commit()
        return jsonify({"message": "Joined game", "game_id": game.id}), 200
    else:
        return jsonify({"message": "Cannot join game"}), 400

@routes.route('/submit_result', methods=['POST'])
def submit_result():
    data = request.json
    game_id = data['game_id']
    winner_id = data['winner_id']
    game = Game.query.get(game_id)
    if game.status == 'ongoing':
        game.winner_id = winner_id
        game.status = 'completed'
        winner = User.query.get(winner_id)
        loser_id = game.player1_id if game.player2_id == winner_id else game.player2_id
        loser = User.query.get(loser_id)
        total_amount = game.amount * 2
        winner_amount = total_amount * 0.95
        owner_amount = total_amount * 0.05
        winner.balance += winner_amount
        loser.balance -= game.amount
        # Assume owner's balance is handled separately
        db.session.commit()
        return jsonify({"message": "Result submitted"}), 200
    else:
        return jsonify({"message": "Invalid game status"}), 400
