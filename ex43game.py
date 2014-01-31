# Exercise 43: Basic Object-Oriented Analysis and Design
# http://learnpythonthehardway.org/book/ex43.html 

# FINAL

'''
A text-only game written in Python. This is based on exercise 43 in Zed Shaw's free online book _Learn Python the Hard Way_. Things I have added include a way to carry and set the bomb and a countdown announcement that runs after the bomb has been set. 

You can run the game in Terminal by typing: python ex43game.py  
'''

from sys import exit  # for quitting the game 
from random import randint
import time  # for the countdown 

#  I had to make global vars for the bomb because it moves from room to room 
#  at least I think I had to do it this way 
#  and the timer also needs to be used in more than one room 

bomb_with_hero = False
bomb_armed = False
ticks = time.time()


class Scene(object):
    '''
    All the rooms in the spaceship are child-classes of Scene(). None of 
    them override its enter() function. Conveniently, Scene() puts the 
    global vars into every room. 
    '''

    def enter(self):
        print self.name # works
        print self.descrip # works
    # this applies to all classes under Scene, but Zed does it differently
    # seems to me this is more efficient - every scene prints its name & descrip
    
    # make global vars explicit in every scene -- 
    # maybe should be in an __init__ instead? But this works 
        global bomb_with_hero
        global bomb_armed
        global ticks
        self.countdown = Countdown() # places a countdown object in every scene

class Engine(object):
    '''
    Engine has the play() function, which is an infinite loop that runs the 
    game until you either win or die! All scenes return to this loop, and the 
    loop sends you to the next scene. 
    '''

    def __init__(self, scene_map):
        self.scene_map = scene_map
        # gets the game's map from instance "mymap," at bottom of this file 
        
        print "\nTHE GAME"
        print "\nAliens have invaded your spaceship and you must go from "
        print "room to room, defeating them, so you can escape to the planet "
        print "below. The game is text only. It accepts simple commands such "
        print "as look, leave, open, fight, and take. You can type complete "
        print "sentences to tell it what you want to do."
        print "\nIn one of the rooms, there is a bomb. It would be a good "
        print "idea for you to find it and arm it before you escape."

    def play(self):
        current_scene = self.scene_map.opening_scene()
        # see the Map object: this runs function named opening_scene()
        # this runs only once 
        # this STARTS THE GAME
        
        while True: # infinite loop to run the game - repeats until exit() 
            print "\n--------"
            current_scene.enter()  # from Scene 
            
            #  note: will throw error if no new scene passed in by next line: 
            next_scene_name = current_scene.action() 
            #  get the name of the next scene from the action() function that
            #     runs in the current scene - what it returns 
            #     Thus - action() in each scene MUST return a string 
            #     used as a key in Map() class dictionary 

            current_scene = self.scene_map.next_scene(next_scene_name)
            #  here we use that val returned by current scene to go to
            #    the next scene, running function in Map 


class Bomb(object):
    '''
    The bomb can be taken in the armory and can be set on the bridge. No other 
    locations contain a bomb. 
    '''

    def __init__(self):
        self.present = True # this allows us to remove the bomb   

    def takebomb(self):
        while True:
            response = raw_input("> ")
            if "case" in response or "open" in response:
                print "You open the case and look inside. Yep. It's a bomb!"
                print "You close the case. It has a convenient handle for carrying."
            elif "take" in response or "pick up" in response:
                print "You pick up the case by its handle. It is not too heavy."
                print "Thank goodness -- because you are not in the best of shape."
                self.present = False
                global bomb_with_hero
                bomb_with_hero = True # now bomb is being carried 

            elif "arm" in response or "set" in response:
                print "I don't think you want to do that yet."
            elif "bomb" in response:
                print "Do you want to do something with the bomb?"
            elif "leave" in response or "exit" in response:
                return 'corridor' # returns to the return in Armory()
            else:
                print "Huh? What?"

    def setbomb(self):
        print "You set the case down and open it. You see a big switch "
        print 'marked "On/Off." It is set to "Off." You flip the switch!'
        global bomb_armed
        bomb_armed = True
        global ticks
        ticks = time.time() # this changes ticks to the time when bomb is set
        print
        print 'The bomb timer now reads "00:00:30."'
        print "I think you'd better hurry to the escape pod!" 
        global bomb_with_hero
        bomb_with_hero = False # now bomb is not being carried 


