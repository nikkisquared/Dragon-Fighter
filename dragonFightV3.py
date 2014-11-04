# DRAGON FIGHTER RPG (Dragon Fighter Version 3.1)
# A Dragon fighting RPG simulator, developed by Nikki
# TODO: expanded shop, items, bigger town, skills, saving, last dragon mechanic

import random
from sys import exit
# speeds up the game for testing purposes
fast = False
# makes the game much easier by giving the player loads of money
cheat = False

class Player(object):

	def __init__(self):
		self.name = ''
		self.kills = 0
		self.money = random.randint(5, 25)
		# keeps track of ALL money made
		self.totalmoney = 0
		# general stats
		self.stats = {'attack': 4, 'defense': 0, 'magic': 2, 'speed': 3, 'health': 40, 'experience': 0, 'level': 1}
		# used only for fights
		self.status = {'currHealth': 0, 'defend': 0, 'defendTurns': 0, 'poisonTurns': 0}

	def checklevel(self):
		"""levels up the character if applicable"""
		s = self.stats

		if (s['level'] == 1 and s['experience'] > 12) or (s['experience'] > pow(2, s['level'] + 3) + 12):
			s['attack'] += random.randint(2 * s['level'], 4 * s['level'])
			s['defense'] += random.randint(1 + (s['level']/2), 2 * s['level'])
			s['magic'] += random.randint(1 * s['level'], 2 * s['level'])
			s['speed'] += random.randint(1, 2 + (s['level']/3))
			s['health'] += random.randint(1 * s['level'], 2 * s['level']) * 5
			s['level'] += 1
			print "LEVEL UP! You are now level %s." % (s['level'])
			print "STATS UP! You now have: %s attack, %s defense, %s magic, %s speed, and %s health." % (s['attack'], s['defense'], s['magic'], s['speed'], s['health'])

class Dragon(object):

	def __init__(self):
		# number of dragons remaining to fight, level 1 = 1 dragon, level 2 = 2 dragons, etc
		self.dragons = 5000
		self.last = False

	def makeDragon(self, level, kills):
		"""returns health/damage stats for the dragon, and lowers the number of dragons left"""
		self.dragons -= level
		if self.dragons <= 0: self.lastDragon = True
		# health is between 30 and 40, going up 5 every level and 2 every fight
		# damage starts at 1, increasing by 1 every 3 kills and 2 every level
		# if it is the last dragon, killing it ends the game
		return {'health': 25 + random.randint(0, 10) + (level * 5) + (kills * 2), 
				'Damage': (kills / 3) + (level * 2) - 1, 'Last': self.last}

def getInput(msg, allowed):
	"""checks for special input options and returns ordinary, successful input"""
	while True:
		userInput = raw_input(msg + '\n').upper()
		if userInput in allowed.split() and len(userInput) != 0:
			return userInput
		elif userInput == 'AUTO':
			autoOptions()
		elif userInput == 'QUIT':
			quit()
		else:
			print "That doesn't make sense in this context!"

def autoOptions():
	# lets the user change the options for skipping choices
	global autoShop; global autoFight
	while True:
		choice = raw_input("Auto Shop: %s \tAuto Fight: %s\n1 - Shop\t2 - Fight\t3 - All \t4 - None\n5 - Finish\n" % (autoShop, autoFight))
		if choice == '1': autoShop = not autoShop
		elif choice == '2': autoFight = not autoFight
		elif choice == '3': autoShop = True; autoFight = True
		elif choice == '4': autoShop = False; autoFight = False
		elif choice == '5': break
		else: print "That isn't a choice!"

def quit():
	if raw_input('Are you SURE you want to quit? Y/n\n').startswith('Y'):
		print "You defeated %s dragons, and made %s gold. See you next time %s!" % (p.kills, p.totalmoney, p.name)
		raw_input("Press any key to exit.")
		exit(0)

