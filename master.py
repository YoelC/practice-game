from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, FONT, convert_to_prefix, distance_two_points
from random import randint
import pygame

pygame.init()
pygame.font.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BACKGROUND_IMG = pygame.image.load('images/background.png')

from classes.entities.player import Player
from classes.entities.enemy import Enemy
from classes.entities.orb import Orb
from classes.entities.hive import Hive
from classes.decoration.background import Background
from classes.decoration.hitmarker import HitMarker
from classes.decoration.button import Button
from classes.decoration.shop_background import ShopBackground
from classes.decoration.shop_button import ShopButton


def game(surface, tick, clicked):
    cheats = True

    shop_background.current_img = 0
    shop1 = False
    player.repair = False
    if player.health_bar.health < player.health_bar.max_health:
        player.repair = True

    hive.attempt_enemy_spawn(tick)

    if pygame.key.get_pressed()[pygame.K_d]:
        player.right()

    if pygame.key.get_pressed()[pygame.K_a]:
        player.left()

    if pygame.key.get_pressed()[pygame.K_z] and cheats:
        player.money += 1e6

    if pygame.key.get_pressed()[pygame.K_SPACE] and player.delay1 == 0:
        player.shoot()
        player.delay1 += player.delay1_delay

    elif player.delay1 != 0:
        player.delay1 -= 1

    for i, enemy in enumerate(hive.enemies):
        for j, bullet in enumerate(player.bullets):
            if bullet.get_rect().colliderect(enemy.get_rect()):
                player.bullets.pop(j)
                hitmarkers.append(HitMarker(
                    pos=(bullet.x + bullet.width/2, bullet.y + bullet.height/2),
                    indicator=-bullet.damage,
                    color=(255, 255, 0),
                    crit=bullet.crit,
                    crit_color=(255, 0, 0),
                    decimal=False))

                try:
                    dead = hive.enemies[i].hit(bullet.damage)
                    if dead:
                        if enemy.spaceship_type == 0:
                            for _ in range(randint(1, 5)):
                                money_orbs.append(Orb((enemy.x + enemy.width / 2, enemy.y + enemy.height / 2), player,
                                                      reward=enemy.reward,
                                                      reward_ratio=hive.reward_ratio,
                                                      deviation=5))
                        hive.enemies.pop(i)
                except IndexError:
                    pass

        if enemy.get_rect().colliderect(player.get_rect()):
            player.hit(1)
            hitmarkers.append(HitMarker(
                pos=(player.x + player.width / 2, player.y + player.height / 2),
                indicator=-1,
                color=(255, 0, 0),
                spread=80,
                decimal=False))
            dead = hive.enemies[i].hit(1)
            if dead:
                hive.enemies.pop(i)

    for i, bullet in enumerate(player.bullets):
        if bullet.chase:
            best_distance = 10e9
            enemy_to_attack = None
            for j, enemy in enumerate(hive.enemies):
                x1, y1 = bullet.x, bullet.y
                x2, y2 = enemy.x + enemy.width/2, enemy.y + enemy.height/2

                if distance_two_points(x1, y1, x2, y2) < best_distance:
                    best_distance = distance_two_points(x1, y1, x2, y2)
                    enemy_to_attack = j

            if enemy_to_attack is not None:
                temp_enemy = hive.enemies[enemy_to_attack]
                bullet.set_target(temp_enemy.x + temp_enemy.width/2, temp_enemy.y + temp_enemy.height/2)
            else:
                bullet.set_target()

    for i, orb in enumerate(money_orbs):
        cash_hitbox = player.get_rect()
        cash_hitbox.x += cash_hitbox.width/2
        cash_hitbox.y += cash_hitbox.height/2
        cash_hitbox.width /= 4
        cash_hitbox.height /= 4
        if orb.get_rect().colliderect(cash_hitbox):
            hitmarkers.append(HitMarker(
                pos=(WINDOW_WIDTH - 150, 65),
                indicator=orb.reward,
                extra='$',
                color=(0, 255, 0),
                spread=40,
                y_vel=-1))
            player.money += orb.reward
            money_orbs.pop(i)

    if clicked:
        if shop_button1.clicked():
            shop1 = True

        if player.repair and repair_button.clicked() and (player.health_bar.max_health - player.health_bar.health)*player.repair_cost <= player.money:
            player.money -= (player.health_bar.max_health - player.health_bar.health)*player.repair_cost
            for i in range(player.health_bar.max_health - player.health_bar.health):
                hitmarkers.append(HitMarker(
                    pos=(player.x + player.width / 2, player.y + player.height / 2),
                    indicator=0,
                    extra='+',
                    color=(0, 255, 0),
                    spread=40))

            player.health_bar.health = player.health_bar.max_health
            player.repair = False


    # Move

    background.move()
    player.move()
    for hitmarker in hitmarkers:
        hitmarker.move()

    for enemy in hive.enemies:
        enemy.move()

    for orb in money_orbs:
        orb.move()


    # Draw Screen

    win.fill((0, 0, 0))
    background.draw(surface)
    player.draw(surface)
    for i, enemy in enumerate(hive.enemies):
        enemy.draw(surface)
        if enemy.y > WINDOW_HEIGHT:
            hive.enemies.pop(i)

    for i, hitmarker in enumerate(hitmarkers):
        hitmarker.draw(surface)
        if hitmarker.delay < 0:
            hitmarkers.pop(i)

    for orb in money_orbs:
        orb.draw(surface)

    font, font_pos = FONT.render(f'Money: ${convert_to_prefix(player.money)}', fgcolor=(255, 255, 255), size=30)
    surface.blit(font, (WINDOW_WIDTH - font_pos.width - font_pos.height, font_pos.height))
    shop_button1.draw(surface)
    if player.repair:
        repair_button.text = f' REPAIR (${(convert_to_prefix(player.health_bar.max_health - player.health_bar.health)*player.repair_cost)})'
        repair_button.draw(surface)

    pygame.display.flip()

    tick += 1

    return tick, shop1


