def get_mans_leaps(start): #see documentation for get_possible_moves()
		
	up_right = position[start+4] < 0 and position[start+8] == 0
	up_left = position[start+5] < 0 and position[start+10] == 0
	is_node = False
	
	if up_right:
		is_node = True
		to_append = list(leaps[-1])
		leaps[-1].extend([start-5, start-1])
		get_mans_leaps(start+8)
	if up_left:
		if is_node:leaps.append(to_append)
		leaps[-1].extend([start-4, start+1])
		get_mans_leaps(start+10)
		
	#false in both = base case
	return
	
def get_mans_jumps(start): #see documentation for get_possible_moves()
	global leaps
	leaps = [[start-9]]
	get_mans_leaps(start)
		
	return leaps
	
def get_kings_leaps(start, position): #see documentation for get_possible_moves()
		
	up_right = position[start+4] < 0 and position[start+8] == 0
	up_left = position[start+5] < 0 and position[start+10] == 0
	down_left = position[start-4] < 0 and position[start-8] == 0
	down_right = position[start-5] < 0 and position[start-10] == 0
	is_node = False
	
	if up_right:
		is_node = True
		to_append = list(leaps[-1])
		new_position = list(position)
		new_position[start+4] = 0
		leaps[-1].extend([start-5, start-1])
		get_kings_leaps(start+8, new_position)
		
	if up_left:
		if is_node:leaps.append(to_append)
		is_node = True
		to_append = list(leaps[-1])
		new_position = list(position)
		new_position[start+5] = 0
		leaps[-1].extend([start-4, start+1])
		get_kings_leaps(start+10, new_position)
		
	if down_left:
		if is_node:leaps.append(to_append)
		is_node = True
		to_append = list(leaps[-1])
		new_position = list(position)
		new_position[start-4] = 0
		leaps[-1].extend([start-13, start-17])
		get_kings_leaps(start-8, new_position)
	
	if down_right:
		if is_node:leaps.append(to_append)
		new_position = list(position)
		new_position[start-5] = 0
		leaps[-1].extend([start-14, start-19])
		get_kings_leaps(start-10, new_position)
	
	#false in all four = base case
	return

def get_kings_jumps(start): #see documentation for get_possible_moves()
	global leaps
	
	leaps = [[start-9]]
	new_position = list(position)
	new_position[start] = 0
	get_kings_leaps(start, new_position)

	# remove duplicates
	new_leaps = []
	for item in leaps:
		if reversed(item) not in new_leaps:
			new_leaps.append(item)
	
	return new_leaps
	
def get_possible_moves(position_): #see documentation
	global position
	position = [3,3,3,3,3,3,3,3,3] + position_ + [3,3,3,3,3,3,3,3,3,3]
	
	possible_moves = []
	is_jump = False
	
	for start in range(44,9, -1):  
		piece = position[start]
		if piece <= 0 or piece == 3:
			continue
				
		if not is_jump:
			if position[start+4] < 0 and position[start+8] == 0:
				possible_moves = []
				is_jump = True
			else:
				if position[start+4] == 0:
					possible_moves.append([start-9, start-5])
				if position[start+5] < 0 and position[start+10] == 0:
					possible_moves = []
					is_jump = True
				else:
					if position[start+5] == 0:
						possible_moves.append([start-9, start-4])
					if piece == 2:
						if position[start-4] < 0 and position[start-8] == 0:
							possible_moves = []
							is_jump = True
						else:
							if position[start-4] == 0:
								possible_moves.append([start-9, start-13])
							if position[start-5] < 0 and position[start-10] == 0:
								possible_moves = []
								is_jump = True
							elif position[start-5] == 0:
									possible_moves.append([start-9, start-14])
						  
		if is_jump:
			if piece == 1:
				possible_jumps = get_mans_jumps(start)
			else:
				possible_jumps = get_kings_jumps(start)
			
			if possible_jumps != [[start-9]]:
				possible_moves.extend(possible_jumps)
				
	
	# next start
	
	return possible_moves

def update_main_position(the_move, who_am_I, main_position):
	who_are_you = who_am_I * -1
	main_position[0][0] += 1
	main_position[0][2] = 0
	main_position[0][3] = 0
	
	if the_move[-1] > 31: # promoted?
		if main_position[who_am_I][the_move[0]] == 1: # yes, promoted!
			main_position[0][2] = 1 # 1 when promoted (used for ai's logic in my_spider())
		
		main_position[who_am_I][the_move[0]] = 2 #to ensure 2 is assigned to the end square in the following 2 lines after this block
		main_position[who_are_you][36 - the_move[0]] = -2 #to ensure -2 is assigned to the end square in the following 2 lines after this block
	
	main_position[who_am_I][the_move[-1]] = main_position[who_am_I][the_move[0]] # assign value of start square to the end square (may be 1 or 2)
	main_position[who_are_you][36 - the_move[-1]] = main_position[who_are_you][36-the_move[0]] # assign value of start square to the end square (may be -1 or -2)
	
	if the_move[0] != the_move[-1]: # condition for the case when a king lands on the same square after multi jump
		main_position[who_am_I][the_move[0]] = 0 #start square is assigned with 0 = empty
		main_position[who_are_you][36 - the_move[0]] = 0 #start square is assigned with 0 = empty
		
	for i in range(1, len(the_move)-1, 2): # does not happen if no captures occured
		main_position[0][0] = 0 		# capture occured: erase
		main_position[0][3] += abs(main_position[who_am_I][the_move[i]] + 1) # adds 1 for each captured opponent's king
		main_position[who_am_I][the_move[i]] = 0 #erase squares with captured pieces
		main_position[who_are_you][36 - the_move[i]] = 0 #erase squares with captured pieces
		main_position[0][who_are_you] -= 1 # decreases the number of opponent's pieces on the board
		
	return main_position