class Countdown(object):
    '''
    This is a sweet little object that talks to a global var, ticks. When the 
    bomb is set, it resets the value of ticks to "the time in seconds since 
    the epoch." Apparently that was midnight (UTC) on January 1, 1970. Anyway, 
    any time you call time.time() you'll get a later (higher) number of 
    seconds, so we use that to find how many seconds have passed since you set 
    the bomb. Use int() to shave off the milliseconds.
    '''
# http://docs.python.org/2/library/time.html#time.time 

    # I love how this works - a lucky accident for me 
    def announce(self, basetime):
        nowticks = time.time()
        timeleft = 30 - int(nowticks - basetime)
        global bomb_armed
        if bomb_armed and timeleft > 0:
            print 'The ship\'s computer announces: "The explosive device will '
            print 'detonate in %d seconds."' % timeleft
        elif bomb_armed:
            print "\nThe ship explodes into a quadrillion pieces! "
            print "Your mortal remains are flung to the far corners of the universe!"
            print "Goodbye!\n"
            exit()
        else:
            pass # this is important 
            # bomb timer announcement prints ONLY if bomb_armed is True


class Alien(object):
    '''
    We can create a new alien in any room. The fight is quite simplistic. 
    '''

    def __init__(self):
        self.present = True
        self.stamina = 10

    def report(self, s):
        if s > 8:
            print "The alien is strong! It resists your pathetic attack!"
        elif s > 5:
            print "With a loud grunt, the alien stands firm."
        elif s > 3:
            print "Your attack seems to be having an effect! The alien stumbles!"
        elif s > 0:
            print "The alien is certain to fall soon! It staggers and reels!"
        else:
            print "That's it! The alien is finished!"

    def fight(self, stam, loc): # stamina and scene key 
        while stam > 0:
            response = raw_input("> ")
            # fight scene
            if "hit" in response or "attack" in response:
                less = randint(0, stam)
                stam -= less # subtract random int from stamina 
                self.report(stam) # see above 
            elif "fight" in response:
                print "Fight how? You have no weapons, silly space traveler!"
            elif "run" in response:
                print "Sadly, there is nowhere to run.",
                print "The spaceship is not very big."
            else:
                print "The alien zaps you with its powerful ray gun!"
                return True, 'death'
        return False, loc


class Death(Scene):
    '''
    Mainly this pops up if you press Enter/Return without typing anything.
    '''

    name    = "You have died!"
    descrip = '''    Your spirit leaves swiftly as your body collapses.\n''' 
    
    def action(self):
        exit() # this is Death, so game over


class CentralCorridor(Scene):
    '''
    An alien is already standing here. Must be defeated before continuing. 
    You can get to all the other rooms from here.
    '''

    def __init__(self):
        self.alien = Alien()
        # initialize the corridor scene with an alien present 

    name    = "Central Corridor"
    descrip = '''    A broad passage extends in front of and behind you.
    There are doors to your left and right. The is a ladder going up.''' 
    
    def action(self):
        # -----
        # shortcut to pod scene - 3 lines
        # global bomb_armed
        # bomb_armed = True
        # self.alien.present = False
        # -----
        if self.alien.present:
            print "    An alien is here."
            self.alien.present, location = self.alien.fight(self.alien.stamina, 'corridor')
            # catch the returns from fight() in Alien -
            # pass in stamina and location, get out present and scene name
            return location # note: this might be Death() from the fight 
        else:

            while True:
                # bomb timer announcement here - relies on Scene()
                self.countdown.announce(ticks)
                response = raw_input("> ")
                if "look" in response:
                    print self.descrip
                elif "bomb" in response:
                    if bomb_with_hero:
                        print "You are carrying the bomb."
                    else:
                        print "There is no bomb here."
                elif "up" in response or "ladder" in response:
                	return 'bridge'
                elif "right" in response:
                	return 'armory'
                elif "left" in response:
            	    return 'pod'
                elif response != "":
                    print "Huh? I didn't understand that."
                else:
                    print "Something went wrong ..."
                    return 'death'


