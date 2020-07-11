import requests
from tkinter import filedialog
import tkinter as tk
from tkinter.ttk import Combobox
import json
import pyperclip

root = tk.Tk()
root.title("MyFirstProgramm")


#file = filedialog.askopenfilename()
#print(file)

#print("--------------------------------------------------")

#files = filedialog.askopenfilenames()
#print(files)

#print("--------------------------------------------------")

#files_txt = filedialog.askopenfilename(filetypes = (('Только текстовые файлы','*.txt'),('Все файлы','*.*')))
#print(files_txt)

#print("--------------------------------------------------")

#dirs = filedialog.askdirectory()
#print(dirs)


class Programm():
	def __init__(self,root):

		self.L0 = tk.Label(text = "Выберите файл который хотите отправить на серврер", font = "Arial 15", justify = tk.CENTER)
		self.L1 = tk.Label(text = "Обязательно проверте запрос GET или POST", font = "Arial 10", justify = tk.CENTER)
		self.L2 = tk.Label(text = ":", font = "Arial 25", justify = tk.CENTER)
		
		self.urlTextEntry = tk.StringVar()
		self.dirsTextEntry = tk.StringVar()
		self.dataTextEntry = tk.StringVar()
		self.data_valueTextEntry = tk.StringVar()
		self.nameTextEntry = tk.StringVar()

		self.dirs = tk.Entry(width = 40, textvariable = self.urlTextEntry)
		self.name = tk.Entry(width = 40, textvariable = self.nameTextEntry)
		self.url = tk.Entry(width = 40, textvariable = self.dirsTextEntry)
		self.data = tk.Entry(width = 20, textvariable = self.dataTextEntry)
		self.data_value = tk.Entry(width = 20, textvariable = self.data_valueTextEntry)

		self.button_files_dir = tk.Button(root, text = "...", command =self.file_dir)
		self.button_files_add = tk.Button(root, text = "Добавить файл", command =self.file_add)
		self.button_data_add = tk.Button(root, text = "Добавить", command =self.data_add)
		self.button_data_edit = tk.Button(root, text = "Изменить", command =self.data_edit)
		self.button_data_delete = tk.Button(root, text = "Удалить", command =self.data_delete)
		self.button_send_data_POST = tk.Button(root, text = "Отправить POST", command =self.send_POST)
		self.button_send_data_GET = tk.Button(root, text = "Отправить GET", command =self.send_GET)
		self.button_urls_save = tk.Button(root, text = "Добавить ссылку", command =self.urls_save)
		self.button_test = tk.Button(root, text = "ТестКнопка", command =self.test)
		
		self.list_box = tk.Listbox()
		self.list_box_2 = tk.Listbox()

		self.button_place_data = tk.Button(root, text = "Вставить данные", command = lambda: PlaceText(self.list_box_2))

		self.combox = Combobox(root)

		self.L0.grid(row = 0, column = 2)
		self.L1.grid(row = 3, column = 2)
		self.L2.grid(row = 1, column = 2)
		
		self.url.grid(row = 1, column = 1, padx = 20)
		self.data.grid(row = 1, column = 1, columnspan = 2)
		self.data_value.grid(row = 1, column = 2, columnspan = 2)
		self.dirs.grid(row = 1, column = 3, pady = 10, padx = 20)
		self.name.grid(row = 2, column = 3)

		self.button_send_data_POST.grid(row = 2, column = 1)
		self.button_send_data_GET.grid(row = 3, column = 1)
		self.button_urls_save.grid(row = 4, column = 1)
		self.combox.grid(row = 5, column = 1, rowspan = 3)

		self.button_place_data.grid(row = 6, column = 1)

		self.button_data_edit.grid(row = 2, column = 1, columnspan = 2)
		self.button_data_add.grid(row = 2, column = 2, columnspan = 1)
		self.button_data_delete.grid(row = 2, column = 2, columnspan = 3)
		self.button_files_dir.grid(row = 3, column = 3)
		self.button_files_add.grid(row = 4, column = 3)
	
		self.list_box.grid(row = 4 ,column = 2, sticky = tk.W+tk.E)
		self.list_box_2.grid(row = 5 ,column = 2, sticky = tk.W+tk.E)

		self.dirs.insert(0,'Выберите файл')
		self.url.insert(0,'http://httpbin.org/post') # https://truecoding.ru/guild/pvp2.php

		
		self.list_box_2.bind("<<ListboxSelect>>", self.focusbox)
		self.combox.bind("<<ComboboxSelected>>", self.focuscombox)

		root.protocol("WM_DELETE_WINDOW", self.save_session)

		json_data_str = open("session.json")
		try:
			json_data = json.load(json_data_str)
			for data_json in json_data:
				if json_data[data_json] == None or json_data[data_json] == []:
					pass
				else:
					if data_json == "url":
						url_data = json_data[data_json]
						self.url.delete(0, tk.END)
						self.url.insert(0, url_data)
					elif data_json == "dirs":
						dirs_data = json_data[data_json]
						self.dirs.delete(0, tk.END)
						self.dirs.insert(0, dirs_data)
					elif data_json == "name":
						name_data =json_data[data_json]
						self.name.delete(0, tk.END)
						self.name.insert(0, name_data)
					elif data_json == "data":
						data_data = json_data[data_json]
						self.data.delete(0, tk.END)
						self.data.insert(0, data_data)
					elif data_json == "data_value":
						data_value_data = json_data[data_json]
						self.data_value.delete(0, tk.END)
						self.data_value.insert(0, data_value_data)
					elif data_json == "listbox":
						self.list_box.delete(0, tk.END)
						for data_list in json_data[data_json][::-1]:
							self.list_box.insert(0, data_list)
					elif data_json == "listbox2":
						self.list_box_2.delete(0, tk.END)
						for data_list in json_data[data_json][::-1]:
							self.list_box_2.insert(0, data_list)
					elif data_json == "urls":
						self.combox['values'] = json_data[data_json]
		except json.decoder.JSONDecodeError:
			pass

	def urls_save(self):
		url = self.url.get()
		urls = []
		urls.append(url)
		for value in self.combox["values"]:
			urls.append(value)
		self.combox["values"] = urls

	def focusbox(self,get):
		cursor = self.list_box_2.curselection()
		data_all = self.list_box_2.get(cursor, cursor)
		for data in data_all:
			data_key = data.split(' : ')[0]
			data_value = data.split(' : ')[1]

			if data_key == "file":
				data_name = data_value.split(" --> ")[0]
				data_dir = data_value.split(" --> ")[1]
				
				self.dirs.delete(0, tk.END)
				self.name.delete(0, tk.END)

				self.dirs.insert(0, data_dir)
				self.name.insert(0, data_name)
			else:
				self.data.delete(0, tk.END)
				self.data_value.delete(0, tk.END)

				self.data.insert(0, data_key)
				self.data_value.insert(0, data_value)

	def focuscombox(self,get):
		cursor = self.combox.get()
		self.url.delete(0, tk.END)
		self.url.insert(0, cursor)

	def file_dir(self):
		file = filedialog.askopenfilename()
		
		self.dirs.delete(0, tk.END)
		self.name.delete(0, tk.END)

		self.dirs.insert(0, f"{file}")
		self.name.insert(0, f"{file.split('/')[-1]}")


	def Check_key(self, data):

		data_key1 = data

		print(data_key1)

		data = self.list_box_2.get(0, tk.END)

		for data_key_value in data:
			data_key2 = data_key_value.split(' : ')[0]
			if data_key2 == 'file':
				data_key = data_key_value.split(' : ')[1]
				data_key2 = data_key.split(' --> ')[0]
			if data_key1 == data_key2:
				self.L1['text'] = "Ошибка Такие данные уже есть в таблице пожалуйста введите другое название"
				return 1

	def file_add(self):
		file = self.dirs.get()
		name = self.name.get()

		if self.Check_key(name) == 1:
			return

		self.name.delete(0, tk.END)
		self.dirs.delete(0, tk.END)

		if name != "":
			if self.Check_key(name) != 1:
				self.list_box_2.insert(0, f'file : {name} --> {file}')
			else:
				return
		else:
			if file == "" or file == "Выберите файл":
				self.L1['text'] = "Ошибка Выберите файл пожалуйста"
				return
			else:
				file = file.split('/')[-1]
				if self.Check_key(file) == 1:
					return
				else: 
					self.list_box_2.insert(0, f'file : {file.split("/")[-1]} --> {file}')

	def data_add(self):
		data = self.data.get()
		data_value = self.data_value.get()

		check = self.Check_key(data)

		if check == 1:
			return

		self.data_value.delete(0, tk.END)
		self.data.delete(0, tk.END)

		if data == "" and data_value == "":
			self.L1['text'] = "Ошибка Введите данные"
			return
		if data == "" and data_value != "":
			self.L1['text'] = "Ошибка Введите данные в первое поле ввода"
			return
		else:
			if data == '':
				self.list_box_2.insert(0, f'{data} : ""')
			else:
				self.list_box_2.insert(0, f'{data} : {data_value}')

	def data_edit(self):
		index = self.list_box_2.curselection()
		data = self.list_box_2.get(index, index)
		print(data)
		key = data[0].split(' : ')[0]

		if key == "file":
			dirs = self.dirs.get()
			name = self.name.get()

			self.list_box_2.delete(index, index)
			self.list_box_2.insert(index, f"file : {name} --> {dirs}")
		else:
			data = self.data.get()
			data_value = self.data_value.get()

			self.list_box_2.delete(index, index)
			self.list_box_2.insert(index, f'{data} : {data_value}')

	def data_delete(self):
		cursor_data = self.list_box_2.curselection()

		if cursor_data == ():
			pass
		else:
			self.list_box_2.delete(cursor_data[0])

	def send_POST(self):
		url = self.url.get()
		
		files_dates = {}
		files_data = []

		data_box = {}
		self.list_box.delete(0, tk.END)
		data_all = self.list_box_2.get(0, tk.END)
		
		if data_all == ():
			self.L1['text'] = "Ошибка Пожалуйста добавте данные для POST запроса"
			return


		for data in data_all:
			data_key = data.split(" : ")[0]
			data_value = data.split(" : ")[1]
			if data_key == "file":
				name = data_value.split(' --> ')[0]
				dirs = data_value.split(' --> ')[1]

				files_data += [(name, open(dirs, 'rb'))]
				files_dates = files_data
			else:
				if data_value == "":
					data_box[data_key] = ""
				else:
					data_box[data_key] = data_value

		if data_box == {}:
			data_box = None

		if files_dates == {}:
			files_dates = None

		s = requests.post(url, data = data_box, json = data_box, files = files_dates)
		log = s.text

		try:
			json_data = json.loads(log)
		except json.decoder.JSONDecodeError:
			self.L1['text'] = "Ошибка POST запроса ответа некоректный"
			return 

		for name in json_data:
			if name == "headers":
				for name_head in json_data['headers']:
					self.list_box.insert(0, f"    {name_head} --> {json_data['headers'][name_head]}")
				self.list_box.insert(0, f"{name} -->")
			else:
				if json_data[name] == None or json_data[name] == {} or json_data[name] == " ":
					pass
				else:
					self.list_box.insert(0, f"{name} --> {json_data[name]}")

	def send_GET(self):
		url = self.url.get()		

		data_box = {}

		files_data = []
		files_dates = {}

		self.list_box.delete(0, tk.END)

		data_all = self.list_box_2.get(0, tk.END)
		
		if data_all == ():
			self.L1['text'] = "Ошибка Пожалуйста добавте данные для GET запроса"
			return

		for data in data_all:
			data_key = data.split(" : ")[0]
			data_value = data.split(" : ")[1]
			if data_key == "file":
				name = data_value.split(' --> ')[0]
				dirs = data_value.split(' --> ')[1]

				files_data += [(name, open(dirs, 'rb'))]
				files_dates = files_data
			else:
				if data_value == "":
					data_box[data_key] = ""
				else:
					data_box[data_key] = data_value

		if data_box == {}:
			data_box = None

		if files_dates == {}:
			files_dates = None

		s = requests.get(url, params = data_box, files = files_dates)
		log = s.text

		try:
			json_data = json.loads(log)
		except json.decoder.JSONDecodeError:
			self.L1['text'] = "Ошибка GET запроса ответа некоректный"
			return 

		for key in json_data:
			if key == "headers":
				for headers_data in json_data[key]:
					self.list_box.insert(0, f"    {headers_data} --> {json_data[key][headers_data]}")
				self.list_box.insert(0, f"{key} --> ")
			else:
				self.list_box.insert(0, f"{key} --> {json_data[key]}")

	def test(self):
		q = pyperclip.paste()
		dirs = self.dirs.get()
		dir_file = dirs.split(',')
		dir_file.pop()
		return
		data = self.list_box_2.get(self.list_box_2.curselection())
		
		data_key = data.split(" : ")[0]
		data_value = data.split(" : ")[1]

		self.data.delete(0, tk.END)
		self.data_value.delete(0, tk.END)

		self.data.insert(0, data_key)
		self.data_value.insert(0, data_value)

	def save_session(self):
		url = self.url.get()
		dirs = self.dirs.get()
		name = self.name.get()
		data = self.data.get()
		data_value = self.data_value.get()
		data_listbox1 = self.list_box.get(0, tk.END)
		data_listbox2 = self.list_box_2.get(0, tk.END)
		urls = []
		for value in self.combox["values"]:
			urls.append(value)
		
		if data == "":
			data = None

		if data_value == "":
			data_value = None

		if name == "":
			name = None

		if dirs == "" or dirs == "Выберите файл":
			dirs = None

		if url == "":
			url = None

		json_data = {}
		json_data["url"] = url
		json_data["urls"] = urls
		json_data["dirs"] = dirs
		json_data["name"] = name
		json_data["data"] = data
		json_data["data_value"] = data_value
		json_data["listbox"] = data_listbox1
		json_data["listbox2"] = data_listbox2

		file = open('session.json', 'w')

		file.write(json.dumps(json_data))

		file.close()

		root.destroy()
class PlaceText:
	def __init__(self, listbox2):
		self.rooter = tk.Toplevel(root)
		self.rooter.title('Place')
		self.listbox2 = listbox2

		self.TextEntry = tk.StringVar()

		self.text = tk.Text(self.rooter, wrap = tk.WORD)
		self.btn = tk.Button(self.rooter, text = "Place", command = self.place)
		self.btn_text = tk.Button(self.rooter, text = "Вставить из буфера обмена", command = self.place_text)

		self.text.grid(row = 1, column = 1)
		self.btn.grid(row = 2, column = 1)
		self.btn_text.grid(row = 2, column = 2)

	def place_text(self):
		q = pyperclip.paste()
		self.text.insert(1.0, q)

	def place(self):
		text_place = self.text.get(1.0, tk.END)
		json_data = json.loads(text_place)

		self.listbox2.delete(0, tk.END)

		for data,value in json_data.items():
			self.listbox2.insert(0, f"{data} : {value}")
			
		def __missing__(self, key):
			pass

		return self.rooter.destroy()


s = Programm(root)

root.mainloop()