def pTurn(p, d):
	"""
	manages the player's turn for various attacks and spells
	they can fight until they run out of stamina, or end the turn early to have another turn sooner
	"""

	# limits the number of moves the player can make
	stamina = 10 

	while stamina > 0 and d['health'] > 0:
		print "\nThe dragon has %s health. You have %s stamina (Stm)." % (d['health'], stamina)

		# main turn menu
		move = getInput("\nAttack (A)\nMagic (M)\nEnd Turn (E)", ('A M E'))

		# physical attack menu
		if move == 'A': 
			move = getInput("\nQuick - 2 Stm (Q)\nNormal - 3 Stm (N)\nStrong - 5 Stm (S)\nBack (B)", ('Q N S B'))

			# fast, accurate, weak
			if move == 'Q':	moveSet = ['A', 2, 90, random.randint(2, 5) + p.stats['attack']/3]
			# all around average attack
			elif move == 'N': moveSet = ['A', 3, 80, random.randint(5, 12) + p.stats['attack']/2]
			# slow, inaccurate, strong
			elif move == 'S': moveSet = ['A', 5, 70, random.randint(12, 18) + p.stats['attack']]

		# magic menu
		elif move == 'M': 
			move = getInput("\nIceball - 4 Stm (I)\nHeal - 6 Stm (H)\nDefend - 7 Stm (D)\nCure - 9 Stm (C)\nBack (B)", ('I H D C B'))

			# an iceball attack: average accuracy, very random damage
			if move == 'I':
				moveSet = ['A', 4, 85, random.randint(8, 20) + p.stats['magic']/2] 
			# heals the player somewhat
			elif move == 'H':
				if p.status['currHealth'] == p.stats['health']:
					print "Your health is at max!"
					move = 'B'
				else:
					moveSet = ['H', 6, random.randint(5, 20) + p.stats['magic']/4]
			# raises defense for a few turns
			elif move == 'D':
				if p.status['defendTurns'] != 0:
					print "You are already magically defending!"
					move = 'B'
				else:
					moveSet = ['D', 7, random.randint(1, 3) + p.stats['magic']/6, random.randint(2, 8) + p.stats['magic']/4]
			# cures poison
			elif move == 'C':
				if p.status['poisonTurns'] == 0:
					print "You aren't poisoned, you don't need to cure yourself!"
					move = 'B'
				else:
					moveSet = ['C', 9]

		# ends turn early
		elif move == 'E':
			print "You slow down your attack, and find it a bit easier to catch your breath."
			break

		# goes back to the first menu if the user attempted a bad move
		if move == 'B':
			continue 
		else:
			stamina -= moveSet[1]

			# attack move - needs to surpass the accuracy roll
			if moveSet[0] == 'A': 
				# accuracy roll
				success = random.randint(0, 100) 
				if success < moveSet[2]:
					if move == 'I':
						print "You hurl a giant ball of ice created from the air at the dragon! It does %s damage!" % moveSet[3]
					else:
						print "You stab at the dragon! You deal %s damage!" % moveSet[3]
					d['health'] -= moveSet[3]
				elif move == 'I':
					print "You fail to conjure up a ball of ice."
				else:
					print "You flail wildly, accomplishing nothing."

			# heal spell - restores some of the players health, up to their maximum
			elif moveSet[0] == 'H': 
				p.status['currHealth'] += moveSet[2]
				if p.status['currHealth'] > p.stats['health']:
					p.status['currHealth'] = p.stats['health']
				print "You heal yourself. You now have %s health." % p.status['currHealth']

			# defend spell - raises a defensive shield for a few turns
			elif moveSet[0] == 'D':
				p.status['defend'] = moveSet[2]
				p.status['defendTurns'] = moveSet[3]
				print "You raise a magic shield to help defend you."

			# cure move - removes poison
			elif moveSet[0] == 'C':
				p.status['poisonTurns'] = 0
				print "You cure yourself of the deadly poison toxins."

	return stamina, d