class LaserWeaponArmory(Scene): # keypad works! 
    '''
    This is where the hero gets a neutron bomb to blow up the ship before 
    going to the escape pod. It has a keypad he/she has to guess the number for.
    '''

    def __init__(self):
        self.doorlocked = True # self.door.locked threw an error 
        self.keycode = randint(1, 9) * 111 # 3 of the same number 
        self.bomb = Bomb()
        # initialize the armory scene with door locked and bomb here

    name    = "Laser Weapon Armory"
    descrip = '''    The door to this room is closed and locked.  
    There is a digital keypad set into the wall.'''
    descrip2 = '''    Shelves and cases line the walls of this room. 
    Weapons of every description fill the shelves and cases. '''
    
    def action(self):
        global bomb_with_hero  # lets Python know we will use this 
        while True:
            # bomb timer announcement here - relies on Scene()
            self.countdown.announce(ticks)
            if self.doorlocked:
                return self.keypad() # magic! 
                # the function keypad() returns a Map key, which THIS then 
                # returns to the Engine!
            else:
                response = raw_input("> ")
                if "look" in response:
                    print self.descrip
                    print "    Are you looking for anything in particular?"
                elif "bomb" in response and self.bomb.present:
                    print "Searching the shelves, you discover a small red case."
                    print 'On the case is a label: "Neutron Bomb."'
                    return self.bomb.takebomb()
                elif "bomb" in response and bomb_with_hero:
                    print "You are carrying the bomb."
                elif "leave" in response or "exit" in response:
                    return 'corridor'
                elif response != "":
                    print "Huh? I didn't understand that."
                else:
                    print "Something went wrong ..."
                    return 'death'

    # this should probably not be infinite - probably should have range instead 
    def keypad(self):
        print "    The keypad has 9 buttons with numbers from 1 to 9."
        print "    3 numbers must be entered to unlock the door."
        while self.doorlocked:
            response = raw_input("> ")
            if "leave" in response or "exit" in response:
            	return 'corridor' 
            elif not response.isdigit() or (int(response) > 999 or int(response) < 100):
                print "That is not a suitable number. Try again."
            elif int(response) == self.keycode:
                self.doorlocked = False
                print "The door slides smoothly and quietly open."
                self.descrip = self.descrip2 # switches the description text 
                return 'armory' # will print new descrip now 
            elif int(response) > self.keycode:
                print "That number is too high."
            elif int(response) < self.keycode:
                print "That number is too low."
            else:
                "No good. Try again with 3 numbers."


class TheBridge(Scene):
    '''
    Another battle scene with an alien before the hero can place the bomb here.
    '''
    def __init__(self):
        self.alien = Alien()
        # initialize the corridor scene with an alien present 
        # I can't initialize a bomb because one is not here yet 
        # exactly the same alien as we saw in corridor, new instance  

    name    = "The Bridge"
    descrip = '''    Clearly this is a central command station of the 
    spaceship. A wide viewscreen shows the stars against a black  
    curtain of empty space. There is a ladder going down.''' 
    
    def action(self):
        if self.alien.present:
            print "    Another alien is here!"
            self.alien.present, location = self.alien.fight(self.alien.stamina, 'bridge')
            # catch the returns from fight() in Alien -
            # pass in stamina and location, get out present and scene name
            return location # note: this might be Death() from the fight 
        else:
            while True:
                # bomb timer announcement here - relies on Scene()
                self.countdown.announce(ticks)
                response = raw_input("> ")
                if "look" in response:
                    print self.descrip
                elif "down" in response or "ladder" in response:
                    return 'corridor'
                elif "bomb" in response:
                    if bomb_armed:
                        print "That bomb is set to blow! Get out!!"
                    elif bomb_with_hero:
                        self.bomb = Bomb() # create a Bomb object here 
                        self.bomb.setbomb() # arm the bomb 
                    else:
                        print "There is no bomb here."
                    # the order above is very important 
                elif response != "":
                    print "Huh? I didn't understand that."
                else:
                    print "Something went wrong ..."
                    return 'death'


