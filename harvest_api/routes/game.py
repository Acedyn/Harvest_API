from flask import Blueprint, jsonify, request
from database import sessions, engines
from mappings.nimbygame_tables import Player

# Initialize the set to routes for tractor
game = Blueprint("game", __name__)


# Route to get a player profile
@game.route("/game/player/<computername>")
def get_player(computername):
    name = request.args.get('name', default = computername, type = str)

    player = sessions["nimbygame"].query(Player.computer, Player.name, Player.score) \
    .filter(Player.computer == computername)

    # If the sql result is no empty
    if len(player.all()) >= 1:
        response = {"computer": player[0][0], "name": player[0][1], "score": player[0][2]}
        return jsonify(response)

    new_player = Player(
        computer = computername,
        name = name)

    sessions["nimbygame"].add(new_player)
    sessions["nimbygame"].commit()

    player = sessions["nimbygame"].query(Player.computer, Player.name, Player.score) \
    .filter(Player.computer == computername)

    # If the sql result is no empty
    if len(player.all()) >= 1:
        response = {"computer": player[0][0], "name": player[0][1], "score": player[0][2]}
        return jsonify(response)

    return "ERROR: Could not create the player"

@game.route("/game/score/<computername>")
def increment_score(computername):
    points = request.args.get('points', default = 0, type = int)
    
    player = sessions["nimbygame"].query(Player) \
    .filter(Player.computer == computername).first()
    player.score += points

    sessions["nimbygame"].commit()
    
    response = {"computer": player.computer, "name": player.name, "score": player.score}
    return jsonify(response)
