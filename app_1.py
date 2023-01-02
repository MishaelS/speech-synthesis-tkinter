import tkinter.ttk as ttk
import webbrowser
import sys, os
import random

from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.scrolledtext import *
from tkinter import *

from playsound import playsound
from gtts import gTTS

# ------------------------------------------------------------------------------------

WIDTH  = 420
HEIGHT = 420

# ------------------------------------------------------------------------------------

class MainWindow(Tk):
	def __init__(self):
		super().__init__()
		self.title("Speech Synthesis")
		self.geometry(f"{WIDTH}x{HEIGHT}")
		self.resizable(width=False, height=False)

		self.speech_lang = StringVar(self)
		self.file_extension = StringVar(self)

		self.speech_lang.set("ru")
		self.file_extension.set(".mp3")

		### Creating the main menu bar -----------------------------------------------
		self.mainmenu = Menu(self)
		self.config(menu=self.mainmenu)

		# Init of the main menu panels
		self.menu_file()
		self.menu_tools()
		self.menu_help()

		# Menu Displays
		self.mainmenu.add_cascade(label="Файл", menu=self.filemenu)
		self.mainmenu.add_cascade(label="Инструменты", menu=self.toolsmenu)
		self.mainmenu.add_cascade(label="Помогите", menu=self.helpmenu)

		self.frm = Frame(self)

		self.scrollbar_x = Scrollbar(master=self.frm, orient=HORIZONTAL)
		self.scrollbar_x.pack(side=BOTTOM, fill=BOTH)

		self.scrollbar_y = Scrollbar(master=self.frm)
		self.scrollbar_y.pack(side=RIGHT, fill=BOTH)

		self.textbox = Text(master=self.frm,
							width=50,
							height=50,
							# bg=,
							# fg=,
							# bd=,
							# font=,
							wrap=NONE)
		self.textbox.insert("end", "Это пробный текст который можно испытать!\nThis is a trial text that can be tested!")
		self.textbox.pack(side=LEFT, expand=True)

		self.textbox.config(xscrollcommand=self.scrollbar_x.set)
		self.textbox.config(yscrollcommand=self.scrollbar_y.set)

		self.scrollbar_x.config(command=self.textbox.xview)
		self.scrollbar_y.config(command=self.textbox.yview)

		self.frm.pack(expand=True)

		# ----------------------------------------------------------------------------

		self.mainloop()

	### Creating menu panels ---------------------------------------------------------
	def menu_file(self):
		self.filemenu = Menu(self.mainmenu, tearoff=0)
		self.filemenu.add_command(label="Новый файл"    , accelerator="Ctrl+N", command=self.file_new_file)
		self.filemenu.add_command(label="Открыть файл...", accelerator="Ctrl+O", command=self.file_open_file)
		self.filemenu.add_command(label="Сохранить как..."  , accelerator="Ctrl+Shift+S", command=self.file_save_as)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Выйти", accelerator="Ctrl+Q", command=self.file_quit)

	def menu_tools(self):
		self.toolsmenu = Menu(self.mainmenu, tearoff=0)
		self.toolsmenu.add_command(label="Синтез речи", accelerator="Alt+S", command=self.tools_speech)
		self.toolsmenu.add_command(label="Синтез текста", accelerator="Alt+T", command=self.tools_text)
		self.toolsmenu.add_separator()

		self.langmenu = Menu(self.toolsmenu, tearoff=0)
		self.langmenu.add_radiobutton(label="Русский", variable=self.speech_lang, value="ru")
		self.langmenu.add_radiobutton(label="Английский", variable=self.speech_lang, value="en")
		self.toolsmenu.add_cascade(label="Язык озвучки", menu=self.langmenu)

		self.expansionmenu = Menu(self.toolsmenu, tearoff=0)
		self.expansionmenu.add_radiobutton(label="MP3", variable=self.file_extension, value=".mp3")
		self.expansionmenu.add_radiobutton(label="WAV", variable=self.file_extension, value=".wav")
		self.expansionmenu.add_radiobutton(label="OGG", variable=self.file_extension, value=".ogg")
		self.expansionmenu.add_radiobutton(label="FLAC", variable=self.file_extension, value=".flac")
		self.toolsmenu.add_cascade(label="Расширение аудиофайла", menu=self.expansionmenu)

	def menu_help(self):
		self.helpmenu = Menu(self.mainmenu, tearoff=0)
		self.helpmenu.add_command(label="Помогите", command=self.help_window)
		self.helpmenu.add_command(label="О программе", command=self.info_window)

	### Creating commands ------------------------------------------------------------

	# File Menu
	def file_new_file(self):
		showwarning(title="Окно предупреждения",
					message="Эта функция еще не реализована, так как она может работать некорректно.",
					detail="При создании нового окна и использовании его функций вы не сможете использовать главное окно!",
					icon="warning",
					type="ok")

	def file_open_file(self):
		try:
			filepath = askopenfilename(filetypes=[('All Files', '*.*')],
									   defaultextension=[('All Files', '*.*')])

			if filepath == (): return

			with open(filepath, 'r') as file:
				text = str(file.read())
				self.textbox.delete("1.0", END)
				self.textbox.insert("end", text)

		except Exception as ex:
			showerror(title="Окно ошибки",
					  message=f"Exception: {ex}",
					  detail="Если вы не знаете, в чем ошибка, то обратитесь в службу поддержки!",
					  icon="error",
					  type="ok")

	def file_save_as(self):
		try:
			filepath = asksaveasfile(initialfile=str(self.randname()) + str(self.file_extension.get()),
									 filetypes=[('All Files', '*.*')],
									 defaultextension=str(self.file_extension.get()))

			if filepath is None: return
			filepath = filepath.name

			text = self.textbox.get("1.0", END)

			var = gTTS(text=text, lang=self.speech_lang.get())
			var.save( filepath )

		except Exception as ex:
			os.remove( filepath )
			showerror(title="Окно ошибки",
					  message=f"Exception: {ex}",
					  detail="",
					  icon="error",
					  type="ok")
		
	def file_quit(self):
		self.destroy()

	# Tools Menu
	def tools_speech(self):
		try:
			showwarning(title="Окно предупреждения",
						message="Синтез речи может занять некоторое время!",
						detail="После прослушивания файл будет удален...",
						icon="warning",
						type="ok")


			text = self.textbox.get("1.0", END)

			self.filename = self.randname()
			var = gTTS(text=text, lang=self.speech_lang.get())
			var.save( str(self.filename + self.file_extension.get()) )
			playsound( f"./{str(self.filename + self.file_extension.get())}" )

		except Exception as ex:
			showerror(title="Окно ошибки",
					  message=f"Exception: {ex}",
					  detail="",
					  icon="error",
					  type="ok")
		finally:
			os.remove( str(self.filename + self.file_extension.get()) )

	def tools_text(self):
		try:
			showwarning(title="Окно предупреждения",
						message="Это функция пока не реализована!",
						detail="",
						icon="warning",
						type="ok")
			
		except Exception as ex:
			showerror(title="Окно ошибки",
					  message=f"Exception: {ex}",
					  detail="",
					  icon="error",
					  type="ok")
		finally:
			pass

	# Help Menu
	def help_window(self):
		result = askyesno(title="Окно справки",
						  message="Если у вас возникли проблемы с программой, пожалуйста, обратитесь в службу поддержки!",
						  detail="salofutdinov.misha02@gmail.com",
						  icon="info",
						  type="yesno")
		
		if result: webbrowser.open("mailto:salofutdinov.misha02@gmail.com")

	def info_window(self):
		showinfo(title="Информационное окно",
				 message="Программа доступна для бесплатного использования, всю информацию можно найти на GitHub!",
				 detail="https://github.com/MishaelS",
				 icon="info",
				 type="ok")

	def randname(self):
		name = ''
		symbols = 'qwertyuiopasdfghjklzxcvbnm1234567890'
		for i in range(6):
			name += random.choice(symbols)
		return name 

# ------------------------------------------------------------------------------------

if __name__ == '__main__':
	win = MainWindow()
	sys.exit(0)