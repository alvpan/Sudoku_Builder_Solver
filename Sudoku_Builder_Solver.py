import pprint
import numpy as np
import random
from collections import deque, Counter
import math
from itertools import chain
from tabulate import tabulate, SEPARATING_LINE #seperateline might be useful next on visualization

def CreateEmptyMatrix(sides):					#empty matrix (of zeros)
	d = int(sides/3) 
	block_matrix = [[[0 for i in range(d)] for i in range(d)] for i in range(sides)]
	return(block_matrix)

def CreateBlock(d):								#block creator (dxd)
	block = [d*[0] for i in range(d)]
	squared = int(d*d)
	numbers = [0]*squared
	for i in range(squared):
		numbers[i] = i+1
	rndm = random.sample(numbers,squared)
	counter = 0
	for i in range(d):
		for j in range(d):
			block[i][j] = rndm[counter]
			counter +=1
	return(block)

def LineRotator(block, step):
	lines = [[0 for i in range(len(block))] for i in range(len(block))]
	block = list(block)
	for i in range(len(block)):
		lines[i] = deque(block[i])
		lines[i].rotate(step)
		lines[i] = list(lines[i])
		block[i] = lines[i]
	return(block)

def RowsRotator(block, step):
	block = deque(block)
	block.rotate(step)
	block = list(block)
	return(block)

def CreateFullMatrix(sides):
	if(sides>0):
		matrix = CreateEmptyMatrix(sides)
		block = CreateBlock(sides)
		for i in range(sides):
			block = LineRotator(block,step=1)
			matrix[i] = block
			for j in range(sides):
				block = RowsRotator(block,step=1)
				matrix[i][j] = block
		matrix = list(chain.from_iterable(matrix))
		for i in range(len(matrix)):
			matrix[i]= list(chain.from_iterable(matrix[i]))
		return(matrix)

def Scramble_3_Rows(matrix,start):     					#ROOOOWWWSSSS
	pattern = []
	start = int(start)
	third = int(len(matrix)/3)	
	numbers = [0 for i in range(start,start+third)]
	for p in range(0,third):							#pattern
		numbers[p] = p + start
	pattern = random.sample(numbers,third)								
	new_matrix = CreateEmptyMatrix(len(matrix)) 		#copy to new matrix in differtent order
	for a in range(len(pattern)):
		copy = matrix[pattern[a]]
		new_matrix[a] = copy		
	return(new_matrix[0:3])   							#return the first 3 rows

def Scramble_3_Cols(matrix,start):						#COLLLLLSSSS   				
	pattern = []
	third = int(len(matrix)/3)	
	start = int(start)
	numbers = [0 for i in range(start,start+third)]
	for p in range(0,third):							#pattern
		numbers[p] = p + start
	pattern = random.sample(numbers,third)								
	new_matrix = CreateEmptyMatrix(len(matrix)) 		#copy to new matrix in differtent order
	for a in range(len(pattern)):
		col = [val[pattern[a]] for val in matrix]
		for row_b, row_a in zip(new_matrix, matrix):	#SOME GOOFY SHIET HERE 
			row_b[a] = row_a[pattern[a]]				
	return(new_matrix)									#return the 3 columns from start->start+third

matrix = CreateFullMatrix(3)
new_matrix = CreateEmptyMatrix(9)

for i in range(0,9,3):									#use rows scrambler	(NEEDS IMPROVEMENT) (integrate with col scrambler in s single function)
	new_matrix[i:i+3] = Scramble_3_Rows(matrix,i)							
for i in range(0,6,3):									#use cols scrambler (NEEDS IMPROVEMENT)
	if(i==3):
		cols_next = np.array(Scramble_3_Cols(new_matrix,i+3))
		final_matrix = np.concatenate((final_matrix,cols_next),axis=1)
	else:
		cols_here = np.array(Scramble_3_Cols(new_matrix,i))
		cols_next = np.array(Scramble_3_Cols(new_matrix,i+3))
		final_matrix = np.concatenate((cols_here,cols_next),axis=1)

complete_matrix = final_matrix.tolist()		#full matrix
complete_matrix_copy = complete_matrix




