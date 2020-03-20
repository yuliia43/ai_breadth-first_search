class State:
	rightbank = {}
	leftbank = {}
	boat = {}
	prev_state = None

	def __init__(self, leftbank = None,\
					 rightbank = None,\
					 boat = None):
		if leftbank == None:
			leftbank = {'pairs_num':0, 'males_num':0, 'females_num':0}
		if rightbank == None:
			rightbank = {'pairs_num':0, 'males_num':0, 'females_num':0}
		if boat == None:
			boat = {'males_num':0, 'females_num':0, 'position':None}
		self.rightbank = rightbank
		self.leftbank = leftbank
		self.boat = boat
		self.prev_state = None


	def __eq__(self, state):
		return self.__class__ == state.__class__ and \
				self.rightbank['pairs_num']==state.rightbank['pairs_num'] and \
				self.rightbank['males_num']==state.rightbank['males_num'] and \
				self.rightbank['females_num']==state.rightbank['females_num'] and \
				self.boat['males_num']==state.boat['males_num'] and \
				self.boat['females_num']==state.boat['females_num']


class TreeBuilder:
	num_of_pairs = 0
	existing_states = []
	first_state = None
	final_state = None

	def __init__(self, num_of_pairs, first_state, final_state, boat_position = None):
		self.num_of_pairs = num_of_pairs
		self.first_state = first_state
		if boat_position == None and first_state.boat['position']==None:
			boat_position = 'left'
		self.first_state.boat['position'] = boat_position
		self.final_state = final_state

	def get_all_states(self):          #fills the array of all correct states
		num_of_pairs = self.num_of_pairs
		for pairs in range(num_of_pairs+1):
			pairs_num=num_of_pairs-pairs
			for male_quantity in range(pairs+1):
				males_num = male_quantity
				females_num = 0
				if pairs == num_of_pairs and males_num == 0:
					for female_quantity in range(pairs+1):
						females_num = female_quantity
						leftbank = {'pairs_num':pairs_num, 'males_num':males_num, 'females_num':females_num}
						self.add_boat_passengers_and_fill_states(leftbank)
				else:
					leftbank = {'pairs_num':pairs_num, 'males_num':males_num, 'females_num':females_num}
					self.add_boat_passengers_and_fill_states(leftbank)

	def add_boat_passengers_and_fill_states(self, leftbank):   #fill boat vocabulary and create state
		if(leftbank['pairs_num']!=self.num_of_pairs):
			for male_quantity in range(3):
				for female_quantity in range(3-male_quantity):
					state_to_add = State()
					state_to_add.leftbank = leftbank
					state_to_add.boat['males_num'] = male_quantity
					state_to_add.boat['females_num'] = female_quantity
					state_to_add = self.form_state_if_possible(state_to_add)
					if state_to_add != None:         #if state can exist
						self.existing_states.append(state_to_add)
		else:
			state_to_add = State()
			state_to_add.leftbank = leftbank
			state_to_add = self.form_state_if_possible(state_to_add)
			if state_to_add != None:         #if state can exist
				self.existing_states.append(state_to_add)



	def form_state_if_possible(self, state_to_add):   #adds right bank state and checks if state could exist
		males = self.get_males(state_to_add.leftbank, state_to_add.boat)
		females = self.get_females(state_to_add.leftbank, state_to_add.boat)
		if  max(males, females) > self.num_of_pairs\
			or (females < males and males!=self.num_of_pairs):  #that means that on the left bank would be female without her male
			return None
		else:
			self.set_bank(state_to_add.rightbank, males, females)
			return state_to_add

	def set_bank(self, bank, males, females):     #fills persons on the bank due to the number of filled persons
		if(females>males):
			bank['pairs_num'] = self.num_of_pairs-females
			bank['males_num'] = females-males
			bank['females_num'] = 0
		else:
			bank['pairs_num'] = self.num_of_pairs-males
			bank['females_num'] = males-females
			bank['males_num'] = 0

	def get_males(self, bank, boat = None):   #gets males on bank and boat (unless it`s unset)
		quantity = bank['pairs_num']+\
			bank['males_num']
		if boat != None:
			quantity = quantity + boat['males_num']
		return quantity

	def get_females(self, bank, boat = None):  #gets males on bank and boat (unless it`s unset)
		quantity = bank['pairs_num']+\
			bank['females_num']
		if boat != None:
			quantity = quantity + boat['females_num']
		return quantity

	def is_final_state(self, state):     
		return self.final_state == state

	def breadth_first_search(self):        #algorithm realization
		self.get_all_states()
		#finds first state in existing states array and mark it as first state
		self.existing_states[self.existing_states.index(self.first_state)].prev_state = "first" 
		states = [self.first_state]
		while (states != None):
			for state in states:
				new_states = self.iteration(state)
				if new_states == None:
					states = None
					break
				for new_state in new_states:
					states.append(new_state)

	def iteration(self, state):
		if not self.is_final_state(state):
			states = self.find_next_states(state)
			return states
		else:
			return None


	def find_next_states(self, state):
		states = []
		current_bank = ''
		next_bank = ''
		new_position = ''
		position = state.boat['position']
		if position == 'left':
			current_bank = state.leftbank
			next_bank = state.rightbank
			new_position = 'right'
		else:
			current_bank = state.rightbank
			next_bank = state.leftbank
			new_position = 'left'
		males = self.get_males(current_bank, state.boat)
		females = self.get_females(current_bank, state.boat)
		males_opposite = self.get_males(next_bank)
		females_opposite = self.get_females(next_bank)
		for male_quantity in range(min(3, males+1)):
			for female_quantity in range(min(3-male_quantity, females+1)):
				self.create_new_state_and_append_to_list(state, position, new_position, next_bank,\
					male_quantity, female_quantity, males_opposite, females_opposite, states)
		return states

	def create_new_state_and_append_to_list(self, state, previous_position, new_position, next_bank,\
					 male_quantity, female_quantity, males_opposite, females_opposite, states):
		new_state = State()
		new_state_current_bank = None
		new_state_opposite_bank = None
		new_state_current_bank = next_bank
		if previous_position == 'left':
			new_state.rightbank = new_state_current_bank
			new_state_opposite_bank = new_state.leftbank
		else:
			new_state.leftbank = new_state_current_bank
			new_state_opposite_bank = new_state.rightbank
		new_state.boat['males_num']=male_quantity
		new_state.boat['females_num']=female_quantity
		if male_quantity+female_quantity != 0:         #if boat is empty, its position will not be changed
			new_state.boat['position']=new_position
		else:
			new_state.boat['position']=previous_position	
		self.set_bank(new_state_opposite_bank, males_opposite+male_quantity, females_opposite+female_quantity)
		if self.state_is_unchecked(new_state):
			self.existing_states[self.existing_states.index(new_state)].prev_state = \
						self.existing_states[self.existing_states.index(state)]
			states.append(new_state)

	def state_is_unchecked(self, state):
		try:
			index = self.existing_states.index(state)
			return self.existing_states[index].prev_state==None
		except:         #if state is incorrect, it will not be in the array, so we should return 'False'
			return False

	
