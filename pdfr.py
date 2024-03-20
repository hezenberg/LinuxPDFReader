import sys
from pypdf import PdfReader
import os
import shutil 
from colorama import Fore, Back, Style
import tty, termios, sys
from time import sleep

class CreatePages:
	def __init__(self):
		self.height_term, self.widht = shutil.get_terminal_size()




class PDFReader:
	def __init__(self):
		self.current_page = 0
		self.over_count_page = 0
		self.pages = None
		self.file = None
		self.file_path = '/'
		self.height_term = 0
		self.widht_term = 0

		self.old_height_term = 0
		self.old_widht_term = 0

	def start_program_loop(self):
		self.get_argv()
		self.check_file()
		self.update_drawing()

		reader = PdfReader(self.file_path)
		self.pages = reader.pages

		self.over_count_page = len(self.pages)
   	
		self.draw_statbar()

		while 1:
			
			fd = sys.stdin.fileno()
			old_settings = termios.tcgetattr(fd)
			try:
				tty.setraw(sys.stdin.fileno())
				key = sys.stdin.read(1)
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			if key == 'q':
				exit(0)
			elif key == 'w':
				self.next_page()
			elif key == 's':
				self.back_page()
			elif key == 'i':
				self.current_page = int(input("page: "))
				self.page_draw()

			self.update_drawing()
			sleep(0.30)
	 

	def get_argv(self):
		if len(sys.argv) > 1:
			self.file_path = sys.argv[1]
		else:
			print("pdfr [path_to_pdf]")
			exit()


	def check_file(self):
		if os.path.isfile(self.file_path) == False:
			print("pdfr - file not found! runing pdfr only ROOT!")
			exit(1)
		self.file = open(self.file_path, "rb")


	def draw_statbar(self):
		spce_s = ""
		stats_s = (Back.WHITE + Fore.BLACK+"page " + 
		str(self.current_page) + "/" + str(self.over_count_page) + " q - exit w - next s - back " + 
		"w" + str(self.widht_term) + " h"+str(self.height_term) + Style.RESET_ALL)
		spce = ((self.height_term - len(stats_s)) / 2)
		for i in range(int(spce)): spce_s += " "
		print(spce_s  + "### "+ stats_s + " ###" + spce_s)


	def next_page(self):
		if self.current_page > self.over_count_page:
			return
		self.current_page += 1
		self.page_draw()


	def back_page(self):
		if self.current_page <= 0:
			return
		self.current_page -= 1
		self.page_draw()


	def page_draw(self):
		os.system("clear")
		text_page = self.pages[self.current_page].extract_text()
		print(text_page)
		self.draw_statbar()


	def update_drawing(self):
		height = shutil.get_terminal_size()[0]
		widht = shutil.get_terminal_size()[1]
		
		self.widht_term = widht
		self.height_term = height

				


def init():
	PDF = PDFReader()
	PDF.start_program_loop()

if __name__ == '__main__':
	init()