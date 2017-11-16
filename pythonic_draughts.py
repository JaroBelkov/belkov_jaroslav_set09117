main_path = 'C:\Pythonic Draughts'#:~~~~~
# title: Pythonic Draughts
# author: Jaroslav Belkov
# description: English Draughts game

try:  # Wraps the whole program.

	# import built-in modules:
	import os
	import importlib
	import random
	random.seed(version=2)
	import time
	import datetime

	# CORRECT INSTALLATION CHECK
	example_alert = main_path
	while True:
		try:
			os.chdir(main_path)
			if os.path.isfile("pd_config.py") and (os.path.isfile("pd_functions.py") or os.path.isfile("pd_functions.pyc")) and (os.path.isfile("pythonic_draughts.py")  or os.path.isfile("pythonic_draughts.pyc")):
				break 	# out of the while loop
				
			raise FileNotFoundError
		except FileNotFoundError:
			try:
				main_path = input(get_path_alert)
				if main_path == "stop":
					raise Exception("pd_end_by_user") # for python shell users
		
				get_path_alert = "\n Ooops! Could not follow this specified path: " + str(main_path) + "\n Please, specify the path to the folder containing:\n     - pythonic_draughts.py\n    - pd_functions.py\n Do not include files names. Do not use quotes.\n Example: '" + example_alert + "'.\n Or type 'stop' to terminate. -> "
				continue 	#do loop
			
			except NameError as e:
				get_path_alert = "\n Please, specify the path to the ~~~Pythonic~Draughts~~~ files. Example: '" + example_alert + "'.\n Or type 'stop' to terminate. -> "
				main_path = os.getcwd()
				print (main_path)
				continue	# do loop
					
	try:
		if get_path_alert and os.path.isfile("pythonic_draughts.py"):
			del get_path_alert # for python shell users: if they terminate the program and then re-launch it, global variables are still present
			do_compile = ""
			if os.path.isfile("pythonic_draughts.pyc"):
				do_compile = " and re-compile pythonic_draughts.py to pythonic_draughts.pyc"
			
			print ("\n It seems that the path to the Pythonic Draughts installation was changed to '." + main_path + "'.")
			the_answer = input("\n Would you like to save this path" + do_compile + "?\n\n Enter 'y' to save, or any key to continue without saving. -> ")
			if the_answer == "y":
				with open("pythonic_draughts.py", mode='r', encoding='utf-8') as my_file:
					my_code = my_file.read()
					
				my_index = my_code.index("#:~~~~~")
				my_code = "main_path = " + "'" + main_path + "'" + my_code[my_index:] 
				with open("pythonic_draughts.py", mode='w', encoding='utf-8') as my_file:
					my_file.write(my_code)
				
				
				
				if os.path.isfile("pythonic_draughts.pyc"):
					os.remove("pythonic_draughts.pyc")
					import py_compile
					py_compile.compile(main_path + '/pythonic_draughts.py', main_path + '/pythonic_draughts.pyc')
					
				print("\n New path was saved successfully\n")
	except NameError:
		pass


	# GLOBAL CONSTANTS DECLARATION AND INITIALISATION:

	pieces_graphics = ((),(" W ", " o ", " . ", " x ",  " R "), (" R ", " x ", " . ", " o ", " W ")) # for draw_board()
		# pieces_graphics = ((limbo),(white king, white man, empty reachable field, red man, red king),(reversed pieces_graphics[1]))	
	no_spaces = (4,12,20,28) # for draw_board()

	two_spaces = (8,16,24) # for draw_board()

	red_or_white = ("random choice!","Red","White") # using who_am_I for output for the user

	translator_data = ((),('','g1', 'e1', 'c1', 'a1', 'h2', 'f2', 'd2', 'b2', 0, 'g3', 'e3', 'c3', 'a3', 'h4', 'f4', 'd4', 'b4', 0, 'g5', 'e5', 'c5', 'a5', 'h6', 'f6', 'd6', 'b6', 0, 'g7', 'e7', 'c7', 'a7', 'h8', 'f8', 'd8', 'b8'),('','b8', 'd8', 'f8', 'h8', 'a7', 'c7', 'e7', 'g7', 0, 'b6', 'd6', 'f6', 'h6', 'a5', 'c5', 'e5', 'g5', 0, 'b4', 'd4', 'f4', 'h4', 'a3', 'c3', 'e3', 'g3', 0, 'b2', 'd2', 'f2', 'h2', 'a1', 'c1', 'e1', 'g1')) # for translate()

	central_squares = (15,16,20,21) # for AI strategical decision making in get_ais_move()

	lead_to_central_squares = (10,11,12,13,15,16,17,20,21) # for AI strategical decision making in get_ais_move()

	on_off = ("", "on", "off") # for output for the user in Settings menu

	#IMPORT SETTINGS FROM pd_config.py AND INITIALISE CONFIGURABLE GLOBAL VARIABLES:

	from pd_config import auto_move			 # When set to 1 and there only is one possible move, it is played automatically
	from pd_config import auto_replay 		 # When set to 1, 'Replay' is played automatically, otherwise needs user's input after every move replayed
	from pd_config import ar_delay 			 # Length of delay between moves if auto-replay is on. Float in pd_config, then converted to 3 characters string.
	from pd_config import is_gui			 # When set to 1, will save current position for pytonick_draughts_gui.html
	from pd_config import diff_level		 # list [0, x, y]. x for difficulty level of red player, y for the level of white player
	from pd_config import default_who_am_I   # set to 1: red plays first. Set to -1: white plays first. Set to 0: random choice.
	from pd_config import default_main_position # Not configurable via Settings menu! More information in comments on main_position[] and in README.md
	
	if auto_replay > 0:
		ar_delay = " and the delay between moves is set to seconds: " + str(ar_delay)
	else:
		ar_delay = ""
	old_auto_replay = auto_replay
	old_auto_move = auto_move


	# GLOBAL VARIABLES DECLARATION:
	main_position = []  # Two-dimensional list of lists (a.k.a. array with a different width of rows) records the current position in the game.
						# - On the start of a new game assigned with a start position from pd_config.py via imported variable default_main_position.
						# 	The game is distributed with the position of English Draughts as described on https://en.wikipedia.org/wiki/English_draughts). 
						#   For a game variations, which have different start position, this var needs to be changed manually in pd_config.py.
						#	Please, read the following comment and README.md carefully before any manual changes in configuration file.
						# - First row consists of 5 elements and is only used to record auxiliary information:
						#		main_position[0][0]: Tracks number of moves without capturing.
						#		main_position[0][1]: total number of red pieces on the board.
						#		main_position[0][2]: 1 if a man promoted to king during the most recent move, otherwise 0.
						#		main_position[0][3]: number of captured kings in the most recent move (0+).
						#		main_position[0][4]: total number of white pieces on the board.
						# - Both second and third rows consist of 35 elements each. Elements represent the "value" of a square of the gaming board.
						#		Indexes of elements in a row correspond to the following squares of the board:
						#		##################
						#		#  01  02  03  04#
						#		#05  06  07  08  #
						#		#  10  11  12  13#
						#		#14  15  16  17  #
						#		#  19  20  21  22#
						#		#23  24  25  26  #
						#		#  28  29  30  31#
						#		#32  33  34  35  #
						#		##################
						#	  !Four elements indexed [0], [9], [18], [27] are not used (void, limbo) to improve program's performance avoiding unnecessary conditioning.
						# - Second row consists of "values" of squares from red player's point of view:
						# 		0 = empty square.
						# 		1 = red checker (man). 
						# 		2 = red king
						# 		-1 = white man
						# 		-2 = white king
						# 		3 - limbo
						# - Third row row consists of "values" of squares from white player's point of view:
						# 		0 = empty square.
						# 		1 = white man. 
						# 		2 = white king
						# 		-1 = red man
						# 		-2 = red king
						# 		3 - limbo
						# - !Therefore the third row is reversed and negated second row except for limbo - these indexes (0, 9, 18, 27) are always assigned with the number 3
						# - !No other values than int(-2 to 3) are ever assigned to elements of second and third rows of main_position array
						
	who_am_I = 0  	# variable used to identify which player is to move. Initial value imported from pd_config.py.
					# Number 1 for red, number -1 for white. Never gets any other values! Even set to 0 in pd_config.py, will invoke random choice of (-1, 1)
					# Widely used to improve program's performance avoiding unnecessary conditioning. Example:
						# print (main_position[who_am_I]) outputs the second row (indexed [1]) if who_am_I = 1 or the third row (indexed [2] or [-1]) if who_am_I = -1

	game_history = [] # LIFO list of tuples. After each move, a new position's record is appended as a tuple. On 'Undo' the last two are popped out
						# 																						('Undo' undoes 2 moves at a time).
						# On the start of a new game assigned with start position from main_position.
	redo_stack = [] # LIFO list of tuples. Fills from game_history when 'Undo' or 'Replay' is used.
					# 						On 'Redo' last tuple is popped out and appended to game_history.  ('Redo' redoes one move at a time).
					# Also is filled up on load game from a file: to be replayed.

	# 			position's record in redo_stack and game_history (below) is made of the second row of main_position by removing limbo and converted to tuple


	# GET FUNCTIONS that may be adjusted to change the game variation. These are for English Draughts.
	from pd_functions import get_possible_moves # Gets all possible moves from all squares with value > 0 and < 3 in main_position[who_am_I]
												# Parameter: strictly list of 35 integers in range -2:3. Usually main_position[1] or [2]. 
												# Returns two dimensional array (list of lists), where each row represents a possible move in the following format:
												# elements of a row:
												#	 	col[0]  = start square. 
												#	    col[-1] = end square.
												#	 !if longer than 2 elements, it is a jump
												# 		col[1] and all following odd indexed elements = squares to be set to 0 (captured pieces)
												#       col[2] and all following even indexed elements apart from the last
												# 											= inter-jump squares. Only exist, if it is a multiple jump. 
																																										
	from pd_functions import get_mans_leaps 	# recursion used in get_possible_moves()
	from pd_functions import get_kings_leaps 	# recursion used in get_possible_moves()
	from pd_functions import get_mans_jumps 	# used in get_possible_moves()
	from pd_functions import get_kings_jumps 	# used in get_possible_moves()
	from pd_functions import update_main_position 	# Used to update main_position array when a move is made
													# Parameters:
													#  - the_move: list of integers in range 1:35 exclusive 9,18,27 
													#		It is usually one element of the list from the return of get_possible_moves()
													#  - who_am_I : integer 1 or -1 (who_am_I)
													#  - position: two dimensional array strictly in format of main_position (see above).
													#		!It is usually main_position passed to this function.
													# Returns a two dimensinal array in format of main_position

	def my_induction(x,n):  # returns x + x^2 +...+ x^n
		if n < 1:
			return 0
		else:
			return x**n + my_induction(x,n-1)												
													
	def draw_board(): # draws text-based board to the console
		if who_am_I == -1:
			j = 2
			board = "1.    "
			i = 1
			for piece in main_position[1]:
				if piece == 3:
					continue
				board += pieces_graphics[1][piece+2]
				if i in no_spaces:
					board += "\n" + str(j) + ". "
					j +=1
				elif i in two_spaces:
					board += "   \n"+ str(j) + ".    "
					j +=1
				else:
					board += "   "
				i += 1
			board += "\n    h  g  f  e  d  c  b  a"
		else:
			j = 7
			board = "8.    "
			i = 31
			for piece in main_position[2]:
				if piece == 3:
					continue
				board += pieces_graphics[2][piece+2]
				if i in no_spaces:
					board += "\n" + str(j) + ". "
					j -=1
				elif i in two_spaces:
					board += "   \n"+ str(j) + ".    "
					j -=1
				else:
					board += "   "
				i -=1
			board += "\n    a  b  c  d  e  f  g  h"
		
		print()
		print (board)
		print()
		return
		
	def translate(one_move):	# changes move's notation to understandable chess notation to present to the user in the console.
		translated_move = translator_data[who_am_I][one_move[0]] + "-" + translator_data[who_am_I][one_move[-1]] + " "
		for i in range(1, len(one_move)-1, 2):
			translated_move += " X" + translator_data[who_am_I][one_move[i]]
		
		return translated_move

	def save_position_for_gui(possible_moves): # !Not a part of the project. Pythonic_draughts_gui.html then uses the saved file.
		possibleMoves_for_gui = "possibleMoves = [[ "
		for i in range(len(possible_moves)):
			for item in possible_moves[i]:
				possibleMoves_for_gui += str(item) + ", "
			possibleMoves_for_gui = possibleMoves_for_gui[:-2] + "],["
		possibleMoves_for_gui = possibleMoves_for_gui[:-2] + "];\n"
		
		myMove_count = "move_count = " + str(move_count)  + ";\n"
		myWho_am_I = "who_am_I = " + str(who_am_I) + ";\n"
		myArray = "myArray = ["
		for item in main_position[1]:
			myArray = myArray + "\"" + str(item) + "\", "
		myArray = myArray[:-2] + "];\n"
			
		with open(main_path + "/pd_gui/position_data.js", mode='w', encoding='utf-8') as my_file:
			my_file.write(possibleMoves_for_gui)
		with open(main_path + "/pd_gui/position_data.js", mode='a', encoding='utf-8') as my_file:
			my_file.write(myMove_count)
		with open(main_path + "/pd_gui/position_data.js", mode='a', encoding='utf-8') as my_file:
			my_file.write(myArray)
		with open(main_path + "/pd_gui/position_data.js", mode='a', encoding='utf-8') as my_file:
			my_file.write(myWho_am_I)
		
	def save_game():
		global game_history
		
		# construct default filename from the current date and time:
		get_date = datetime.datetime.now()
		file_name = "my_game_on_" + str(get_date.day) + "_" + str(get_date.month) + "_" + str(get_date.year) + "_at_" + str(get_date.hour) + "_" + str(get_date.minute)
		# get user's input (the filename)
		alert = " Please, enter a file name or hit enter to save the game as " + file_name + ".\n Alternatively, enter 'Q' to return without saving. -> "
		while True:
			new_file_name = input(alert)
			if new_file_name.lower() == "q":
				return 
				
			alert = "\n Something went wrong. Probably, entered value is not a valid file name. Please, check https://en.wikipedia.org/wiki/Filename for further advise.\n\n" + "  Please, enter a valid file name or hit enter to save the game as " + file_name + " -> "
			if not new_file_name: # Hit enter means agree with default filename
				new_file_name = file_name
			
			new_file_name = main_path + "/myGames/" + new_file_name + ".pdh"
			try:
				with open(new_file_name, mode='w', encoding='utf-8') as my_file:
					my_file.write(game_history[0] + ";")
			except OSError: # invalid filename
				continue #do loop
			
			break #continues on the next source code line
			
		with open(new_file_name, mode='a', encoding='utf-8') as my_file:
			for i in range (1, len(game_history)):
				my_file.write(game_history[i] + ";")
				
		print ("\n The game was saved as %s\n" %new_file_name)
		return 
		
	def get_humans_move():
		global main_position
		global game_history
		global who_am_I
		global redo_stack
		global move_count
		global game_mode
		global move_began_time
		global auto_move
		global old_auto_move
		global auto_replay
		global old_auto_replay
		
		possible_moves = get_possible_moves(main_position[who_am_I])
		if is_gui == 1:
			save_position_for_gui(possible_moves)
			
		if redo_stack and auto_replay == 1:
			move_number = 7
			possible_moves = []
			time.sleep(float(ar_delay[-3:]))
		else:
			if not possible_moves:
				return 0 # no moves = lost the game
				
			if len(possible_moves) == 1 and auto_move == 1:
				print(" AUTOMATIC MOVE %s OCCURED!\n" %translate(possible_moves[0]), end = "", flush = True)
				time.sleep(0.4) 
				print(".", end = "", flush = True)
				time.sleep(0.3) 
				print("..", end = "", flush = True)
				time.sleep(0.2) 
				print("...", end = "", flush = True)
				time.sleep(0.1)
				print("....")
				time.sleep(0.1) 
				return possible_moves[0]
			
			# Print menu with moves
			for i in range(len(possible_moves)):
				print(" %d.  %s" %(i+1, translate(possible_moves[i])))
			
			j = i
			quick_tip = ""
			if redo_stack:
				print (" %d. Hand over   %d. Offer draw   %d. Resign   %d. Save/Quit   %d. Replay    %d. Undo    %d. Redo\n" %(i+2, i+3, i+4, i+5, i+6, i+7, i+8))
				quick_tip = "\n Tip: you can use 'Redo' option hitting the 'Enter' key instead of entering the number of your 'Redo' choice ;)"
			elif len(game_history) > 2:
				auto_move = old_auto_move
				auto_replay = old_auto_replay
				print (" %d. Hand over   %d. Offer draw   %d. Resign   %d. Save/Quit   %d. Replay    %d. Undo\n" %(i+2, i+3, i+4, i+5, i+6, i+7))
				i -= 1
			else:
				print (" %d. Hand over   %d. Offer draw   %d. Resign   %d. Quit\n" %(i+2, i+3, i+4, i+5))
				i -= 3
			
			# get users input
			move_number = 0
			alert = " Please, enter the number corresponding to your choice of action. " + quick_tip + "-> "
			
			while move_number < 1 or move_number > i+8:
				try:
					move_number = int(input("%s: " %alert))
					alert = (" Please, to select your choice use a whole number between 1 and %d. Try again." %(j+7))
					if move_count < 3 and move_number == len(possible_moves) + 6:
						alert = (" 'Undo' is not available! Please, choose a move or another action from the list by entering its number.")
						move_number = 0
				except ValueError:
					if redo_stack and not move_number:
						move_number = i+8
						
					alert = (" Please, to select your choice use a whole number (a number which is not a fraction) between 1 and %d. Try again." %(j+7))
				
	# Game menu options:
		# Hand over:
		if move_number == len(possible_moves) + 1:
			if game_mode != "pLp":
				alert = " 1. Get suggestion   2. Hand over to AI to play the rest of the game   3. Rotate the board   4. Switch to Player vs Player mode  -> "
				the_answer = 0
				while the_answer not in ('1','2','3','4'):
					the_answer = input(alert)
					alert = " Please, choose one of the four options by entering a number  -> "
					
				if the_answer == '1':
					move_began_time = time.time()
					buffer_ = diff_level[who_am_I]
					diff_level[who_am_I] = diff_level[who_am_I * -1]	
					print ("\n AI at the difficulty level " + str(diff_level[who_am_I]) + " suggests: %s" %translate(get_ais_move()))
					diff_level[who_am_I] = buffer_
					return "continue"
					
				elif the_answer == '2':
					game_mode = "aLa"
					return get_ais_move()
					
				elif the_answer == '3':
					game_mode = game_mode[2] + "L" + game_mode[0]
					return get_ais_move()
					
				else:
					game_mode = "pLp"
					return "continue"
			else:
				alert = " 1. Get suggestion   2. Hand over to AI to play for " + red_or_white[who_am_I] + "  -> "
				the_answer = 0
				while the_answer not in ('1','2'):
					the_answer = input(alert)
					alert = " Please, choose one of the two options by entering a number  -> "
				if the_answer == "2":
					game_mode = "aLp"
					if who_am_I == 1:
						game_mode = "pLa"
					move_began_time = time.time()
					return get_ais_move()
				else:
					move_began_time = time.time()
					print ("\n AI at the difficulty level " + str(diff_level[who_am_I]) + " suggests: %s" %translate(get_ais_move()))
					return "continue"
					
		# Draw offer:		
		if move_number == len(possible_moves) + 2: 
			if game_mode == "pLp":
				the_answer = input(" %s offers to draw the game. %s, do you accept? (input 'yes' or any key for 'no') -> " %(red_or_white[who_am_I], red_or_white[who_am_I * -1])).lower()
				if the_answer == "yes":
					return "tied"
				else:
					return "continue"
			elif will_draw > 20:
				print (" " + red_or_white[who_am_I * -1] + " says:")
				print (" Yeah, ok. GG! ;)")
				return "tied"
			else:
				print (red_or_white[who_am_I * -1] + " says:")
				print ("\n Nooo! :).\n   Lets play on!")
				return "continue"
				
		# Resignation:	
		if move_number == len(possible_moves) + 3: 
			the_answer = input(" Are you sure you want to resign from the game? (input 'yes' or any key for 'no') -> ").lower()
			if the_answer == "yes":
				return []
			else:
				return "continue"
		
		# Quit:
		if move_number == len(possible_moves) + 4: 
			the_answer = input(" Would you like to save the game or go to Main Menu? (input 's' to save, 'q' to quit,  or any other key to return to Game Menu) -> ").lower()
			if the_answer == "q":
				return "quit"
			elif the_answer == "s" and len(game_history) > 2:
				save_game()
			elif the_answer == "s":
				print (" Sorry, you have to play at least one move before saving the game.")
			
			return "continue"
			
		# Replay:	
		if move_number == len(possible_moves) + 5:
			redo_stack += reversed(list(game_history[1:]))
			main_position = [list(default_main_position[0]), list(default_main_position[1]), list(default_main_position[2])]
			game_history = [game_history[0]]
			while True:
				try:
					os.rename(main_path + "/myGames/backup.pdh", main_path + "/myGames/backup_previous.pdh") # to preserve what was in backup before the replay
				except FileExistsError:
					os.remove(main_path + "/myGames/backup_previous.pdh")
					# then loop
				except FileNotFoundError:
					break
			with open(main_path + "/myGames/backup.pdh", mode='w', encoding='utf-8') as my_file:
				my_file.write(game_history[0] + ";")
			
			who_am_I = old_who_am_I # who had the first move (if random then differs from default)
			move_count = 1
			game_mode = "pLp" # Only replays in "pp" mode. After replay the AI's side can be 'Hand over'-ed
			old_auto_move = auto_move
			auto_move = -1
			auto_replay = old_auto_replay
			if auto_replay == -1:
				print ("\n The game was set to the starting position. Please, use 'Redo' option to replay it.\n")
			else:
				print ("\n The game is being replayed.\n")
				
			return "continue"
			
		# Undo:	
		if move_number == len(possible_moves) + 6: 
			if not redo_stack:
				old_auto_move = auto_move
				old_auto_replay = auto_replay
				
			redo_stack.append(game_history.pop())
			redo_stack.append(game_history.pop())
			main_position = recreate_position(game_history[-1])
			auto_move = -1
			auto_replay = -1
			move_count -= 2
			with open(main_path + "/myGames/backup.pdh", mode='w', encoding='utf-8') as my_file:
				my_file.write(game_history[0] + ";")
			with open(main_path + "/myGames/backup.pdh", mode='a', encoding='utf-8') as my_file:
				for i in range (1, len(game_history)):
					my_file.write(game_history[i] + ";")
			
			return "continue"
		
		# Redo:
		if move_number == len(possible_moves) + 7: 
			game_history.append(redo_stack.pop())
			main_position = recreate_position(game_history[-1])
			move_count += 1
			who_am_I = who_am_I * -1
			with open(main_path + "/myGames/backup.pdh", mode='a', encoding='utf-8') as my_file:
				my_file.write(game_history[-1] + ";")
			
			return "continue"
		
	# The actual move is chosen. Return to caller:
		return possible_moves[move_number-1]

	def my_spider(position, for_who, level, extra_score): #recursion used in get_ais_move()

		possible_moves = get_possible_moves(position[for_who])
		if not possible_moves: # First of two base cases. No moves = the game is won/lost
			score_collector[the_move_number][for_who * who_am_I] += my_induction(position[0][for_who * -1], level + 2)
																# !The expression would emulate the value that score_collector would collect if my_spider() had continued
																# to recur without opponents pieces (moves). It also adds more weight in the evaluation expression
																# to this particular move value in score_collector:
																# 1. Level matters: it depends if win/loss is possibile the very next move, or just at the
																# 	very end of the branch. Level cannot be lower than -1, but negative and zero values 
																# 	are not needed: +2 solves the problem and adds strategical decision:
																#		- if win is possible: signify it!
																# 		- if loss is possible: better choose another move
																# 2. Values to collectors are added for every stage of recursion (using induction),
																# 		in contrast to non-ultimate moves, where only values from the farthest leafs are added up.
																			
			weight_collector[the_move_number][for_who * who_am_I] += position[0][for_who * -1] ** (level + 2)
			return
				
		for item in (possible_moves):
			preserved_position = [list(position[0]), list(position[1]), list(position[2])]
			preserved_position = update_main_position(item, for_who, preserved_position)
			counter_c[0] +=1
			extra_score += preserved_position[0][2] * who_am_I * for_who * 2 # add/substruct value if you/opponent can promote
			extra_score += preserved_position[0][3] * who_am_I * for_who * 2 # add/substruct if you/opponent can capture opponent's/yours king (for each caped king)
			if level >= 0:
				my_spider(preserved_position, for_who * -1, level - 1, extra_score)
			else:  # Second of two base cases. Of course, the for loop will run first.
				this_score = sum(preserved_position[who_am_I]) - 12	
				this_score += extra_score 
				if this_score > my_status:								# I'm getting better with this move..
					score_collector[the_move_number][2] += abs(this_score - my_status)
					weight_collector[the_move_number][2] += 1			# ..but how often in this branch?
					
				elif this_score < my_status:							# i'm worsening with this move..
					score_collector[the_move_number][1] += abs(this_score - my_status)
					weight_collector[the_move_number][1] += 1			# ..but how often in this branch?
					
				else:
					weight_collector[the_move_number][0] += 1         	# how often there is no change in my status
					
								
			extra_score -= preserved_position[0][2] * who_am_I * for_who * 2 # remove values before next item loops
			extra_score -= preserved_position[0][3] * who_am_I * for_who * 2 # remove values before next item loops
		
		return
		
	def get_ais_move():
		global the_move_number 	# the number of a move from possible_moves (index of a sublist)
		global counter_c 		# counts every update_main_position call
		global my_status 		# holds current value of the position of current AI player
		global weight_collector	# collector
		global score_collector 	# collector
		
		possible_moves = get_possible_moves(main_position[who_am_I])
		if is_gui == 1:
			save_position_for_gui(possible_moves)
			
		if not possible_moves:
			return 0 # no moves = lost the game
		
		will_draw = main_position[0][0]
		if game_mode == "aLa" and will_draw > 20:
			return "tied"
		
		if len(possible_moves) == 1:
			time.sleep(0.5) # for GUI 
			return possible_moves[0] #nothing to choose from (presumably a jump)
		
		if diff_level[who_am_I] == 0:
			time.sleep(0.5) # for GUI 
			return random.choice(possible_moves)	
			
	# Collect information from the farthest leafs:
		# initialise the collectors...
		my_status = sum(main_position[who_am_I]) - 12
		score_collector = [[0,0,0]]
		weight_collector = [[0,0,0]]
		for i in range (1, len(possible_moves)):
			score_collector.append([0,0,0])
			weight_collector.append([0,0,0])
		
		# ...determine the depth of recursion...
		level = diff_level[who_am_I]
			# game ending needs more possibilities to be considered:
		if main_position[0][1] + main_position[0][-1] <= 12: #Low level AI starts to do more or less random moves here, as a rule repetitive moves with king
			level += 1
			if level < 3:
				level = 3
		if main_position[0][1] + main_position[0][-1] <= 6: #Low level AI starts to do more or less random moves here, as a rule repetitive moves with king
			level += 1
			if level < 5:
				level = 5 # This should be at least 7 for the best outcome (7 moves are needed for a man on the back line to promote)
		
		if len(possible_moves[0]) > 2:  #if jump(s) possible,
			level +=1 					#then go one level deeper to see outcome (will retaliate?)
		
		# ...and traverse for each possible move:
		counter_c = [0] # just for fun to see how many recursions * loops where made
		extra_score = 0 # score added when promoted or captured opponents king
		print ("\n %s has %d possible moves. Calculating move number: " %(red_or_white[who_am_I], len(possible_moves)), end = "", flush = True)
		
		for the_move_number in range (len(possible_moves)):
			preserved_position = [list(main_position[0]), list(main_position[1]), list(main_position[2])] # !sending as function parameter does not preserve global main_position
			preserved_position = update_main_position(possible_moves[the_move_number], who_am_I, preserved_position)
			extra_score += preserved_position[0][2] * 2 # add extra 2 if promoted
			extra_score += preserved_position[0][3] * 2 # add extra 2 if captured opponent's king (for each caped king)
			print ("%d, " %(the_move_number + 1), end = "", flush = True)
			my_spider(preserved_position, who_am_I * -1, level, extra_score)
			extra_score -= preserved_position[0][2] * 2 # remove values before next item loops
			extra_score -= preserved_position[0][3] * 2 # remove values before next item loops
		print("\n %s has evaluated %d positions." %(red_or_white[who_am_I], counter_c[0]))
		
	# Evaluate gathered information:
		# prepare the value of each move...
		min_max = []
		for i in range (len(possible_moves)):
			try:
				min_max.append(round((score_collector[i][2] * weight_collector[i][2] - score_collector[i][1] * weight_collector[i][1 ])/(weight_collector[i][0] + weight_collector[i][1] + weight_collector[i][2])))
			except ZeroDivisionError: # This cannot happen! This handler remains here from alfa testing phase just for the sake of good programming practice
				min_max.append(0)
		
		# ...and compare them choosing the best:
		moves_to_choose_from = [possible_moves[0]]
		max_score = min_max[0]
													
		for i in range (1, len(possible_moves)):
			if min_max[i] > max_score: 
				moves_to_choose_from = list([possible_moves[i]])
				max_score = min_max[i]
			elif min_max[i] == max_score:
				moves_to_choose_from.append(possible_moves[i])
				
		if move_count < 20:		# if game opening, run comparsion again with 50% relief (strategical moves are more important)
			moves_to_choose_from = [moves_to_choose_from[0]]
			for i in range (len(possible_moves)):
				if min_max[i] * 1.5 >= max_score:
					moves_to_choose_from.append(possible_moves[i])
					
			if len(moves_to_choose_from) > 1: 			# = time to make a strategical decision
				min_max = [0]
				for i in range (1, len(moves_to_choose_from)):
					min_max.append(0)
					
				for i in range(len(moves_to_choose_from)):
					if moves_to_choose_from[i][0] > 4: # whatch your back.
						min_max[i] = 1
					if moves_to_choose_from[i][1] > 26 and main_position[who_am_I][moves_to_choose_from[i][0]] < 2: # try to promote, or shatter opp's defense.
						min_max[i] += 1
					if moves_to_choose_from[i][1]  > 31 and main_position[who_am_I][moves_to_choose_from[i][0]] < 2: # promote, if you can!
						min_max[i] += 1
					
					if moves_to_choose_from[i][0] not in central_squares and moves_to_choose_from[i][1] in central_squares: # try to secure the centre.
						min_max[i] = 1
					if moves_to_choose_from[i][0] not in central_squares and moves_to_choose_from[i][1] in lead_to_central_squares: # go closer to centre.
							min_max[i] += 1
				
				moves_to_choose_from_v2 = [moves_to_choose_from[0]]
				max_score = min_max[0]
				for i in range(1,len(moves_to_choose_from)):
					if min_max[i] > max_score:
						moves_to_choose_from_v2 = list([moves_to_choose_from[i]])
						max_score = min_max[i]
					elif min_max[i] == max_score:
						moves_to_choose_from_v2.append(moves_to_choose_from[i])
					
				moves_to_choose_from = moves_to_choose_from_v2	
								
	# Send back to caller	
		try:
		
			time.sleep(1 - time.time() + move_began_time)  #for GUI to delay for at least 1 second
		except ValueError:
			pass
			
		return random.choice(moves_to_choose_from)  # In the first 20 moves it is likely to get more than one moves to choose from due to strategical algorithm.
													# Also, probability to get more than one move raise as the number of pieces on the board diminish close to zero.
				
	def recreate_position(reds_position): #reformats position's record to the main_position format
		
		reds_position = [int(item) - 2 for item in reds_position]  
		whites_position = [item * -1 for item in reversed(reds_position)]
		reds = int(sum(item/item for item in reds_position if item >= 1))
		whites = int(sum(item/item for item in whites_position if item >= 1))
		for i in range (0, 28, 9):
			reds_position.insert(i,3)
			whites_position.insert(i,3)

		return ([[0, 0, reds, 0, whites], reds_position, whites_position])
		