def dTurn(p, d):
	"""simulates the turn for the dragon"""

	if p.status['poisonTurns'] > 0:
		# won't make a poison attack if the player is already poisoned
		move = random.randint(0, 3)
	else:
		move = random.randint(0, 4)

	if move == 0:
		move = [random.randint(8, 12), 'The dragon roars and breathes a ball of fire at you!', True]
	elif move == 1:
		move = [1, 'The Dragon swipes at you, and just misses, scraping you!', False]
	elif move == 2:
		move = [random.randint(4, 7), 'The dragon flicks you with its tail!', False]
	elif move == 3:
		move = [random.randint(10, 18), 'The dragon takes a huge bite out of you!', True]
	elif move == 4:
		p.status['poisonTurns'] = random.randint(2, 4) * 5
		move = [random.randint(1, 3), 'The dragon spits poison at you!', False]

	print move[1]
	# adds extra damage for a strong attack
	if move[2]:
		move[0] += d['Damage'] 
	# subtracts any applicable defenses from the damage
	move[0] -= p.stats['defense'] + p.status['defend']
	if move[0] <= 0:
		move[0] = 1
	p.status['currHealth'] -= move[0]
	print "You take %s damage! You now have %s health." % (move[0], p.status['currHealth'])

def fight(p, dragon, first):
	"""
	the player fights against a dragon in turns until one of them dies.
	returns true if the dragon dies, false if the player dies
	"""

	# sets current health to the maximum
	p.status['currHealth'] = p.stats['health'] 
	# resets all statuses
	p.status['defend'] = 0
	p.status['defendTurns'] = 0
	p.status['poisonTurns'] = 0
	# generates a dragon
	d = dragon.makeDragon(p.stats['level'], p.kills)
	# calculates experience points gained on win
	d['XP'] = d['health']/10
	# stamina needs to reach 10 for either character to take a turn
	pStamina = 0
	dStamina = 0 

	print "\nYou step into the arena as the giant gate crashes shut behind you. A dragon charges towards you from the other side.\n"
	if first == 'p':
		print "You get the first strike!"
		pStamina, d = pTurn(p, d)
	else:
		print "The dragon gets the first strike!"
		dTurn(p, d)

	# loops until a combatant dies
	while True:

		pStamina += random.randint(1, p.stats['speed']/3)
		if pStamina >= 10:
			pStamina = 0
			print "\nYou ready yourself for another move."
			pStamina, d = pTurn(p, d)

		# the dragon died
		if d['health'] <= 0: 
			print "\nThe dragon lies defeated before you! You walk out of the arena in a hail of applause."
			p.kills += 1
			earned = 40 + random.randint(0, 20) + ((p.kills + p.stats['level']) * 5) # money reward
			p.money += earned
			p.totalmoney += earned
			print "You gained %s experience Points, and %s gold. You now have %s gold." % (d['XP'], earned, p.money)
			p.stats['experience'] += d['XP']
			p.checklevel()
			return True

		dStamina += random.randint(1, p.stats['level'] * 2)
		if dStamina >= 20:
			dStamina = 0
			print "\nThe dragon makes an attack!\n"
			dTurn(p, d)

			# defense spell runs out over time
			if p.status['defendTurns'] > 0: 
				p.status['defendTurns'] -= 1
				# defense spell runs out
				if p.status['defendTurns'] == 0: 
					print "Your shield of defense vanishes!"
					p.status['defend'] == 0

		# doesn't mention poison damage if player already died 
		if p.status['poisonTurns'] > 0 and p.status['currHealth'] > 0: 
			p.status['poisonTurns'] -= 1
			# poison damage doesn't always occur, so it's less deadly
			if p.status['poisonTurns'] % 5 == 0:
				poiDmg = random.randint(2, 6)
				p.status['currHealth'] -= poiDmg
				print "\nPain wracks your body from the poison. You take %s damage. You now have %s health." % (poiDmg, p.status['currHealth'])
			if p.status['poisonTurns'] == 0:
				print "\nYou feel healthier. The poison has weared off."

		# player has died
		if p.status['currHealth'] <= 0:
			print "\nYou fall down, defeated. Your fighting has come to an end."
			return False