def shop_screen1(surface, tick, clicked):
    shop1 = True
    shop2 = False

    def not_enough():
        hitmarkers_shop.clear()
        hitmarkers_shop.append(HitMarker(
            pos=pygame.mouse.get_pos(),
            indicator=0,
            extra='NOT ENOUGH MONEY!',
            color=(255, 0, 0),
            size=30,
            angle_variation=15))

    def enough():
        hitmarkers_shop.clear()
        hitmarkers_shop.append(HitMarker(
            pos=pygame.mouse.get_pos(),
            indicator=0,
            extra='BOUGHT!',
            color=(0, 255, 0),
            size=40,
            angle_variation=15))

    def max_level():
        hitmarkers_shop.clear()
        hitmarkers_shop.append(HitMarker(
            pos=pygame.mouse.get_pos(),
            indicator=0,
            extra='MAX LVL!',
            color=(255, 0, 0),
            size=40,
            angle_variation=15))

    if clicked:
        if back_button.clicked():
            shop1 = False
            shop2 = False

        if shop_button2.clicked():
            shop1 = False
            shop2 = True

        for button in buttons_p1:
            if button.clicked():
                money = button.upgrade(money=player.money)
                if money is False:
                    max_level()

                elif money != player.money:
                    player.money = money
                    enough()

                else:
                    not_enough()


    # Move
    for hitmarker in hitmarkers_shop:
        hitmarker.move()


    # Draw Screen
    shop_background.draw(surface)

    font, font_pos = FONT.render(f'Money: ${convert_to_prefix(player.money)}', fgcolor=(255, 255, 255), size=30)
    surface.blit(font, (WINDOW_WIDTH - font_pos.width - font_pos.height, font_pos.height))

    back_button.draw(surface)

    for button in buttons_p1:
        button.draw(surface, player.money)

    for i, hitmarker in enumerate(hitmarkers_shop):
        hitmarker.draw(surface)
        if hitmarker.delay < 0:
            hitmarkers_shop.pop(i)

    shop_button2.draw(surface)

    pygame.display.flip()

    return tick, shop1, shop2


def shop_screen2(surface, tick, clicked):
    shop2 = True
    shop1 = False

    def not_enough():
        hitmarkers_shop.clear()
        hitmarkers_shop.append(HitMarker(
            pos=pygame.mouse.get_pos(),
            indicator=0,
            extra='NOT ENOUGH MONEY!',
            color=(255, 0, 0),
            size=30,
            angle_variation=15))

    def enough():
        hitmarkers_shop.clear()
        hitmarkers_shop.append(HitMarker(
            pos=pygame.mouse.get_pos(),
            indicator=0,
            extra='BOUGHT!',
            color=(0, 255, 0),
            size=40,
            angle_variation=15))

    def max_level():
        hitmarkers_shop.clear()
        hitmarkers_shop.append(HitMarker(
            pos=pygame.mouse.get_pos(),
            indicator=0,
            extra='MAX LVL!',
            color=(255, 0, 0),
            size=40,
            angle_variation=15))

    if clicked:
        if back_button.clicked():
            shop1 = True
            shop2 = False

        for button in buttons_p2:
            if button.clicked():
                money = button.upgrade(money=player.money)
                if money is False:
                    max_level()

                elif money != player.money:
                    player.money = money
                    enough()

                else:
                    not_enough()


    # Move
    for hitmarker in hitmarkers_shop:
        hitmarker.move()


    # Draw Screen
    surface.blit(BACKGROUND_IMG, (0, 0))
    back_button.draw(surface)
    font, font_pos = FONT.render(f'Money: ${convert_to_prefix(player.money)}', fgcolor=(255, 255, 255), size=30)
    surface.blit(font, (WINDOW_WIDTH - font_pos.width - font_pos.height, font_pos.height))

    for button in buttons_p2:
        button.draw(surface, player.money)

    for i, hitmarker in enumerate(hitmarkers_shop):
        hitmarker.draw(surface)
        if hitmarker.delay < 0:
            hitmarkers_shop.pop(i)

    pygame.display.flip()

    return tick, shop1, shop2

CLOCK = pygame.time.Clock()

