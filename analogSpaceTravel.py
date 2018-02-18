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
        self.turn_count = 0

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
            self.fuel -= 1
            self.distance_travelled += 1
            if not self.combat:
              self.new_event()
            else if self.combat:
              self.combat = False
               

    def fire_laser(self, enemy):
        if (random.random() * (self.speed / enemy.speed)) > 0.1:
            enemy.take_shield_damage

    def fire_missile(self, enemy):
        if ((random.random() * (self.speed / enemy.speed)) > 0.2:)
            enemy.take_shield_damage

    def destroy(self, enemy):
        if(random.random() > 0.2):
            self.health += self.speed

    def surrender_win(self, enemy):
        if(random.random() > 0.4):
            self.fuel += enemy.fuel
        if(random.random() > 0.4):
            self.health += 1

    def upgrade(self, attribute):
        if self.health > 1:
            if attribute === self.energy || attribute === self.ammo:
                if self.energy + self.ammo === self.storage:
                    return
            self.health -= 1
            self.attribute += 1

    def gain_attribute(self, attribute, amount):
        self.attribute += amount

    def lose_attribute(self, attribute, amount):
        self.attribute -= amount
        if self.health < 1:
            self.destroy

    def new_event(self):
        roll = random.random() * 100

        if(roll == 99):
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
        else:
            return



@app.route('/create_player')
def CreatePlayer():
    player = Ship(4,2,2,1,5,1,1,1)
    request.session['player'] = player
    return jsonify(player) 

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/move_ship')
def move_ship(ship):
        ship.move()
        return jsonify(ship) 

@app.route('fire_laser'):
def fire_lasers(ship, target):
        ship.fire_laser(target)
        return jsonify(ship, target)

app.run(debug=True)