def shop(p):
	"""lets the player buy stat upgrades"""
	
	costs = {'attack': 40 + random.randint(5, 15) + p.stats['attack']/4, 'defense': 50 + random.randint(7, 17) + p.stats['defense']/2,
			'speed': 55 + random.randint(5, 25) + p.stats['speed'], 'magic': 45 + random.randint(2, 30) + p.stats['magic']/3,
			'health': 40 + random.randint(10, 20) + p.stats['health']/5}
	# abbreviations for stats
	abbr = {'A': 'attack', 'D': 'defense', 'S': 'speed', 'M': 'magic', 'H': 'health'}

	print "\nYou head over to the fighter shop in town."
		
	# loops until the player is done shopping
	while True:
		print "\nYour current stats are:\nAttack - %s, Defense - %s, Speed - %s, Magic - %s, Health - %s." % (
			p.stats['attack'], p.stats['defense'], p.stats['speed'], p.stats['magic'], p.stats['health'])
		print "You have %s gold to spend, and here is what there is to purchase:" % p.money
		choice = getInput("\nUpgrade Sword - $%s (A), Strengthen Shield - $%s (D), Boost Speed - $%s (S), Increase Magic - $%s (M), Buff Health - $%s (H), or you can leave the store to fight more (B)." % (
			costs[abbr['A']], costs[abbr['D']], costs[abbr['S']], costs[abbr['M']], costs[abbr['H']]), 'A D S M H B')
		# leaves the store
		if choice == 'B':
			return True
		
		stat = abbr[choice]
		#  checks that the player can purchase the chosen upgrade
		if costs[stat] <= p.money:
			p.money -= costs[stat]

			if choice == 'A': upgrade = [2, random.randint(5, 15), "Your sword is stronger!"]
			elif choice == 'D':	upgrade = [1, random.randint(8, 18), "Your shield is tougher!"]
			elif choice == 'S': upgrade = [1, random.randint(12, 24), "You feel faster!"]
			elif choice == 'M': upgrade = [2, random.randint(4, 17), "Magic flows through your veins!"]
			elif choice == 'H': upgrade = [5, random.randint(10, 20), "You feel healthier!"]

			p.stats[stat] += upgrade[0]
			costs[stat] += upgrade[1]
			print upgrade[2]

		else: print "You can't afford that!"

def main():
	"""runs everything in the game from here"""

	# options for automatically entering the shop and automatically starting fights
	global autoShop
	global autoFight

	while True:
		# always goes to the shop
		autoShop = fast
		# fights automatically after shopping
		autoFight = fast 
		global p
		p = Player()
		if cheat:
			p.money += 5000000

		print "\nWelcome to Dragon Fighter RPG! (v. 3.1)\nTo end the game at any time, just enter QUIT. You can also enter AUTO to change settings."
		print "Can you defeat all 5000 dragons in the arena? Test your strength!"
		if fast == True:
			p.name = 'Nikki'
		else:
			p.name = raw_input("\nFirst, what is your name?\n")
		print "\nWelcome to the dragon arena, %s!" % p.name

		alive = fight(p, d, 'p')
		# loops until death or quit
		while alive:

			choice = '' 

			if not autoShop:
				choice = getInput("\nWould you like to go to fight again (F), shop (S), or automatically shop (A)?", 'F S A')
			if choice == 'A':
				autoShop = True
			if autoShop or choice == 'S':
				shop(p)

			if not autoFight and choice != 'F':
				choice = getInput("\nFight again (F), Automatically fight from now on (A), or quit (QUIT)?", 'F A')
			if choice == 'A':
				autoFight = True

			firstStrike = random.randint(0, 100)
			# player goes first
			if firstStrike > 70 - p.stats['speed']:
				firstStrike = 'p'
			# dragon goes first
			else:
				firstStrike = 'd'
			alive = fight(p, d, firstStrike)

		print "You were able to kill %s dragons, and had %s gold. Better luck next time, %s!" % (p.kills, p.money, p.name)
		if getInput("Do you want to start over? y/N", "Y N") == 'N':
			# user quit
			break

	# only reached if player dies and does not want to retry
	exit(0)

# initialized here to allow stat print on death
p = Player
d = Dragon()
# runs the game
main()