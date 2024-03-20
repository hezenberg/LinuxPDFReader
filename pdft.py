import sys
from pypdf import PdfReader
import os
import shutil 
from colorama import Fore, Back, Style
import tty, termios, sys

class PDFReader:
	def __init__(self):
		self.current_page = 0
		self.over_count_page = 0
		self.pages = None
		self.file = None
		self.file_path = '/'
		self.start_program_loop()


	def start_program_loop(self):
		self.get_argv()
		self.check_file()

		reader = PdfReader(self.file_path)
		self.pages = reader.pages

		self.over_count_page = len(self.pages)
   	
		self.draw_statbar()
		while 1:
			fd = sys.stdin.fileno()
			old_settings = termios.tcgetattr(fd)
			try:
				tty.setraw(sys.stdin.fileno())
				ch = sys.stdin.read(1)
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			if ch == 'q':
				exit(0)
			elif ch == 'w':
				self.next_page()
	 

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
		H,W = shutil.get_terminal_size()
		stats_s = (Back.WHITE + Fore.BLACK+"Enter - next | page " + 
		str(self.current_page) + "/" + str(self.over_count_page) + "q - exit w - next s - back" + Style.RESET_ALL)
		spce = ((H - len(stats_s)) / 2)
		for i in range(int(spce)): spce_s += " "
		print(spce_s + stats_s)


	def next_page(self):
		self.current_page += 1
		self.page_draw()
		self.draw_statbar()

	def page_draw(self):
		os.system("clear")
		text_page = self.pages[self.current_page].extract_text()
		print(text_page)


def init():
	PDF = PDFReader()
	PDF.start_program_loop()

if __name__ == '__main__':
	init()