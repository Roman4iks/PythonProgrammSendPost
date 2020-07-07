import requests
from tkinter import filedialog
import tkinter as tk
from tkinter import Menu
import json
import pyperclip

root = tk.Tk()
root.title("MyFirstProgramm")
menu = Menu(root)
menu.add_command(label='File')
root.config(menu=menu)
new_item = Menu(menu)
new_item.add_command(label='Новое')
menu.add_cascade(label='Файл', menu=new_item)
new_item.add_separator()
new_item.add_command(label='Редактирование')




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

		self.dirs = tk.Entry(width = 40, textvariable = self.urlTextEntry)
		self.url = tk.Entry(width = 40, textvariable = self.dirsTextEntry)
		self.data = tk.Entry(width = 20, textvariable = self.dataTextEntry)
		self.data_value = tk.Entry(width = 20, textvariable = self.data_valueTextEntry)

		self.button_files_dir = tk.Button(root, text = "...", command =self.file_dir)
		self.button_data_add = tk.Button(root, text = "Добавить", command =self.data_add)
		self.button_data_edit = tk.Button(root, text = "Изменить", command =self.data_edit)
		self.button_data_delete = tk.Button(root, text = "Удалить", command =self.data_delete)
		self.button_send_data_POST = tk.Button(root, text = "Отправить POST", command =self.send_POST)
		self.button_send_data_GET = tk.Button(root, text = "Отправить GET", command =self.send_GET)

		self.button_test = tk.Button(root, text = "ТестКнопка", command =self.test)
		
		self.list_box_2 = tk.Listbox()

		self.L0.grid(row = 0, column = 2)
		self.L1.grid(row = 3, column = 2, rowspan = 1)
		self.L2.grid(row = 1, column = 2)
		
		self.url.grid(row = 1, column = 1, padx = 20)
		self.data.grid(row = 1, column = 1, columnspan = 2)
		self.data_value.grid(row = 1, column = 2, columnspan = 2)
		self.dirs.grid(row = 1, column = 3, pady = 10, padx = 20)

		self.button_send_data_POST.grid(row = 2, column = 1)
		self.button_send_data_GET.grid(row = 3, column = 1)

		self.button_data_edit.grid(row = 2, column = 1, columnspan = 2)
		self.button_data_add.grid(row = 2, column = 2, columnspan = 1)
		self.button_data_delete.grid(row = 2, column = 2, columnspan = 3)
		self.button_files_dir.grid(row = 2, column = 3)
		
		self.button_test.grid(row = 3, column = 3)

		self.list_box_2.grid(row = 5 ,column = 2, sticky = tk.W+tk.E)

		self.dirs.insert(0,'Выберите файлы')
		self.url.insert(0,'http://httpbin.org/post')
		
		self.list_box_2.bind("<<ListboxSelect>>", self.test)
		
		
		self.dirs.bind('<FocusIn>', self.on_entry_click)

	def on_entry_click(self,get):
		print(get)
		q = pyperclip.paste()
		if q != "":
			self.url.delete(0, "end") # delete all the text in the entry
			self.url.insert(0, q) #Insert blank for user input
		else:
			pass
	
	def file_dir(self):
		file = filedialog.askopenfilename()
		
		self.dirs.insert(0, f"{file},")

	def data_add(self):
		data = self.data.get()
		data_value = self.data_value.get()

		if data == '':
			pass
		else:
			sel = self.list_box_2.curselection()
			self.list_box_2.insert(0, f'{data} : {data_value}')

	def data_edit(self):
		data = self.data.get()
		data_value = self.data_value.get()
		
		index = self.list_box_2.curselection()

		self.list_box_2.delete(index, index)
		self.list_box_2.insert(0, f'{data} : {data_value}')

	def data_delete(self):
		cursor_data = self.list_box_2.curselection()

		if sel == ():
			pass
		else:
			self.list_box_2.delete(cursor_data[0])

	def send_POST(self):
		dirs = self.dirs.get()
		url = self.url.get()
		dirs_files = dirs.split(',')
		dirs_files.pop()

		files = {}
		files_data = []

		if dirs_files == []:
			files_dates = None
		else:
			for dir_file in dirs_files:
				file_name = dir_file.split('/')[-1]
				files_data += [(file_name ,open(file_name,'rb'))]

			files_dates = files_data

		data_box = {}

		for data in self.list_box_2.get(0, tk.END):
			data_key = data.split(" : ")[0]
			data_value = data.split(" : ")[1]
			if data_value == "":
				data_box[data_key] = ""
			else:
				data_box[data_key] = data_value

		s = requests.post(url, data = data_box, json = data_box, files = files_dates if files_dates != "" else None)
		log = s.text

		try:
			json_data = json.loads(log)
		except json.decoder.JSONDecodeError:
			self.L1['text'] = "Ошибка POST JSON данные не получены"
			return 

		list_box = tk.Listbox()
		
		list_box.grid(row = 4 ,column = 2, sticky = tk.W+tk.E)

		for name in json_data:
			if name == "headers":
				for name_head in json_data['headers']:
					list_box.insert(0, f"    {name_head} --> {json_data['headers'][name_head]}")
				list_box.insert(0, f"{name} -->")
			else:
				if json_data[name] == None or json_data[name] == {} or json_data[name] == " ":
					pass
				else:
					list_box.insert(0, f"{name} --> {json_data[name]}")

	def send_GET(self):
		dirs = self.dirs.get()
		url = self.url.get()
		dirs_files = dirs.split(',')
		dirs_files.pop()

		data = self.list_box_2.get(0, tk.END)
		param = {}

		files = {}
		files_data = []

		if dirs_files == []:
			files_dates = None
		else:
			for dir_file in dirs_files:
				file_name = dir_file.split('/')[-1]
				files_data += [(file_name, open(file_name,'rb'))]

			files_dates = files_data

		for str_data in data:
			data_key = str_data.split(" : ")[0]
			data_value = str_data.split(" : ")[1]

			param[data_key] = data_value

		s = requests.get(url, params = param, files = files_dates)
		log = s.text

		try:
			json_data = json.loads(log)
		except json.decoder.JSONDecodeError:
			self.L1['text'] = "Ошибка GET JSON данные не получены"
			return 

		list_box = tk.Listbox()
		list_box.grid(row = 4 ,column = 2, sticky = tk.W+tk.E)

		for key in json_data:
			if key == "headers":
				for headers_data in json_data[key]:
					list_box.insert(0, f"    {headers_data} --> {json_data[key][headers_data]}")
				list_box.insert(0, f"{key} --> ")
			else:
				list_box.insert(0, f"{key} --> {json_data[key]}")

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
s = Programm(root)

root.mainloop()