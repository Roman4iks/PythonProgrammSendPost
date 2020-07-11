import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinter.ttk import Radiobutton 
import requests

class MyApp:
	def __init__(self, root):
		self.root = root
		
		urlTextEntry = tk.StringVar()
		entry_dirTextEntry = tk.StringVar()

		self.selected = tk.IntVar()
		self.Name_select = tk.IntVar()

		self.entry_dir = tk.Entry(root, width = 90, textvariable = entry_dirTextEntry)

		self.btn_select = tk.Button(root, text = "Select", command = self.file_select)
		self.btn_send = tk.Button(root, text = "Send", command = self.send)
		self.btn_options = tk.Button(root, text = "Options", command = lambda:Options(root))

		self.GET = tk.Radiobutton(root, text = "GET", value = 0, variable = self.selected)
		self.POST = tk.Radiobutton(root, text = "POST", value = 1, variable = self.selected)

		self.console = scrolledtext.ScrolledText(root)

		self.entry_dir.pack()
		self.btn_select.pack()
		self.btn_options.pack()
		self.btn_send.pack()
		self.GET.pack()
		self.POST.pack()
		self.console.pack()

		self.EntryNameTextEntry = tk.StringVar()
		self.Entry_Name = tk.Entry(self.root, textvariable = self.EntryNameTextEntry)

		self.Entry_Name.place(x = 100, y = 100)

		file = open("Test.txt", "w")

		file.write("""Hello World
			My name is Roman
			I live in Ukraine
			I love Python
			My nickname Maran
			Thanks""")

		file.close()

		self.entry_dir.insert(0,'D:/Важное/Программирование/PythonCode/Programs/PostSend/PythonProgrammSendPost v2/Test.txt')
		self.Entry_Name.insert(0, self.entry_dir.get().split('/')[-1])
		root.bind('<Button-1>', self.loadoptions)

	def loadoptions(self, lo = None):
		try:
			options_file = open("options.txt", "r").read()
			self.url = options_file
		except FileNotFoundError:
			options_file = open("options.txt", "w")
			options_file.write("http://httpbin.org/post")

	def send(self):
		dir_file = self.entry_dir.get()
		name_file = self.Entry_Name.get()
		url = self.url

		if name_file == "":
			name_file = self.entry_dir.get().split('/')[-1]

		if self.Check_Entry([dir_file, name_file, url]):
			return

		try:
			file = [(name_file, open(dir_file, 'rb'))]
		except FileNotFoundError:
			tk.messagebox.showerror('Ошибка', f'файл не найден!')
			return

		if self.selected.get() == 1:
			data_url = requests.post(url, files = file)
		elif self.selected.get() == 0:
			data_url = requests.get(url, files = file)

		data = data_url.text

		self.console.delete(1.0, tk.END)
		self.console.insert(tk.INSERT, data)
		
		return


	def file_select(self):
		file = tk.filedialog.askopenfilename()
		if file == "":
			return
		self.entry_dir.delete(0, tk.END)
		self.entry_dir.insert(0, file)

	def Check_Entry(self, entrytext):
		for text in entrytext:
			if text == "":
				tk.messagebox.showerror('Ошибка', f'введите данные')
				return True

class Options:
	def __init__(self, root):
		self.window = tk.Toplevel(root)
		self.window.title("Options")

		urlTextEntry = tk.StringVar()

		self.LabelUrl = tk.Label(self.window, text = "Сыллка запроса")
		self.url = tk.Entry(self.window, textvariable = urlTextEntry)
		self.btn_Accept = tk.Button(self.window, text = "Accept", command = self.Accept)

		self.url.pack(side = tk.LEFT)
		self.LabelUrl.pack(side = tk.LEFT)
		self.btn_Accept.pack(side = tk.RIGHT)

		file = open('options.txt', 'r').read()
		self.url.insert(0,file)
	def Accept(self):
		url = self.url.get()
		file = open('options.txt', 'w')
		file.write(url)
		file.close()
		close = True
		return url, close, self.window.destroy()

def main():
	root = tk.Tk()
	root.title("Post_send v2")
	root.geometry('700x500')


	MyApp(root)

	root.mainloop()

main()