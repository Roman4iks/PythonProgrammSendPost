import os
import json
import tkinter as tk
import uuid
from tkinter import filedialog, scrolledtext, messagebox
from tkinter.ttk import Radiobutton 
import requests

class MyApp:
	def __init__(self, root):
		
		self.root = root
		
		urlTextEntry = tk.StringVar()
		entry_dirTextEntry = tk.StringVar()
		
		frame = tk.LabelFrame(root, text = 'Выбор файла')
		self.frame_console = tk.Frame(root, bg = "#ffffff")
		frame_bot = tk.Frame(root)
		
		self.entry_dir = tk.Entry(frame, textvariable = entry_dirTextEntry)

		self.list_box_3 = self.list_box()

		self.btn_select = tk.Button(frame, text = "...", command = self.file_select, width = 3)
		self.btn_send = tk.Button(frame, text = "Отправить", command = self.send)
		self.btn_options = tk.Button(frame_bot, text = "Опции", command = lambda:Options(root, self.entry_dir))

		self.Label_log = tk.Label(self.frame_console, text = 'Лог')
		
		self.console = scrolledtext.ScrolledText(self.frame_console)

		frame.pack(side = tk.TOP, fill = tk.X, padx = 70)
		frame_bot.pack(side = tk.BOTTOM, fill = tk.X)
		self.frame_console.pack(fill = tk.BOTH, expand = 1)

		self.Label_log.pack()
		
		self.console.pack_forget()

		self.entry_dir.pack(side = tk.TOP, fill = tk.X, padx = 10, pady = 10)
		
		self.btn_select.pack(side = tk.LEFT, padx = 10)
		self.btn_send.pack(side = tk.RIGHT, padx = 10)
		self.btn_options.pack(side = tk.RIGHT, anchor = tk.SW, pady = 10, padx = 20)

		file = open("Test.txt", "w")

		file.write("""Hello World
			My name is Roman
			I live in Ukraine
			I love Python
			My nickname Maran
			Thanks""")

		file.close()

		root.protocol('WM_TAKE_FOCUS', self.loadoptions)
		
		self.loadoptions()

		self.entry_dir.insert(0, self.dir_files)
		
	
	def createoption(self):
		options_file = open("options.txt", "w")
		options_file.write("url : http://httpbin.org/post\n")
		options_file.write("file_name : test.txt\n")
		options_file.write("SendPethod : 0\n")
		options_file.write("dir_file : D:\n")
		options_file.close()

	def loadoptions(self, lo = None):
		try:
			if open("options.txt", "r").read() == "":
				self.createoption()
				self.loadoptions()
			else:
				options_file = open("options.txt", "r").read().split('\n')
				options_file.pop()
				for option in options_file:
					option_values = option.split(' : ')

					if option_values[0] == "url":
						self.url = option_values[1]
					
					if option_values[0] == "file_name":
						self.file_name = option_values[1]
					
					if option_values[0] == "SendPethod":
						self.selected = option_values[1]
					
					if option_values[0] == "dir_file":
						self.dir_files = option_values[1]

		except FileNotFoundError:
			self.createoption()
			self.loadoptions()

	def send(self):
		self.loadoptions()

		dir_file = self.entry_dir.get()
		name_file = self.file_name
		url = self.url
		selected = self.selected

		if len(url.split('://')) > 2:
			url = f"http://{url}"

		if name_file == "":
			name_file = self.entry_dir.get().split('/')[-1]

		if self.Check_Entry([dir_file, name_file, url]):
			return

		try:
			file = [(name_file, open(dir_file, 'rb'))]
		except PermissionError:
			tk.messagebox.showerror('Ошибка', f'Выберите файл!')
			return
		except FileNotFoundError:
			tk.messagebox.showerror('Ошибка', f'Файл не найден!')
			return

		if int(self.selected) == 1:
			try:
				data_url = requests.get(url, files = file)
			except requests.exceptions.MissingSchema:
				tk.messagebox.showerror('Ошибка', f'Некоректный ввод ссылки')
				return
			except requests.exceptions.ConnectionError:
				tk.messagebox.showerror('Ошибка', f'Ошибка соединеня')
				return
			except:
				tk.messagebox.showerror('Ошибка', f'Неизвестная ошибка')
				return
		elif int(self.selected) == 0:
			try:	
				data_url = requests.post(url, files = file)
			except requests.exceptions.MissingSchema:
				tk.messagebox.showerror('Ошибка', f'Некоректный ввод ссылки')
				return
			except requests.exceptions.ConnectionError:
				tk.messagebox.showerror('Ошибка', f'Ошибка соединеня')
				return
			except:
				tk.messagebox.showerror('Ошибка', f'Неизвестная ошибка')
				return

		data = data_url.text

		try:
			json_data = json.loads(data)

			self.console.pack_forget()
			
			self.list_box_3.pack(fill = tk.X, side = tk.TOP, padx = 30)

			self.list_box_3.delete(*self.list_box_3.get_children())
			
			self.json_load(self.list_box_3, "", json_data)

		except Exception as e:
			self.list_box_3.pack_forget()
			self.console.pack(fill = tk.X, side = tk.TOP, padx = 30)
			self.console.delete(1.0, tk.END)
			self.console.insert(tk.INSERT, data)
			
			return

	def json_load(self, tree, parent, data):
		for key in data:
			uid = uuid.uuid4()
			if isinstance(data[key], dict):

				tree.insert(parent, 'end', uid, text = key)
				self.json_load(tree, uid, data[key])
			
			elif isinstance(data[key], list):
			
				tree.insert(parent, 'end', uid, text = key + '[]')
				self.json_load(tree, uid, dict([(x,i) for i, x in enumerate(data[key])]))
			
			else:
				value = data[key]
				if value is None:
					value = 'None'
				tree.insert(parent, 'end', uid, text = key + f'--> {value}')		

	def list_box(self):

		list_box_3 = tk.ttk.Treeview(self.frame_console)
		
		list_box_3.heading('#0', text='Project tree', anchor='w')
		
		list_box_3.pack_forget()

		return list_box_3

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
	def __init__(self, root, dir_file):
		self.window = tk.Toplevel(root)
		self.window.title("Options")

		self.urlTextEntry = tk.StringVar()
		self.EntryNameTextEntry = tk.StringVar()
		
		self.selected = tk.IntVar()
		self.Name_select = tk.IntVar()

		self.frame_url = tk.Frame(self.window)
		self.frame_get_post = tk.Frame(self.window)
		self.frame_file_name = tk.Frame(self.window)

		self.LabelUrl = tk.Label(self.frame_url, text = "Сыллка запроса")
		self.LabelGetPost = tk.Label(self.frame_get_post, text = "Способ отправки")
		self.LabelFileName = tk.Label(self.frame_file_name, text = "Имя файла")

		self.url = tk.Entry(self.frame_url, textvariable = self.urlTextEntry)
		self.Entry_Name = tk.Entry(self.frame_file_name, textvariable = self.EntryNameTextEntry)
		
		self.GET = tk.Radiobutton(self.frame_get_post, text = "GET", value = 1, variable = self.selected)
		self.POST = tk.Radiobutton(self.frame_get_post, text = "POST", value = 0, variable = self.selected)
		
		self.btn_Accept = tk.Button(self.window, text = "Accept", command = self.Accept)

		self.frame_url.pack()
		self.frame_get_post.pack()
		self.frame_file_name.pack()

		self.url.pack(side = tk.RIGHT)
		self.Entry_Name.pack(side = tk.LEFT)

		self.LabelFileName.pack(side = tk.LEFT)
		self.LabelGetPost.pack(side = tk.LEFT)
		self.LabelUrl.pack(side = tk.LEFT)
		
		self.btn_Accept.pack(side = tk.RIGHT)
		
		self.GET.pack(side = tk.LEFT)
		self.POST.pack(side = tk.LEFT)

		self.dir_file = dir_file.get()

		options_file = open("options.txt", "r").read().split('\n')
		options_file.pop()
		
		for option in options_file:
			option_values = option.split(' : ')
			
			if option_values[0] == "url":
				self.url_options = option_values[1]
			
			if option_values[0] == "file_name":
				self.file_name = option_values[1]
			
			if option_values[0] == "dir_file":
				self.dir_files = option_values[1]
		
		if self.url_options == "":
			self.url.insert(0, "http://httpbin.org/post")
		else:
			self.url.insert(0,self.url_options)

		if self.file_name == "":
			self.Entry_Name.insert(0, dir_file.get().split('/')[-1])
		else:
			self.Entry_Name.insert(0, self.file_name)

	def Accept(self):
		url = self.url.get()
		file_name = self.Entry_Name.get()
		selected = self.selected.get()

		file = open('options.txt', 'w')
		file.write(f'url : {url}\n')
		file.write(f'file_name : {file_name}\n')
		file.write(f'SendPethod : {selected}\n')
		file.write(f'dir_file : {self.dir_file}\n')
		file.close()
		
		close = True
		return url, close, file_name, self.window.destroy() 

def main():
	root = tk.Tk()
	
	root.title("Post_sendv2")
	root.geometry('800x500')

	MyApp(root)

	root.mainloop()

main()