#//////////////////////////////////////////////////
#//////////////////////////////////////////////////
#//////////////////////////////////////////////////
#//////////////////////////////////////////////////
#//////////////////////////////////////////////////
#//////////////////////////////////////////////////
#//////////////////////////////////////////////////
#/////////////////BUILDER END/////////////////////
#//////////////SOLVER BEGINNING//////////////////
#//////////////////////////////////////////////
#//////////////////////////////////////////////////
#//////////////////////////////////////////////////
#//////////////////////////////////////////////////
#//////////////////////////////////////////////////
#//////////////////////////////////////////////////
#//////////////////////////////////////////////////



def GetBlock(matrix,a,b):						#RETURNS(list) the unique numbers in the block [a][b] is in
	third = int(len(matrix)/3)
	a = int(a)
	b = int(b)
	if(a<third):								#find previous mulriple  of third for A (NEEDS IMPROVEMENT)
		a_beg = 0
	elif(a<third*2):
		a_beg = 3
	elif(a<third*3):
		a_beg = 6
	if(b<third):								#find previous mulriple  of third for A (NEEDS IMPROVEMENT)
		b_beg = 0
	elif(b<third*2):
		b_beg = 3
	elif(b<third*3):
		b_beg = 6
	k = 0
	block = [' ' for i in range(third*third)]
	for i in range(a_beg,a_beg+third):			#get everything in the 3x3 block starting from [a_beg][b_beg]
		for j in range(b_beg,b_beg+third):
			block[k] = matrix[i][j]
			k = k+1
	block = list(Counter(block).keys())			#get unique numbers only 
	if' 'in block:								#remove the ' '
		block.remove(' ')
	return(block)

def GetCross(matrix,a,b):						#RETURNS(list) the unicue numbers in a cross
	cross = matrix[a] + [r[b] for r in matrix]	#row + column
	cross = list(Counter(cross).keys())			#get all unique numbers once
	if' 'in cross:								#remove the ' '
		cross.remove(' ')
	return(cross)				

def PossibleNumbers_1D(matrix,a,b):					#RETURNS(1d matrix) possible numbers in this square
	block = GetBlock(matrix,a,b)
	cross = GetCross(matrix,a,b)
	existing = list(Counter(block+cross).keys())	#merge these 2 and get the unique numbers only
	numbers = [i+1 for i in range(len(matrix))]
	possible_1d = []
	for i in range(len(numbers)):
		if numbers[i] not in existing:
			possible_1d.append(numbers[i])
	return(possible_1d)

def PossibleNumbers_2D(matrix):						#RETURNS(2d matrix of matrixes) possible numbers in each square of the board
	possible_2d = [[[]*len(matrix) for i in range(len(matrix))] for i in range(len(matrix))]
	for i in range(len(matrix)):
		for j in range(len(matrix)):
			if(matrix[i][j]==' '):
				possible_2d[i][j] = PossibleNumbers_1D(matrix,i,j)	
	return(possible_2d)

recorder = []															#recorder (each move has: order, i_position, j_position, numberPut)
order = 0																#order (not sure if needed bc order = i in recorder[i])
#need to run this in a loop before every other loop
def FillOnlyOnesLeft(matrix,recorder,order):							#RETURNS(nothing) Fills all the empty squares with the only one possible number left.
	print("OnlyOnesLeft results:")	
	change = 0	
	copy = matrix			
	for i in range(len(copy)):										#Visit the whole matrix to check if any len(possible_1d)==1. If so, put the bumber in and record it.
		for j in range(len(copy)):
			possible_2d = PossibleNumbers_2D(copy)
			if(possible_2d[i][j]!=[]):									#if there are any possible numbers for this square
				if(len(possible_2d[i][j])==1):							#if there is only one possible number for this block
					copy[i][j] = possible_2d[i][j][0]					#put the only possible number in the block
					recorder.append([order,i,j,possible_2d[i][j][0]])	#fill in new recorder list
					order+=1					
					print("put number: ", possible_2d[i][j][0],"in position: ", i, j,"   order: ", order)				
					possible_2d = PossibleNumbers_2D(copy)
					change = 1
	if(change==0): 
		print(" N O T H I N G   L E F T   T O   F I L L   I N!!!!!!")
		return(copy,0)
	else:
		print('continuing OnlyOnesLeft')
		return(copy,1)	#remove number put from possible_2d by updating possible_2d (both actions are needed)
#/////////////////////////////////////////////////////////////////////////////////////////////////////