########################################################################################################################################################################

	#main:
	start_game_input = ["aa", "pp", "pa", "ap", "q", "set", "l"] #possible user's inputs in main menu. ("r")eplay and ("s")ave are added when they become possible.
	settings_input = ["r", "w", "a", "b", "c", "q", "s"] #possible user's inputs in settings menu
	can_replay = "" 	 # used for users's input in main menu
	can_save = ""		 # used for users's input in main menu
	is_new_line = ""	 # used for users's input in main menu
	if os.path.isfile("pd_gui/pythonic_draughts_gui.html") and os.path.isfile("pd_gui/pythonic_draughts_gui.css"):
		settings_input.extend("z")

	try:
		os.mkdir("myGames")
	except FileExistsError:
		pass

	while True:	
		if game_history:
			can_replay = " * or 'R' to replay the last or uploaded game,                                     *"
			can_save =   " * or 'S' to save the last game,                                                   *"
			is_new_line = "\n"
			if "r" not in start_game_input:
				start_game_input.extend("r")
			if "s" not in start_game_input:
				start_game_input.extend("s")
		
		print ()
		print (" ***********************************  MAIN MENU  ***********************************")
		print (" *                                                                                 *")
		print (" * Please, select game mode:                                                       *")
		print (" * 'PP' for player vs player or 'PA' for player vs AI or 'AP' for AI vs player,    *")
		print (" * or 'Set' for SETTINGS,                                                          *")
		print (can_replay, end = is_new_line)
		print (can_save, end = is_new_line)
		print (" * or 'L' to load a saved game,                                                    *")
		print (" * or 'Q' to terminate.                                                            *")
		print (" *                                                                                 *")
		print (" *                                                                                 *")
		print (" *                                                      ~~~Pythonic~Draughts~~~    *")
		print (" *                                                          by Jaro Belkov (c)2017 *")
		print (" ***********************************************************************************")
		
		# Display current settings:
		print ("\n~ CURRENT SETTINGS.")
		print (" AI difficulty level:\n    - for player Red: %d\n    - for player White: %d" %(diff_level[1], diff_level[2]))
		print (" a) Automatic move is %s" %on_off[auto_move])
		print (" b) Automatic replay is " + on_off[auto_replay] + ar_delay )
		print (" c) The first move has: " + red_or_white[default_who_am_I])
		#print ("d. whatever")  - to add more options adjust settings_input and add if clause in 'if game_mode == "set":' below. 'q', 'r', 's' and 'w' are reserved!
		if "z" in settings_input:
			print (" z) Saving position for GUI is %s\n" %on_off[is_gui])
		
		alert = "\n Your choice from the MAIN MENU -> "
		game_mode = ""
		while game_mode not in start_game_input: #Tuple with possible inputs, declared and initialised at the top of this document
			game_mode = input(alert).lower()
			alert = " Please, only enter accepted parameters. -> "

	# Follow the user's input processing: 		
		if game_mode == "q": # Quit
			print (" Thank you for playing. Goodbye!")
			time.sleep(0.5) # for console users
			break # terminates '#main' loop, i.e. the program
			
		if game_mode == "r": # Replay
			redo_stack = list(game_history[1:])
			redo_stack.reverse()
			game_mode = "pp"
			old_auto_move = auto_move
			auto_move = -1
			if auto_replay == -1:
				print ("\n The game was set to the starting position. Please, use 'Redo' option to replay it.\n")
			else:
				print ("\n The game is being replayed.\n")
			# continues at '#The game can start!' below
			
		if game_mode == "set": # Settings. May be adjusted with more possibilities as the program grows. I
		
			display_settings = False
			while True:
				users_setting = ""
				if display_settings:
					# Display current settings:
					print ("\n~ CURRENT SETTINGS ARE:")
					print ("\n AI difficulty level:\n    for player Red: %d\n    for player White: %d" %(diff_level[1], diff_level[2]))
					print (" a) Automatic move is %s" %on_off[auto_move])
					print (" b) Automatic replay is " + str(on_off[auto_replay]) + ar_delay )
					print (" c) The first move has: " + red_or_white[default_who_am_I])
					if "z" in settings_input:
						print (" z) Saving position for GUI is %s\n" %on_off[is_gui])
				display_settings = True
				
				# Get user's input:
				alert = "\n Please, enter new AI's level for red or white player. Examples: 'R2', 'W4'\n Or enter a corresponding letter to toggle automatic move, automatic replay, and saving position for GUI on/off.\n Or enter 'S' to save the settings.\n Or enter 'Q' to exit to main menu. -> "
				while users_setting not in settings_input: # Tuple with possible inputs, declared and initialised at the top of this document
					users_setting = input(alert).lower()
					alert = "\n Please, enter AI's difficulty level for Red or White player. For instance, R2 means that if AI plays for red, it will play on the level two. Likewise, W4 means that if AI plays for white, it will play on the fourth level.\n You can use any number for the level, including 0 (zero), when AI just makes random moves. The higher number, the longer it takes to make a move.\n\n Please, enter new AI's level for red or white player. Examples: 'R2', 'W4'\n Or enter a corresponding letter to toggle automatic move, automatic replay, first moving player, and saving position for GUI on/off.\n Or enter 'S' to save the settings.\n Or enter 'Q' to exit to main menu. -> "
					try:
						level = int(users_setting[1:])
					except ValueError:      # If not integer on second character or if string is shorter than two characters
						if users_setting == "q":
							break # break out of 'while users_setting...' loop
							
						if users_setting[0] == "r" or users_setting[0] == "w":
							alert = "\n Difficulty level must be a whole number (a number which is not a fraction).\n" + alert
							users_setting = ""
							continue #do loop
							
						if users_setting == "a":
							auto_move *= -1
							old_auto_move = auto_move
							print ("\n Automatic move was switched " + on_off[auto_move] + " successfully!")
							break # go to Settings menu
							
						if users_setting == "b":	
							auto_replay *= -1
							if auto_replay == 1:
								ar_delay = input(" Please, to set the speed of replay, enter number of seconds between moves (may be fractions). Or, hit enter to set it to one second. -> ")
								try:
									ar_delay = round(float(ar_delay),1)
									ar_delay = " and the delay between moves is set to seconds: " + str(ar_delay)
								except 	ValueError:
									ar_delay = " and the delay between moves is set to seconds: 1.0"
							else:
								ar_delay = ""
								
							old_auto_replay = auto_replay	
							print (" Automatic replay is now " + on_off[auto_replay] + ar_delay )	
							break # go to Settings menu
						
						if users_setting == "c":
							if default_who_am_I == 0:
								default_who_am_I = -1
							elif default_who_am_I == -1:
								default_who_am_I = 0
								
							default_who_am_I *= -1
							print ("\n The first move now has: " + red_or_white[default_who_am_I] + ".")
							break # go to Settings menu
							
						if users_setting == "z":
							is_gui *= -1
							print ("\n Saving the position for GUI is now " + on_off[is_gui] + "!")
							break # go to Settings menu
							
						if users_setting == "s":
							to_save = "# Please, read README.md carefully before editing!\nauto_move = " + str(auto_move) + "\nauto_replay = " + str(auto_replay)
							if ar_delay:
								to_save += "\nar_delay = " + ar_delay[-3:]
							else:
								to_save += "\nar_delay = 0.0"
								
							to_save += "\nis_gui = " + str(is_gui) + "\ndiff_level = " + str(diff_level) + "\ndefault_who_am_I = " + str(default_who_am_I) + "\ndefault_main_position = " + str(default_main_position)
							with open(main_path + "/pd_config.py", mode='w', encoding='utf-8') as my_file:
								my_file.write(to_save)
								
							print ("\n Current settings were saved to pd_config.py successfully!\n")
							break # go to Settings menu
							
						alert = "\n It seems like the input was not valid. Please, try again." + alert  # entered something else
						continue #do loop
					
					# Sets a level of player:
					if level < 0:
						alert = "\n Difficulty level must be a positive number or zero." + alert
						users_setting = " "
						continue #do loop
					if users_setting[0] == "r":
						diff_level[1] = level
						alert = " Please, enter new AI's level for red or white player. Examples: 'R2', 'W4'\nOr, enter a corresponding number to toggle automatic move, automatic replay, first moving player, and saving position for GUI on/off.\nOr enter'Q' to exit to main menu 	-> "
						print ("\n AI difficulty level for player Red is now set to %d." %level)
						print ("\n AI difficulty level for player White is set to %d." %diff_level[2])
						break #go to Settings menu
					elif users_setting[0] == "w":
						alert = " Please, enter new AI's level for red or white player. Examples: 'R2', 'W4'\nOr, enter a corresponding number to toggle automatic move, automatic replay, first moving player, and saving position for GUI on/off.\nOr enter'Q' to exit to main menu 	-> "
						diff_level[2] = level
						print ("\n AI difficulty level for player White is now set to %d." %level)
						print ("\n AI difficulty level for player Red is set to %d." %diff_level[1])
						break #go to Settings menu
					else: # mismatch
						alert = "\n Please, specify which players difficulty level is to be updated entering 'w' or 'r' before the number.\n" + alert
						continue #do loop
				if users_setting == "q":
					break #out of while True loop	
			if users_setting == "q":
				continue #present main menu again
				
		if game_mode == "s": 	
			save_game()					
			continue #present main menu again
			
		if game_mode == "l":  #load game from a file
			# find available files
			available_files = []
			i = 0
			indent = "  "
			try:
				for file in os.listdir(main_path + "/myGames"):
					if file.endswith(".pdh"):
						available_files += [os.path.join(file)]
						i += 1
						print (indent + "%d.  %s" %(i, os.path.join(file)))
						if i > 9:
							indent = " "
							if i > 99:
								indent = ""
			except FileNotFoundError:
				pass  # the next condition will be True
					
			if i < 1:
				print ("\n You do not have any saved games in directory myGames.\n")
				continue #present main menu again
			
			# get the user's choice:
			alert = " Please, choose the file to load entering its corresponding number, or enter 'Q' to return to Main Menu without loading. -> "
			chosen_file = 0
			while chosen_file < 1 or chosen_file > i:
				chosen_file = input(alert).lower()
				alert = (" Please, to select your choice use a whole number between 1 and %d, or enter 'Q' to return to Main Menu without loading. Try again." %(i))
				if chosen_file == "q":
					break
					
				try:
					chosen_file = int(chosen_file)
				except ValueError:
					continue #do loop
			
			if chosen_file == "q":
				continue #present main menu again
				
			chosen_file -= 1
			try:
				with open(main_path + "/myGames/" + available_files[chosen_file], encoding='utf-8') as my_file:		
					game_history_string = my_file.read()	
			except OSError: # previously found file is missing... Well, testers think about every possibility :)
				print("\n Something went wrong. Probably, the file was deleted, renamed or moved from its location. Please, try again. If the problem persists, try to restart Python console.\n")	
				continue #present main menu again
			
			game_history = game_history_string.split(";")[:-1]  # the last delimiter creates an empty sub-list in game_history, so it is removed
			if len(game_history) < 3:
				print ("\n It seems like the only record in the specified file was the first move of the game. If you tried to load backup.pdh, please try to load backup_previous.pdh")
				continue #present main menu again
					
			# feed redo_stack like on 'Replay' for loaded game to be replayed
			redo_stack = list(game_history[1:])
			redo_stack.reverse()
			game_mode = "pp"	
			old_who_am_I = int(game_history[0])
			print ("\n The game was loaded successfully. Please, use Redo option to replay it.\n")
			# continues at '#The game can start!' below

	# End of user's input processing. If no condition above evaluated to True or 'Replay' od 'Load' was chosen, then..	
	# ..The game can start! 
		#set the beginning of the game:
		if not redo_stack:
			who_am_I = default_who_am_I					# from pd_config or changed in settings
			if who_am_I == 0:
				who_am_I = random.choice((-1, 1))
				
			old_who_am_I = who_am_I # for 'Undo', 'Redo', 'Replay'
			old_auto_move = auto_move
			old_auto_replay = auto_replay
		else:
			who_am_I = old_who_am_I
			
		game_mode = game_mode[1] + "L" + game_mode[0]	 # reversed users input! + limbo.
		main_position = [list(default_main_position[0]), list(default_main_position[1]), list(default_main_position[2])]		 # from pd_config
		game_history = [str(who_am_I)]
		move_count = 1
		will_draw = 0
		
		# move backup.pdh to backup_previous.pdh
		while True:
			try:
				os.rename("myGames/backup.pdh", "myGames/backup_previous.pdh") # to preserve what was in backup before start of a new game
			except FileExistsError:
				os.remove("myGames/backup_previous.pdh")
				#do loop
			except FileNotFoundError:
				break
		
		# initialise backup.pdh
		with open(main_path + "/myGames/backup.pdh", mode='w', encoding='utf-8') as my_file:
			my_file.write(game_history[0]+";") # initialise backup file
		
		# Be nice:
		if game_mode[0] == "a":
			print ("\n Hi. AI plays for whites at the level %d. The first move is yours!" %diff_level[2])
		if game_mode[2] == "a":
			print ("\n Hi. AI plays for reds at the level %d." %diff_level[1])
			
		print("\n Enjoy your game and good luck! :)")
		
		# the game starts:
		while True:
			print ("\n\n\n Move number %d. %s plays." %((int(move_count/2 + .5)), red_or_white[who_am_I]))
			if game_mode[who_am_I + 1] == "a": 	# if AI's move:
				move_began_time = time.time()
				who_am_I *= -1
				draw_board()
				who_am_I *= -1
				the_move = get_ais_move()
				if the_move == "tied":
					the_move = "quit"
					print ("\n The game was tied by the 'fourty moves' rule.\n\n")
					break # go to '#continue?' below
				if the_move:
					main_position = update_main_position(the_move, who_am_I, main_position)
					game_history.append("".join((str(item + 2) for item in main_position[1] if item != 3)))
					with open(main_path + "/myGames/backup.pdh", mode='a', encoding='utf-8') as my_file:
						my_file.write(game_history[-1] + ";")
					print("\n %s at the difficulty level %d played %s." %(red_or_white[who_am_I],diff_level[who_am_I], translate(the_move)))
					print(" It took %f seconds." %round(time.time() - move_began_time, 2))
					who_am_I *= -1
				else:
					print ("\n %s wins!!\n\n" %red_or_white[who_am_I*-1])
					break # game ended, go to main menu
			else:
				while True:
					draw_board()
					the_move = get_humans_move()
					if the_move == "quit":
						break # go to '#continue?' below
					if the_move == "continue":
						continue #do loop
					if the_move == "tied":
						the_move = "quit"
						print ("\n The game was tied.\n\n")
						break # go to '#continue?' below
					if the_move: 
						main_position = update_main_position(the_move, who_am_I, main_position)
						game_history.append("".join((str(item + 2) for item in main_position[1] if item != 3)))
						with open(main_path + "/myGames/backup.pdh", mode='a', encoding='utf-8') as my_file:
							my_file.write(game_history[-1] + ";")
						who_am_I *= -1
						redo_stack = []						 # Redo stack is flushed as soon as a move is made
						auto_replay = old_auto_replay 		 # Goes back on if it was switched off on 'Undo'
						auto_move = old_auto_move 			 # Goes back on if it was switched off on 'Undo'
						break # go to '#continue?' below 
					else:
						print ("\n %s wins!!\n\n" %red_or_white[who_am_I*-1])
						break # go to '#continue?' below
				
				#continue?
				if the_move == "quit" or not the_move:
					break # game ended, go to main menu
					
			move_count +=1 # End of one move
		# do loop for the next move 

except Exception as e:
	if str(e) != "pd_end_by_user":
		x = input("\n\n Something went terribly wrong!\n An exception '" + str(e) + "' occured.\n It is most likely caused by incorrent installation. Please, refer to README.md to troubleshoot.\n  If in shell, enter 'r' to raise the exception. Or any key to terminate now.")
		if x == "r":
			raise
	else:
		print (" Goodbye!")