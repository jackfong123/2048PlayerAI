from BaseAI_3 import BaseAI
from random import randint
import math

INFINITY = 100000000000
class PlayerAI(BaseAI):
	def __init__(self, maxdepth=2):
		self.maxdepth = maxdepth
		self.curstep = 0

	def getMove(self, grid):
		self.curstep += 1
		bestMoves = [-1]*5
		index = -1
		availableMoves = grid.getAvailableMoves()
		bestValue = -INFINITY
		for x in availableMoves:
			gridCopy = grid.clone()
			gridCopy.move(x)
			value = self.min_(gridCopy, self.maxdepth, -INFINITY, INFINITY)
			if x == 0 or x == 2:
				value += 10000
			if value > bestValue:
				bestValue = value
				index = 0
				bestMoves[index] = x
			
			elif value == bestValue:
				index += 1
				bestMoves[index] = x

		if index == -1:
			return -1
		if index >= 1:
			index = randint(0, index) #check	 
		return bestMoves[index]

	def max_(self, grid, depth, alpha, beta):
		evalValue = self.heuristic(grid)
		if beta <= alpha or depth == 0:
			return evalValue
		bestValue = -INFINITY
		#availableMoves = grid.getAvailableMoves()
		#if not availableMoves:
		#	return evalValue
		flag = False
		if self.curstep < 1000:
			for x in range(4):
				gridCopy = grid.clone()
				if gridCopy.move(x):
					flag = True
					bestValue = max(bestValue, self.min_(gridCopy, depth-1, max(bestValue,alpha), beta))
					if bestValue >= beta:
						return bestValue
		else:
			avgValue = 0
			cnt = 0
			for x in range(4):
				gridCopy = grid.clone()
				if gridCopy.move(x):
					flag = True
					minValue = self.min_(gridCopy, depth-1, max(bestValue,alpha), beta)
					bestValue = max(bestValue, minValue)
					avgValue += minValue
					cnt += 1
			if cnt != 0:
				avgValue /= cnt
				bestValue = avgValue
		if not flag:
			return evalValue
		return bestValue

	def min_(self, grid, depth, alpha, beta):
		evalValue = self.heuristic(grid)
		if beta <= alpha or depth == 0:   #number adj,avgchild,heucut
			return evalValue
		bestValue = INFINITY
		cells = grid.getAvailableCells()
		if len(cells) == 0:
			return evalValue
		if self.curstep < 1000:
			gridCopy = grid.clone()
			for move in cells:
				gridCopy.setCellValue(move, 2)
				bestValue = min(bestValue, self.max_(gridCopy, depth-1, alpha, min(bestValue,beta)))
				if bestValue <= alpha:
					return bestValue
				gridCopy.setCellValue(move, 4)
				bestValue = min(bestValue, self.max_(gridCopy, depth-1, alpha, min(bestValue,beta)))
				if bestValue <= alpha:
					return bestValue
				gridCopy.setCellValue(move, 0)
		else:
			avgValue = 0
			gridCopy = grid.clone()
			for move in cells:
				gridCopy.setCellValue(move, 2)
				maxValue = self.max_(gridCopy, depth-1, alpha, min(bestValue,beta))
				bestValue = min(bestValue, maxValue)
				avgValue += maxValue
				gridCopy.setCellValue(move, 4)
				maxValue = self.max_(gridCopy, depth-1, alpha, min(bestValue,beta))
				bestValue = min(bestValue, maxValue)
				avgValue += maxValue
				gridCopy.setCellValue(move, 0)
			avgValue /= len(cells)*2
			bestValue = avgValue
		return bestValue

	def heuristic(self, grid):
		emptyTiles = 0
		maxTile = 0
		gridlist = []
		for i in range(grid.size):
			for j in range(grid.size):
				tmp = grid.getCellValue((i,j))
				gridlist.append(tmp)
				if tmp == 0:
					emptyTiles += 1
				if tmp > maxTile:
					maxTile = tmp
		Ord = 0
		weights = [65536,32768,16384,8192,512,1024,2048,4096,256,128,64,32,2,4,8,16]
		#weights = [65536,32768,16384,8192,4096,2048,1024,512,256,128,64,32,16,8,4,2]
		if maxTile == gridlist[0]:
			Ord += (math.log(gridlist[0])/math.log(2))*weights[0]
		for i in range(16):
			if gridlist[i] >= 8:
				Ord += weights[i]*(math.log(gridlist[i])/math.log(2))
		return Ord/(16-emptyTiles)