#!!! WARNING !!!!! NOT WORKING PROPERLY 
def LooksGood(matrix):
	for i in range(len(matrix)):
		for j in range(len(matrix)):
			if(not str(matrix[i][j]).isnumeric()): 
				return(False)
	return(True)

def Solver(matrix, max_tries, counter):
	solvable = False
	matrix_before = matrix
	copy = matrix
	
	if(counter==0):
		first_matrix = matrix

	if max_tries == 0:
		print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
		return copy, False
	
	for i in range(len(copy)):
		for j in range(len(copy)):
			if copy[i][j] == ' ':
				possible_numbers = PossibleNumbers_2D(copy)
				if i < len(possible_numbers) and j < len(possible_numbers[i]) and len(possible_numbers[i][j]) > 0:
					for n in range(len(possible_numbers[i][j])):
						copy[i][j] = possible_numbers[i][j][n]
						print(tabulate(copy, tablefmt='simple_grid'))
						while FillOnlyOnesLeft(copy, recorder, order)[1] == 1:
							FillOnlyOnesLeft(copy, recorder, order) 
						Solver(copy, max_tries=max_tries-1, counter=counter+1)
						if LooksGood(copy):
							print("/////////////////////////////////////////////////////////////// ")
							solvable = True
							return first_matrix, solvable
						else:
							copy[i][j] = ' '
							copy = matrix_before
							PossibleNumbers_2D(copy)
				
#//BULDER EMBED /////////////////////////////////////////////////////////////////////
def DelRotPair(matrix,core_pairs,counter):				#RETURNS(matrix_after ,last pair deleted)
	#check if this is the first loop
	if(counter==0):
		copy = matrix
	last_pair = []
	while(core_pairs>0):
		i = random.randint(0,4)					#pick a random int from 0-4, from 0-9 (first 4 rows)
		j = random.randint(0,8)
		while(copy[i][j]==' '):					#if square is already deleted as pair pick another one
			i = random.randint(0,4)				
			j = random.randint(0,8)
		copy[i][j] = ' '
		copy[len(copy)-1-i][len(copy)-1-j] = ' '
		print("Rotational Pair of: ", i, j, "is: ", len(copy)-i, len(copy)-j)
		print(tabulate(copy, tablefmt='simple_grid'))#TESTINNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
		last_pair = [[i,j], [len(copy)-1-i,len(copy)-1-j]] 
		core_pairs-=1
		counter+=1

	print('delrotpair before:')
	print(tabulate(complete_matrix, tablefmt='simple_grid'))
	print('delrotpair after:')
	print(tabulate(copy, tablefmt='simple_grid'))

	return(copy,last_pair) 						#return latest_pair also so i can call DelRotPair for only 1 pair!

#del and check needs to return if it is ok to delete this pair (taken from DelRotPair) 
#and if its ok, return also the matrix with this pair mssing (code taken from delrotpair but for specific pair)
def DeleteAndCheckOnce(matrix):
	copy = matrix
	copy_after = DelRotPair(copy,1,0)
	copy_after_copy = copy_after[0]
	pair_deleted = copy_after[1]
	if(Solver(copy_after[0],max_tries=10,counter=0)[1]==True):	#max tries of THIS solver
		print("Delete Succeded!")
		return(copy_after_copy,True,pair_deleted)
	else:
		print("Delete Failed!")
		return(copy,False,pair_deleted)

#////END BULDER EMBED///////////////////////////////////////////////////////////////////






#DRIVER

sudoku = (DelRotPair(complete_matrix_copy,15,0))[0]	#how many core pairs
basic_sudoku = sudoku

#add sth here
extra_sudoku = DeleteAndCheckOnce(basic_sudoku)[0]


print("Sudoku after Deleting")
print(tabulate(extra_sudoku, tablefmt='simple_grid'))		#print sudoku(clues only) as simple_grid

#final = (Solver(sudoku,max_tries=20))[0]			#max tries of FINAL Solver
#print("solution")
#print(tabulate(final, tablefmt='simple_grid'))

# #in a later time after the rest is mostly stable
# def BuildSudoku():
# 	#-
# 	return(matrix)

# def SolveSudoku(matrix):
# 	#-
# 	return(solution)





#to provlima einai sto solver kai sto oti peirazei katefthian ton pinaka eno tha eprepe na 
#tsekarei an einai epilysimos kai na gyrnaei ton idio pinaka pou pire san input