import pygame
import random
import math
import queue

pygame.init()

class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BLUE = 0, 0, 255
	BACKGROUND_COLOR = WHITE

	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	SMALL_FONT = pygame.font.SysFont('comicsans', 21)
	FONT = pygame.font.SysFont('comicsans', 30)
	LARGE_FONT = pygame.font.SysFont('comicsans', 40)

	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualization")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2



def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	sorting = draw_info.SMALL_FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | M - Merge Sort | Q - Quick Sort | H - Heap Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 85))

	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val + 1) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst


def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst


def merge_sort(draw_info, ascending=True):

	lst = draw_info.lst
	width = 1    
	n = len(lst)                                          

	while (width < n):
        
		l=0
		while (l < n): 
			r = min(l+(width*2-1), n-1)
			m = min(l+width-1,n-1)
            
			n1 = m - l + 1
			n2 = r - m 
			L = [0] * n1 
			R = [0] * n2 
			ascending_num = 1 if ascending == True else -1

			for i in range(0, n1): 
				L[i] = lst[l + i] 
			for i in range(0, n2):
				R[i] = lst[m + i + 1] 
			i, j, k = 0, 0, l 

			ascending_num = 1 if ascending == True else -1
			while i < n1 and j < n2: 
				if L[i] * ascending_num <= R[j] * ascending_num: 
					lst[k] = L[i]
					draw_list(draw_info, {i + l : draw_info.GREEN, k: draw_info.RED, m: draw_info.BLUE}, True)
					yield True
					i += 1

				else:
					lst[k] = R[j]
					draw_list(draw_info, {j + m +1 : draw_info.GREEN, k: draw_info.RED, m: draw_info.BLUE}, True)
					yield True
					j += 1
				k += 1
			
			while i < n1:
				lst[k] = L[i]
				draw_list(draw_info, {i + l : draw_info.GREEN, k: draw_info.RED, m: draw_info.BLUE}, True)
				yield True
				i += 1
				k += 1

			while j < n2:
				lst[k] = R[j]
				draw_list(draw_info, {j + m + 1 : draw_info.GREEN, k: draw_info.RED, m: draw_info.BLUE}, True)
				yield True
				j += 1
				k += 1

			l += width*2

		width *= 2

	return lst


def quick_sort(draw_info, ascending=True):
	lst = draw_info.lst
	stack = [(0, len(lst)-1)]
	ascending_num = 1 if ascending == True else -1

	while len(stack) != 0:
		start, finish = stack.pop()
		pivot = lst[random.randint(start, finish)] 
		i, j = start, finish

		while i < j:
			while i < j and lst[i] * ascending_num <= pivot * ascending_num:
				i += 1

			while i < j and lst[j] * ascending_num > pivot * ascending_num:
				j -= 1
			
			if i < j and lst[i] * ascending_num > pivot * ascending_num and lst[j] * ascending_num <= pivot * ascending_num: 
				lst[i], lst[j] = lst[j], lst[i]
				draw_list(draw_info, {i : draw_info.GREEN, j: draw_info.RED}, True)
				i += 1
				j -= 1
				yield True

		while i <= finish and lst[i] * ascending_num <= pivot * ascending_num:
			i += 1
		
		if i-1 - start > 0 and [pivot for _ in range(start, finish+1)] != lst[start:finish+1]:
			stack.append((start, i-1))

		if finish - i > 0:
			stack.append((i, finish))

	return lst
			