# Game Initializations
player = Player((WINDOW_WIDTH/2, WINDOW_HEIGHT - WINDOW_HEIGHT/6))
background = Background(150)
shop_button1 = Button((25, 25, 200, 40), ' SHOP')
repair_button = Button((250, 25, 300, 40), ' REPAIR')
hive = Hive()
hitmarkers = []
hitmarkers_shop = []
money_orbs = []

# Shop Initializations
# Page 1
shop_background = ShopBackground()
buttons_p1 = []
back_button = Button((25, 25, 200, 40), ' BACK')
shop_button2 = Button((WINDOW_WIDTH - 200 - 25, 75, 200, 40), 'NEXT')

damage_button = ShopButton(pos=(25, 125),
                           text='Damage per bullet',
                           class_instance=player,
                           attribute_attached='damage',
                           attribute_ratio=0.25,
                           attribute_type='+',
                           upgrade_cost=500,
                           upgrade_ratio=2,
                           upgrade_type='*',
                           attribute_extra='dmg',
                           max_upgrades=16)
buttons_p1.append(damage_button)

rof_button = ShopButton(pos=(25, 200),
                        text='Rate of Fire',
                        class_instance=player,
                        attribute_attached='delay1_delay',
                        attribute_ratio=2,
                        attribute_type='-',
                        upgrade_cost=200,
                        upgrade_ratio=2,
                        upgrade_type='*',
                        attribute_extra=' ticks/shot',
                        max_upgrades=15)

buttons_p1.append(rof_button)

crit_chance_button = ShopButton(pos=(25, 300),
                                text='Crit Chance',
                                class_instance=player,
                                attribute_attached='crit_chance',
                                attribute_ratio=2,
                                attribute_type='+',
                                upgrade_cost=400,
                                upgrade_ratio=1.625,
                                upgrade_type='*',
                                attribute_extra='%',
                                max_upgrades=18)
buttons_p1.append(crit_chance_button)


crit_damage_button = ShopButton(pos=(25, 375),
                                text='Crit Damage Multiplier',
                                class_instance=player,
                                attribute_attached='crit_damage',
                                attribute_ratio=1,
                                attribute_type='+',
                                upgrade_cost=400,
                                upgrade_ratio=2,
                                upgrade_type='*',
                                attribute_extra='x',
                                max_upgrades=12)
buttons_p1.append(crit_damage_button)

max_vel_button = ShopButton(pos=(25, 475),
                            text='Max Player Velocity',
                            class_instance=player,
                            attribute_attached='max_vel',
                            attribute_ratio=1,
                            attribute_type='+',
                            upgrade_cost=1000,
                            upgrade_ratio=2,
                            upgrade_type='*',
                            attribute_extra='m/s',
                            max_upgrades=10)
buttons_p1.append(max_vel_button)

accel_button = ShopButton(pos=(25, 550),
                          text='Player Acceleration',
                          class_instance=player,
                          attribute_attached='accel',
                          attribute_ratio=0.05,
                          attribute_type='+',
                          upgrade_cost=1000,
                          upgrade_ratio=2,
                          upgrade_type='*',
                          attribute_extra='m/s squared',
                          max_upgrades=10)
buttons_p1.append(accel_button)

ship_level = ShopButton(pos=(25, 650),
                        text='Ship Level',
                        class_instance=player,
                        attribute_attached='ship_level',
                        attribute_ratio=1,
                        attribute_type='+',
                        upgrade_cost=10000,
                        upgrade_ratio=100,
                        upgrade_type='*',
                        max_upgrades=3)
buttons_p1.append(ship_level)

# Page 2
buttons_p2 = []

spawn_rate = ShopButton(pos=(25, 125),
                        text='Spawn Rate',
                        class_instance=hive,
                        attribute_attached='spawn_rate',
                        attribute_ratio=5,
                        attribute_type='-',
                        upgrade_cost=100,
                        upgrade_ratio=2.5,
                        upgrade_type='*',
                        attribute_extra=' ticks/spawn',
                        max_upgrades=15)
buttons_p2.append(spawn_rate)

cash_multiplier = ShopButton(pos=(25, 200),
                             text='Money Multiplier',
                             class_instance=hive,
                             attribute_attached='reward_ratio',
                             attribute_ratio=2,
                             attribute_type='*',
                             upgrade_cost=250,
                             upgrade_ratio=2,
                             upgrade_type='*',
                             attribute_extra='x',
                             max_upgrades=15)
buttons_p2.append(cash_multiplier)

tick = 1
shop1 = False
shop2 = False
clicked = False
click_delay = 0

run = True
while run:
    CLOCK.tick(FPS)
    run = False if pygame.QUIT in [x.type for x in pygame.event.get()] else True

    clicked = False
    if pygame.mouse.get_pressed()[0] == 1 and click_delay == 0:
        clicked = True
        click_delay += 1

    if pygame.mouse.get_pressed()[0] == 0:
        click_delay = 0

    if shop1:
        tick, shop1, shop2 = shop_screen1(win, tick, clicked)

    elif shop2:
        tick, shop1, shop2 = shop_screen2(win, tick, clicked)

    else:
        tick, shop1 = game(win, tick, clicked)