class EscapePod(Scene):
    '''
    Where the hero escapes, but only after guessing the right escape pod.
    '''

    name    = "Escape Pod"
    descrip = '''    Set into the wall are several closed and locked 
    hatch doors. Each one leads to an escape pod. The pods are 
    numbered 1 through 5.''' 
    
    def action(self):
        podnum = randint(1, 5)
        while True:
            # bomb timer announcement here - relies on Scene()
            self.countdown.announce(ticks)
            response = raw_input("> ")
            if "look" in response:
                print self.descrip
            elif "bomb" in response:
                if bomb_with_hero:
                    print "You are carrying the bomb."
                else:
                    print "There is no bomb here."
            elif "open" in response:
                choice = int(raw_input("Which pod? "))
                if choice == podnum:
                    self.pod_eject()
                elif choice > 5:
                    print "There are only 5 pods, silly space traveler!"
                else:
                    print "That hatch seems to be jammed."
            elif "pod" in response:
                print "What do you want to do with the pod?"
            elif "leave" in response or "exit" in response:
            	return 'corridor'
            elif response != "":
                print "Huh? I didn't understand that."
            else:
                print "Something went wrong ..."
                return 'death'

    def pod_eject(self):
        print "Ejected! You are safe!"
        global bomb_armed
        if bomb_armed:
            print "Your ship explodes in a quadrillion pieces, flinging "
            print "alien body parts to the far corners of the universe!"
            print "Safe in your cozy pod, you fly away to a nice planet.\n"
            exit() 
        else:
            print "\nUm ... did you forget something? The aliens are firing "
            print "torpedoes at you from your own ship! Aaaiiieeee --" 
            print "That is the end of you!\n"
            exit() 

 
class Map(object):
    '''
    Map tells us where we are and where we can go. It does not make us move - 
    Engine does that. Engine is up near the top. Map must follow all the 
    scene classes because of the dictionary here --
    '''

    scenes = { 
         'death'    : Death(),
         'corridor' : CentralCorridor(),
         'armory'   : LaserWeaponArmory(),
         'bridge'   : TheBridge(),
         'pod'      : EscapePod()
    }
    # above is a dictionary that maps all our scene classes to strings 
    # note, we never have to instantiate those classes (why?) 
    
    def __init__(self, start_scene_key):
        self.start_scene_key = start_scene_key
        # above we make a local var named start_scene_key
        # this is a string, same as the arg we passed in ('corridor')
        # start_scene_key remains unchanged throughout the game 

    def next_scene(self, scene_name):
        val = Map.scenes.get(scene_name)
        # above is how we get value out of the dictionary named scenes 
        return val
        # Zed does not have this return 
        # this function can be called repeatedly in the game, 
        # unlike opening_scene, which is called only ONCE 

    def opening_scene(self):
        return self.next_scene(self.start_scene_key)
        # this function exists only for starting, using the first 
        # string we passed in ('corridor')
        # it combines the previous 2 functions and is called only once 
        # (called in Engine) 


mymap  = Map('corridor')  # instantiate a new Map object w/ one arg
mygame = Engine(mymap)    # instantiate a new Engine object w/ one arg
mygame.play()             # call function from that Engine instance

