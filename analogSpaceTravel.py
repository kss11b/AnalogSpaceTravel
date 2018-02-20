from flask import Flask, render_template, request, redirect, session, flash, jsonify
import os, binascii, hashlib, sys, random
app = Flask(__name__)
app.secret_key = 'shushmans'


# class Ship:
#     def __init__(self, fuel, health, ammo, speed, energy, shield, energy_store, ammo_store, shield_max, storage, combat):
#         self.fuel = fuel
#         self.health = health
#         self.ammo = ammo
#         self.speed = speed
#         self.energy = energy
#         self.shield = shield
#         self.storage = storage
#         self.shield_max = shield_max
#         self.distance_travelled = 0
#         self.surrendered = False
#         self.combat = combat
#         self.market = False
#         self.purchase_option = None
#         self.turn_count = 0
#         self.message = ''
#         self.artifact = 0
#         self.sight = False

def take_ship_damage(ship):
    if ship['shield'] < 1:
        ship['health'] -= 1
        if ship['health'] < 1:
            ship = destroy(ship)
    else:
        ship = take_shield_damage(ship)
    return ship

def take_shield_damage(ship):
    if ship['shield'] > 0:
        ship['shield'] -= 1
    else:
        ship = take_shield_damage(ship)
    return ship


def move_ship(ship):
    if ship['fuel'] > 0:
        if not ship['health'] % 5:
            ship['health'] += 1
        ship['fuel'] -= 1
        ship['distance_travelled'] += 1
        if not ship['combat']:
            ship = new_event(ship)
        elif ship['combat']:
            ship['combat'] = False
    return ship

def fire_laser(ship, enemy):
    if (random.random() * (ship.speed / enemy.speed)) > 0.1:
        enemy.take_shield_damage()
    return ship, enemy

def fire_missile(ship, enemy):
    if ((random.random() * (ship.speed / enemy.speed)) > 0.2 and enemy.shield < 1):
        enemy = take_ship_damage(enemy)
        enemy = take_ship_damage(enemy)
    return ship, enemy

def destroy(ship, enemy):
    if(random.random() > 0.2):
        ship.health += enemy.speed
    ship.combat = False
    return ship

def surrender_win(ship, enemy):
    if(random.random() > 0.4):
        ship.fuel += enemy.fuel
    if(random.random() > 0.8):
        ship.health += 1
    return ship

def upgrade_storage(ship):
    ship.health -= 1
    ship.storage += 1
    return ship

def upgrade_shield(self):
    ship.health -= 1
    ship.shield_max += 1
    return ship


def improve(ship):
    roll = random.random() * 100

    if(roll >= 99):
        ship.sight = True

    elif(roll >= 95):
        ship.speed += 1

    elif(roll >= 90):
        ship.storage += 2

    elif(roll >= 80):
        ship.health += 3

    elif(roll >= 60):
        ship.ammo = (self.storage - self.energy)

    elif(roll >= 55):
        ship.energy = (self.storage - self.ammo)

    elif(roll >= 50):
        ship.shield = self.shield_max

    elif(roll >= 40):
        ship.storage += 1
    else:
        ship.fuel += 5
    return ship

def find_wreckage(ship):
    roll = random.random() * 100

    if(roll >= 99):
        ship.health += 3

    elif(roll >= 95):
        ship.storage += 2

    elif(roll >= 90):
        ship.speed += 1

    elif(roll >= 80):
        ship.ammo = (ship.storage - ship.energy)

    elif(roll >= 60):
         ship.energy = (ship.storage - ship.ammo)

    elif(roll >= 55):
        ship.shield = ship.shield_max

    elif(roll >= 50):
        ship.storage += 1
    else:
        ship.fuel += 5
    return ship

def find_trading_post(ship):
    ship.market = True
    roll = random.random() * 100

    if(roll >= 99):
        ship.purchase_option = 'artifact'

    elif(roll >= 90):
        ship.purchase_option = 'speed'

    elif(roll >= 75):
        ship.purchase_option = 'storage'

    elif(roll >= 60):
        ship.purchase_option = 'missile'

    elif(roll >= 50):
        ship.purchase_option = 'shield'

    else:
        ship.purchase_option = 'battery'

    return ship

def purchase(ship):
    if ship.purchase_option == 'artifact':
        ship.health -= 1
        ship.artifact += 1
    elif ship.purchase_option == 'speed':
        ship.health -= 1
        ship.speed += 1
    elif ship.purchase_option == 'storage':
        ship.health -= 1
        ship.storage += 1
    elif ship.purchase_option == 'missile':
        ship.health -= 1
        ship.speed += 1
    elif ship.purchase_option == 'shield':
        ship.health -= 1
        ship.shield += 1
    elif ship.purchase_option == 'battery':
        ship.health -= 1
        ship.speed += 1
    return ship

def new_event(ship):
    roll = random.random() * 100

    if(roll >= 99):
        # ship = improve(ship)
        ship['message'] = 'improve'
    elif(roll >= 95):
        # ship = find_wreckage(ship)
        ship['message'] = 'find wreckage'
    elif(roll >= 90):
         # ship = find_trading_post(ship)
         ship['message'] = 'find trading post'
    elif(roll >= 80):
        # ship = find_merchant(ship)
        ship['message'] = 'find_merchant'
    elif(roll >= 60):
        # ship = find_enemy(ship)
        ship['message'] = 'enemy'
    elif(roll >= 55):
        # ship = space_debris(ship)
        ship['message'] = 'space debris'
    elif(roll >= 50):
        # ship = illness(ship)
        ship['message'] = 'illness'
    else:
        ship['message'] = 'Nothing of interest happened'
    return ship

def find_enemy(ship):
    enemy = Ship(4,1,2,1,5,1,1,1,1,8, True)
    return jsonify(enemy)


@app.route('/create_player')
def create_player():
        player = Ship(4,2,2,1,5,1,1,1,1,8, False)
        player.message = 'You embark on a journey into the deepest reaches of'\
        ' space, to go further than any before you'
        return jsonify(player.__dict__)

@app.route('/')
def index():
        return render_template("index.html")

@app.route('/move_ship', methods=['POST'])
def move_ship_request():
    ship = request.get_json()
    print(ship, request.is_json)
    sys.stdout.flush()
    # ship = take_ship_damage(ship)
    ship = move_ship(ship)

    return jsonify(ship)

@app.route('/laser')
def fire_laser(ship, target):
        ship.fire_laser(target)
        return jsonify(ship, target)

@app.route('/missile')
def fire_missile(ship, target):
        ship.fire_missile(target)
        return jsonify(ship, target)

@app.route('/upgrade', methods=['POST'])
def upgrade_ship(ship):
    ship = request.get_json()

    ship = upgrade_storage(ship)
    return ship

@app.route('/engage_combat')
def engage_combat(ship):
    ship.combat = True
    enemy = ship.find_enemy()
    return jsonify(ship)

@app.route('/enemy_attack')
def enemy_attack(player, enemy):
    enemy_ai = random.random() * 10
    if enemy_ai + enemy.speed < player.speed:
        enemy.move()
    elif player.shield < 1:
        enemy = fire_laser(enemy, player)
    else:
        enemy = fire_missile(enemy, player)
    return player, enemy

app.run(debug=True)
