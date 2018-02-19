from flask import Flask, render_template, request, redirect, session, flash
import os, binascii, hashlib
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = 'shushmans'


class Ship:
    def __init__(self, fuel, health, ammo, speed, energy, shield, energy_store, ammo_store, shield_max):
        self.fuel = fuel
        self.health = health
        self.ammo = ammo
        self.speed = speed
        self.energy = energy
        self.shield = shield
        self.storage = storage
        self.shield_max = shield_max
        self.distance_travelled = 0
        self.surrendered = False
        self.combat = False
        self.market = False
        self.purchase_option = None
        self.turn_count = 0
        self.message = ''
        self.artifact = 0

    def take_ship_damage(self):
        if self.shield < 1:
            self.health -= 1
            if self.health < 1:
                self.destroy()
        else:
            self.take_shield_damage()

    def take_shield_damage(self):
        self.shield -= 1

    def move_ship(self):
        if self.fuel > 0:
            if not self.health % 5:
                self.health += 1
            self.fuel -= 1
            self.distance_travelled += 1
            if not self.combat:
              self.new_event()
            else if self.combat:
              self.combat = False
        return self


    def fire_laser(self, enemy):
        if (random.random() * (self.speed / enemy.speed)) > 0.1:
            enemy.take_shield_damage
        return self, enemy

    def fire_missile(self, enemy):
        if ((random.random() * (self.speed / enemy.speed)) > 0.2:)
            enemy.take_shield_damage
        return self, enemy

    def destroy(self, enemy):
        if(random.random() > 0.2):
            self.health += self.speed
        return self

    def surrender_win(self, enemy):
        if(random.random() > 0.4):
            self.fuel += enemy.fuel
        if(random.random() > 0.8):
            self.health += 1
        return self

    def upgrade_storage(self):
            self.health -= 1
            self.storage += 1
        return self

    def upgrade_shield(self):
            self.health -= 1
            self.shield_max += 1
        return self


    def improve(self):
        roll = random.random() * 100

        if(roll >= 99):
            self.health += 3

        else if(roll >= 95):
            self.storage += 2

        else if(roll >= 90):
            self.speed += 1

        else if(roll >= 80):
            self.ammo = (self.storage - self.energy)

        else if(roll >= 60):
             self.energy = (self.storage - self.ammo)

        else if(roll >= 55):
            self.shield = self.shield_max

        else if(roll >= 50):
            self.storage += 1
        else:
            self.fuel += 5
        return self

    def find_wreckage(self):
        roll = random.random() * 100

        if(roll >= 99):
            self.health += 3

        else if(roll >= 95):
            self.storage += 2

        else if(roll >= 90):
            self.speed += 1

        else if(roll >= 80):
            self.ammo = (self.storage - self.energy)

        else if(roll >= 60):
             self.energy = (self.storage - self.ammo)

        else if(roll >= 55):
            self.shield = self.shield_max

        else if(roll >= 50):
            self.storage += 1
        else:
            self.fuel += 5
        return self

    def find_trading_post(self):
        self.market = True
        roll = random.random() * 100

        if(roll >= 99):
            self.purchase_option = 'artifact'

        else if(roll >= 90):
            self.purchase_option = 'speed'

        else if(roll >= 75):
            self.purchase_option = 'storage'

        else if(roll >= 60):
            self.purchase_option = 'missile'

        else if(roll >= 50):
            self.purchase_option = 'shield'

        else:
            self.purchase_option = 'battery'

        return self

    def purchase(self):
        if self.purchase_option == 'artifact':
            self.health -= 1
            self.artifact += 1
        else if self.purchase_option == 'speed':
            self.health -= 1
            self.speed += 1
        else if self.purchase_option == 'storage':
            self.health -= 1
            self.storage += 1
        else if self.purchase_option == 'missile':
            self.health -= 1
            self.speed += 1
        else if self.purchase_option == 'shield':
            self.health -= 1
            self.shield += 1
        else if self.purchase_option == 'battery':
            self.health -= 1
            self.speed += 1
        return self


    def new_event(self):
        roll = random.random() * 100

        if(roll >= 99):
            self.improve()

        else if(roll >= 95):
            self.find_wreckage()

        else if(roll >= 90):
             self.find_trading_post

        else if(roll >= 80):
            self.find_merchant()

        else if(roll >= 60):
            self.find_enemy()

        else if(roll >= 55):
            self.space_debris()

        else if(roll >= 50):
            self.illness
        return self




@app.route('/create_player')
def CreatePlayer():
        player = Ship(4,2,2,1,5,1,1,1)
        # request.session['player'] = player
        return jsonify(player)

@app.route('/')
def index():
        return render_template("index.html")

@app.route('/move_ship')
def move_ship(ship):
        ship.move()
        return jsonify(ship)

@app.route('/laser')
def fire_laser(ship, target):
        ship.fire_laser(target)
        return jsonify(ship, target)

@app.route('/missile')
def fire_missile(ship, target):
        ship.fire_missile(target)
        return jsonify(ship, target)

@app.route('/upgrade')
def upgrade_ship(ship):
        ship.upgrade()
        return(ship)

app.run(debug=True)