def get_state_string(state):    #returns formated string of states from first to final
	pairs_left = state.leftbank['pairs_num']
	males_left = state.leftbank['males_num']
	females_left = state.leftbank['females_num']
	males_boat = state.boat['males_num']
	females_boat = state.boat['females_num']
	pairs_right = state.rightbank['pairs_num']
	males_right = state.rightbank['males_num']
	females_right = state.rightbank['females_num']
	state_string = '| '+\
			('{:^20}'.format((('pairs: '+ str(pairs_left)) if pairs_left!=0 else '') +\
							((' males: '+ str(males_left)) if males_left!=0 else '') +\
							((' females: '+ str(females_left)) if females_left!=0 else ''))) + " | "+\
	 		('{:^20}'.format(((' males: '+ str(males_boat)) if males_boat!=0 else '') +\
	 						((' females: '+ str(females_boat)) if females_boat!=0 else ''))) + " | "+\
	 		('{:^20}'.format((('pairs: '+ str(pairs_right)) if pairs_right!=0 else '') + \
	 						((' males: '+ str(males_right)) if males_right!=0 else '') +\
	 						((' females: '+ str(females_right)) if females_right!=0 else '')))  +"|\n"	
	if state.prev_state != 'first' and state.prev_state != None:
		state_string = get_state_string(state.prev_state)+state_string
	return state_string


bank = {'pairs_num':3, 'males_num':0, 'females_num':0}
first_state = State(leftbank = bank)
final_state = State(rightbank = bank)
builder = TreeBuilder(3, first_state, final_state)
builder.breadth_first_search()
#final state object in existing states array
state = builder.existing_states[builder.existing_states.index(builder.final_state)] 
print get_state_string(state)