def heap_sort(draw_info, ascending = True):
	ascending_num = 1 if ascending == True else -1
	lst = draw_info.lst
	queue_action = queue.Queue()
	finish = len(lst)

	for indx in range(finish//2, -1, -1):
		queue_action.put(indx)

	while not queue_action.empty():
		indx = queue_action.get()
		actual_value = lst[indx] * ascending_num
		colors = {indx : draw_info.GREEN}

		if 2*indx +1 < finish:
			right_son = lst[2*indx +1] * ascending_num
			colors[2*indx +1] = draw_info.BLUE
		else:
			right_son = None
		
		if 2*indx +2 < finish:
			left_son = lst[2*indx +2] * ascending_num 
			colors[2*indx +2] = draw_info.BLUE
		else:
			left_son = None
		
		draw_list(draw_info, colors, True)
		yield True

		if not left_son:
			left_son = actual_value
		if not right_son:
			right_son = actual_value
		
		if actual_value != max([left_son, right_son, actual_value]):

			if right_son > left_son:
				lst[indx], lst[2*indx +1] = lst[2*indx + 1], lst[indx]
				colors[2*indx +1] = draw_info.GREEN
				colors[indx] = draw_info.BLUE

				draw_list(draw_info, colors, True)
				yield True
				queue_action.put(2*indx +1)
			else:
				lst[indx], lst[2*indx +2] = lst[2*indx + 2], lst[indx]
				colors[2*indx +2] = draw_info.GREEN
				colors[indx] = draw_info.BLUE

				draw_list(draw_info, colors, True)
				yield True
				queue_action.put(2*indx +2)
		

	while finish > 1:
		lst[0], lst[finish -1] = lst[finish -1], lst[0]
		draw_list(draw_info, {0 : draw_info.RED, finish-1 : draw_info.GREEN}, True)
		yield True
		finish -= 1

		queue_action = queue.Queue()
		queue_action.put(0)
		while not queue_action.empty():

			indx = queue_action.get()
			actual_value = lst[indx] * ascending_num
			colors = {indx : draw_info.GREEN}

			if 2*indx +1 < finish:
				right_son = lst[2*indx +1] * ascending_num
				colors[2*indx +1] = draw_info.BLUE
			else:
				right_son = None
		
			if 2*indx +2 < finish:
				left_son = lst[2*indx +2] * ascending_num 
				colors[2*indx +2] = draw_info.BLUE
			else:
				left_son = None
		
			draw_list(draw_info, colors, True)
			yield True

			if not left_son:
				left_son = actual_value
			if not right_son:
				right_son = actual_value
		
			if actual_value != max([left_son, right_son, actual_value]):

				if right_son > left_son:
					lst[indx], lst[2*indx +1] = lst[2*indx + 1], lst[indx]
					colors[2*indx +1] = draw_info.GREEN
					colors[indx] = draw_info.BLUE

					draw_list(draw_info, colors, True)
					yield True
					queue_action.put(2*indx +1)
				else:
					lst[indx], lst[2*indx +2] = lst[2*indx + 2], lst[indx]
					colors[2*indx +2] = draw_info.GREEN
					colors[indx] = draw_info.BLUE

					draw_list(draw_info, colors, True)
					yield True
					queue_action.put(2*indx +2)
		
	return lst

def selection_sort(draw_info, ascending=True):
	lst = draw_info.lst
	ascending_num = 1 if ascending == True else -1

	for start_indx in range(len(lst)):
		min_number = lst[start_indx] * ascending_num
		min_indx_number = start_indx

		for indx in range(start_indx +1, len(lst)):
			draw_list(draw_info, {indx : draw_info.RED, min_indx_number : draw_info.GREEN}, True)
			yield True

			if lst[indx] * ascending_num < min_number:
				min_number = lst[indx] * ascending_num
				min_indx_number = indx
		lst[start_indx], lst[min_indx_number] = lst[min_indx_number], lst[start_indx]

	return lst 


def main():
	run = True
	clock = pygame.time.Clock()

	n = 32
	min_val = 0
	max_val = 100

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(1100, 760, lst)
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(10)
        
		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				clock.tick(1)
				lst = draw_info.lst
				ascending_num = 1 if ascending == True else -1
				last_number = lst[0] * ascending_num
				colors = {0 : draw_info.GREEN}


				for indx in range(1, len(lst)):
					number = lst[indx] * ascending_num
					colors[indx] = draw_info.RED
					draw_list(draw_info, colors, True)
					if number < last_number : 
						break
					else:
						last_number = number 
						colors[indx] = draw_info.GREEN
				draw_list(draw_info, colors, True)
				sorting = False
				clock.tick(10)
		else:
			draw(draw_info, sorting_algo_name, ascending)
        
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

			elif event.key == pygame.K_a and not sorting:
				ascending = True

			elif event.key == pygame.K_d and not sorting:
				ascending = False

			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"

			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"
			
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selection_sort
				sorting_algo_name = "Selection Sort"
			
			elif event.key == pygame.K_m and not sorting:
				sorting_algorithm = merge_sort
				sorting_algo_name = "Merge Sort"
			
			elif event.key == pygame.K_q and not sorting:
				sorting_algorithm = quick_sort
				sorting_algo_name = "Quick Sort"
			
			elif event.key == pygame.K_h and not sorting:
				sorting_algorithm = heap_sort
				sorting_algo_name = "Heap Sort"
			

	pygame.quit()



if __name__ == "__main__":
    main()