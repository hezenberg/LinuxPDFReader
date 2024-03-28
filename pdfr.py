from pypdf import PdfReader
from time import sleep
import os
import sys
import shutil 
import tty, termios, sys


class Interface:


	@staticmethod
	def hide_cursor():
		sys.stdout.write("\033[?25l")
		sys.stdout.flush()


	@staticmethod
	def show_cursor():
		sys.stdout.write("\033[?25h")
		sys.stdout.flush()


	@staticmethod
	def draw_statbar(current_page, over_page):
		text = ("page {0}/{1} q - exit pdfr | <-- s | w --> | i - enter page".format(current_page, over_page))
		print(Interface.draw_text_center(text.strip(), 0, 1))


	@staticmethod
	def draw_hellopage():
		print(Interface.draw_text_center("Hello its soft by MAXSOFTWARE.\nkey[Q] - exit\nkey[W] - next\nkey[S] - back\nkey[I] - inset page", 1, 1))

	@staticmethod
	def draw_text_center(text, is_height = False, is_widht = False):
		ready_text = ''
		h_spc = ''
		w_spc = ''
		w_term, h_term = shutil.get_terminal_size()
		lines = text.split('\n')
		lines_len = []
	
		if is_widht:
			for i, val in enumerate(lines):	lines_len.insert(i, len(val)) 
			max_widht_str = max(lines_len)
			tab_x = round((w_term - max_widht_str) / 2) 
			for i in range(tab_x): w_spc += ' '
		if is_height:
			tab_y = round((h_term - len(lines)) / 2)
			for i in range(tab_y): h_spc += '\n'

		for line in lines: ready_text += w_spc + line + '\n'
		ready_text = h_spc + ready_text

		return ready_text

			




class PDFReader:
	def __init__(self):
		self.current_page = 0
		self.over_count_page = 0
		self.pages = None
		self.file = None
		self.file_path = '/'
		self.height_term = 0
		self.widht_term = 0

	def start_program_loop(self):
		self.get_argv()
		self.check_file()
		self.update_drawing()

		reader = PdfReader(self.file_path)
		self.pages = reader.pages

		self.over_count_page = len(self.pages)
   		
		os.system("clear")
		Interface.hide_cursor()
		Interface.draw_hellopage()
		Interface.draw_statbar(self.current_page, self.over_count_page)

		while 1:
			
			fd = sys.stdin.fileno()
			old_settings = termios.tcgetattr(fd)
			try:
				tty.setraw(sys.stdin.fileno())
				key = sys.stdin.read(1)
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			if key == 'q':
				os.system("clear")
				exit(0)
			elif key == 'w':
				self.next_page()
			elif key == 's':
				self.back_page()
			elif key == 'i':
				Interface.show_cursor()
				try:
					enter_page = int(input("page: "))
				except ValueError:
					print("page its number!")
					continue
				if enter_page > self.over_count_page:
					print("page > {0}".format(self.over_count_page))
					continue
				enter_page = int(enter_page)
				self.current_page = enter_page
				self.page_draw()
				Interface.hide_cursor()
			self.update_drawing()
	 

	def get_argv(self):
		if len(sys.argv) > 1:
			self.file_path = sys.argv[1]
		else:
			print("pdfr [path_to_pdf]")
			exit()

	def check_file(self):
		if os.path.isfile(self.file_path) == False:
			print("pdfr - file not found!")
			exit(1)
		self.file = open(self.file_path, "rb")


	def next_page(self):
		self.current_page += 1
		self.page_draw()


	def back_page(self):
		self.current_page -= 1
		self.page_draw()


	def page_draw(self):
		os.system("clear")
		if self.current_page <= 0:
			Interface.draw_hellopage()
			self.current_page = 0
			return
		if self.current_page > self.over_count_page:
			self.current_page = self.over_count_page
			return
		text_page = self.pages[self.current_page].extract_text()
		print(text_page)
		Interface.draw_statbar(self.current_page, self.over_count_page)


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