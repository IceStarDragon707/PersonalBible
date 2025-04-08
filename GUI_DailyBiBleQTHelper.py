import tkinter as tk
import tkinter.messagebox as tkm
from PIL import Image, ImageTk
import cv2
import BibleDownloaderReference as BDR
import time
from datetime import datetime
import traceback
import random
import os
import requests
from tkinter import ttk as tk_combo
from tkinter import font
from tkinter import filedialog


##### ------------------------- next update : astract ------------------------- #####


class Theme:
	colors = [] ## different color including: 'BibleContent', 'BibleTitle', 'div', 'button', ...
	def __init__(self, color_panel):
		self.colors = color_panel


## user preference
global_file_name = 'appearance.config'
default_font_size = 12
default_font = 'TkDefaultFont'
default_theme = 'Deafult'
if os.path.exists(global_file_name):
	with open(global_file_name, 'r') as file:
		content = file.read()
		arr = [c.split('=')[-1] for c in content.split('\n')]
		default_font_size = int(arr[0]) if arr[0]!='' else default_font_size
		default_font = arr[1] if arr[1]!='' else default_font
		default_theme = arr[2] if arr[2]!='' else default_theme
else:
	with open(global_file_name, 'w') as file:
		file.writelines('default_font_size=\n')
		file.writelines('default_font=\n')
		file.writelines('default_theme=\n')



##### ------------------------- next update ------------------------- #####

def on_main_window_close():
    print("Main window is closing")
    root.destroy()
## pop-out screen
def on_sub_window_close(sub_window_id):
	print("Sub-window is closing")
	if sub_window_id==1:
		sub_window1.destroy()
		open_sub_window_button1.config(text="<開啟>\n靈修筆記區")
	elif sub_window_id==2:
		sub_window2.destroy()
		open_sub_window_button2.config(text="<開啟>\n歸納式查經")
	# sub_window.grab_release()  # Release grab on sub-window
def on_sub_window_resize(sub_window, size_label):
	width = sub_window.winfo_width()
	height = sub_window.winfo_height()
	size_label.config(text=f"Width: {width}, Height: {height}")
def open_sub_window__default():
	if sub_window is None or not sub_window.winfo_exists():
		sub_window = tk.Toplevel(window)
		sub_window.title("Div")
		
		notebook = tk.ttk.Notebook(sub_window)
		notebook.pack(fill="both", expand=True)
		
		div_frame = tk.ttk.Frame(notebook)
		notebook.add(div_frame, text="Div")
		
		button1 = tk.ttk.Button(div_frame, text="Button 1")
		button2 = tk.ttk.Button(div_frame, text="Button 2")
		combobox1 = tk.ttk.Combobox(div_frame, values=["Option 1", "Option 2"])
		combobox2 = tk.ttk.Combobox(div_frame, values=["Option A", "Option B"])
		button1.pack(padx=10, pady=5)
		button2.pack(padx=10, pady=5)
		combobox1.pack(padx=10, pady=5)
		combobox2.pack(padx=10, pady=5)
	else:
		sub_window1.grab_set()  # Prevent interactions with main window
		flash_sub_window(sub_window1)
def str__ChangeFontSize(NoteContent_Text, arr, index, font):
	print('Change Text Font-Size To %d' % arr[index])
	font_style = (font, arr[index])
	NoteContent_Text.tag_configure("custom_font", font=font_style)
	NoteContent_Text.tag_add("custom_font", "1.0", tk.END)
subwindow1_fontsize_index = 0
subwindow2_fontsize_index = 0
Note__fontsize_array = [12, 14, 16, 18, 20]
subwindow1_font = "TkDefaultFont"
subwindow2_font = "TkDefaultFont"
def NoteContent__font_size_increase(NoteContent_Text, id_, subwindow_default_font):
	global subwindow1_fontsize_index
	global subwindow2_fontsize_index
	global Note__fontsize_array
	if id_==1:
		Note__fontsize_array_index = subwindow1_fontsize_index
	elif id_==2:
		Note__fontsize_array_index = subwindow2_fontsize_index
	tmp_Note__fontsize_array_index = Note__fontsize_array_index + 1
	if tmp_Note__fontsize_array_index>=len(Note__fontsize_array):
		(sub_window1 if id_==1 else sub_window2).grab_set()
		if tkm.askyesno("提示~", "字體最大 = %d"%Note__fontsize_array[Note__fontsize_array_index]):
			(sub_window1 if id_==1 else sub_window2).grab_release()  # Release the grab on the sub-window
		Note__fontsize_array_index = len(Note__fontsize_array) - 1
	else:
		Note__fontsize_array_index = tmp_Note__fontsize_array_index
	if id_==1:
		subwindow1_fontsize_index = Note__fontsize_array_index
	elif id_==2:
		subwindow2_fontsize_index = Note__fontsize_array_index
	str__ChangeFontSize(NoteContent_Text, Note__fontsize_array, Note__fontsize_array_index, subwindow_default_font)
	# print('Change Text Font-Size To %d' % Note__fontsize_array[Note__fontsize_array_index])
	# font_style = (subwindow_default_font, Note__fontsize_array[Note__fontsize_array_index])
	# NoteContent_Text.tag_configure("custom_font", font=font_style)
	# NoteContent_Text.tag_add("custom_font", "1.0", tk.END)
	flash_sub_window(sub_window1 if id_==1 else sub_window2, 0)
def NoteContent__font_size_decrease(NoteContent_Text, id_, subwindow_default_font):
	global subwindow1_fontsize_index
	global subwindow2_fontsize_index
	global Note__fontsize_array
	if id_==1:
		Note__fontsize_array_index = subwindow1_fontsize_index
	elif id_==2:
		Note__fontsize_array_index = subwindow2_fontsize_index
	tmp_Note__fontsize_array_index = Note__fontsize_array_index - 1
	if tmp_Note__fontsize_array_index<0:
		(sub_window1 if id_==1 else sub_window2).grab_set()
		if tkm.askyesno("提示~", "字體最小 = %d"%Note__fontsize_array[Note__fontsize_array_index]):
			(sub_window1 if id_==1 else sub_window2).grab_release()  # Release the grab on the sub-window
		Note__fontsize_array_index = 0
	else:
		Note__fontsize_array_index = tmp_Note__fontsize_array_index
	if id_==1:
		subwindow1_fontsize_index = Note__fontsize_array_index
	elif id_==2:
		subwindow2_fontsize_index = Note__fontsize_array_index
	str__ChangeFontSize(NoteContent_Text, Note__fontsize_array, Note__fontsize_array_index, subwindow_default_font)
	# print('Change Text Font-Size To %d' % Note__fontsize_array[Note__fontsize_array_index])
	# font_style = (subwindow_default_font, Note__fontsize_array[Note__fontsize_array_index])
	# NoteContent_Text.tag_configure("custom_font", font=font_style)
	# NoteContent_Text.tag_add("custom_font", "1.0", tk.END)
	flash_sub_window(sub_window1 if id_==1 else sub_window2, 0)
def str__ChangeFont(NoteContent_Text, FontSelected, id_):
	global Note__fontsize_array_index
	global Note__fontsize_array
	global subwindow1_font
	global subwindow2_font
	if FontSelected:
		if ColorSelected!=(subwindow1_font if id_==1 else subwindow2_font):
			print('Change Text Font To %r' % newFont__Com.get())
		font_style = (FontSelected, Note__fontsize_array[subwindow1_fontsize_index] if id_==1 else Note__fontsize_array[subwindow2_fontsize_index])
		NoteContent_Text.tag_configure("custom_font", font=font_style)
		NoteContent_Text.tag_add("custom_font", "1.0", tk.END)
	if id_==1:
		subwindow1_font = FontSelected
	elif id_==2:
		subwindow2_font = FontSelected
global_color_list = ['black', 'dim gray', 'dark slate gray', 'red', 'deep pink', 'blue', 'dodger blue', 'yellow4', 'gold4', 'purple']
subwindow1_fontcolor = 'black'
subwindow2_fontcolor = 'black'
def str__ChangeColor(NoteContent_Text, ColorSelected, id_):
	global subwindow1_fontcolor
	global subwindow2_fontcolor
	global subwindow1_font
	global subwindow2_font
	global Note__fontsize_array
	global subwindow1_fontsize_index
	global subwindow2_fontsize_index
	if ColorSelected:
		if ColorSelected!=(subwindow1_fontcolor if id_==1 else subwindow2_fontcolor):
			print('Change Text Color To %r' % ColorSelected)
		font_style = (subwindow1_font if id_==1 else subwindow2_font, Note__fontsize_array[subwindow1_fontsize_index] if id_==1 else Note__fontsize_array[subwindow2_fontsize_index])
		NoteContent_Text.tag_configure("custom_color", foreground=ColorSelected)
		NoteContent_Text.tag_add("custom_color", "1.0", tk.END)
	if id_==1:
		subwindow1_fontcolor = ColorSelected
	elif id_==2:
		subwindow2_fontcolor = ColorSelected
def UpdateNoteStyle(NoteContent_Text, id_):
	global Note__fontsize_array
	global subwindow1_fontsize_index
	global subwindow2_fontsize_index
	global subwindow1_font
	global subwindow2_font
	global subwindow1_fontcolor
	global subwindow2_fontcolor
	global default_font
	if id_==1:
		str__ChangeColor(NoteContent_Text, subwindow1_fontcolor, id_)
		str__ChangeFont(NoteContent_Text, subwindow1_font, id_)
		str__ChangeFontSize(NoteContent_Text, Note__fontsize_array, subwindow1_fontsize_index, Note__fontsize_array[subwindow1_fontsize_index])
	elif id_==2:
		str__ChangeColor(NoteContent_Text, subwindow2_fontcolor, id_)
		str__ChangeFont(NoteContent_Text, subwindow2_font, id_)
		str__ChangeFontSize(NoteContent_Text, Note__fontsize_array, subwindow2_fontsize_index, Note__fontsize_array[subwindow2_fontsize_index])
def NoteContent__NewPage(NoteContent_Text, id_, mode):
	global global_saving_pos
	global_saving_pos = None
	flag = NoteContent_Text.get("1.0", tk.END)=='\n'
	# print(flag)
	# [print('%r'%c) for c in NoteContent_Text.get("1.0", tk.END)]
	flag = flag if flag else NoteContent_Text.get("1.0", tk.END)!='\n' and tkm.askyesno('[警告]', '確定開啟新分頁，若尚未儲存，資料將遭刪除。')
	# print(flag)
	if flag:
		NoteContent_Text.delete(1.0, tk.END)
		data_exmaples = f'''
範例 I：
	(彼前5:7~11)
		觀察
			1.什麼是一切的憂慮?
			2.我為什麼要卸下一切的憂慮?
			3.我可以如何處理憂慮?
		解釋
			1.我所有的難題或掛心的事。
			2.因為神顧念我，而且魔鬼要吞吃我。
			3.將憂慮卸給神，求神賜恩典，列下信心不堅固的原因，神召我得永遠的榮耀。
		應用
			我不必為我的籌款不足和身體狀況憂慮，我可以禱告並信靠天父，，因祢愛我顧念我，我不要被不好的經驗影響，我要相信祢的呼召和應許。

範例 II：
	III_ADVANCED
		i.學習找出自己的疑問與好奇
		ii.設身處地思考自己是當事人，並要怎麼解決在自己現在的問題
		iii.學習思考在這個過程， 神的做為有什麼、神為什麼要這麼做；也可以反思人與 神的顧念與想法有什麼不同
		iiii.驗證
	(可4:35~41)
		觀察
			1. 門徒為什麼害怕？
			2.  耶穌為什麼責備他們？
			III_ADVANCED.i.iii
				3.  耶穌為什麼在睡覺？還是 他只是真的累了？
				5. 他們面對風浪的反應？
			III_ADVANCED.i.ii
				4. 門徒此時到底覺得 耶穌是誰？
		解釋
			1. 因為怕被浪捲走或沉船吧！
			2. 因為他們不相信 耶穌， 耶穌前面說"我們度到那邊去"？
			3. (暫時不知道)
			4. (暫時不知道)
		應用
			(針對面對擔憂與害怕，更加的信靠 神)
			(是否相信 神是掌管萬有的 神)
			III_ADVANCED.iiii.驗證
				針對自己的應用，是否可以得到 神的回應
				(個人)(具體)(有回應)

		'''
		seg3 = f'''
範例 III(格式說明)：
		'''
		data_format = f'''
	(取自'經文')
		觀察
			1. ...
			2. ...
			3. ...
		解釋
			1. ...
			2. ...
			3. ...
		應用
			1. ...
			2. ...
			3. ...
	III_ADVANCED
		i.疑問(異想天開)
		ii.設身處地(自己的應對):(自我與歷史借鑑)
		iii.屬靈扎根( 神的心意):(人 神對比)
		iiii.驗證:(提出法則/驗證法則)
		'''
		data = '' if mode=='Empty' else '格式：'+data_format if mode=='New' else data_exmaples+seg3+data_format if 'Examples' else 'IMPOSSIBLE'
		NoteContent_Text.insert(tk.INSERT, data)
		UpdateNoteStyle(NoteContent_Text, id_)
		flash_sub_window(sub_window1 if id_==1 else sub_window2, 0)
global_saving_pos = None
def NoteContent__SaveContent(NoteContent_Text, id_):
	import subprocess
	global global_note_directory
	global sub_window1
	global sub_window2
	global global_saving_pos
	text_content = NoteContent_Text.get("1.0", tk.END)
	file_name = str(datetime.today().strftime("%Y-%m-%d"))+'__'+('歸納式查經' if id_==2 else '靈修筆記' if id_==1 else '')+'.txt'
	if text_content!='':
		file_path = ''
		if not global_saving_pos:
			file_path = filedialog.asksaveasfilename(
				defaultextension=".txt",
				filetypes=[("Text files", "*.txt")],
				initialfile=file_name,
				initialdir=global_note_directory
				# initialfile="custom_file_name.txt",  # Customize default filename
				# initialdir="C:/Users/YourUsername/Documents"  # Set initial directory
			)
			global_saving_pos = file_path
		else:
			file_path = global_saving_pos
		if file_path:
			with open(file_path, "w", encoding='utf-8') as file:
				file.write(text_content)
			if tkm.askyesno('[注意]', '此檔案(%s)將存在(%r)。是否開啟位置。'%(file_name, global_note_directory)):
				# os.system()
				subprocess.Popen(f'explorer "{global_note_directory}"')
	flash_sub_window(sub_window1 if id_==1 else sub_window2, 0)
def open_sub_window_1():
	global window
	global sub_window1
	if sub_window1 is None or not sub_window1.winfo_exists():
		open_sub_window_button1.config(text="<顯示>\n靈修筆記區")
		sub_window1 = tk.Toplevel(window)
		sub_window1.title("靈修筆記區")
		
		sub_window1.protocol("WM_DELETE_WINDOW", lambda: on_sub_window_close(sub_window_id=1))  # Set up detection

		notebook = tk.ttk.Notebook(sub_window1)
		notebook.pack(fill="both", expand=True)
		
		div_frame = tk.ttk.Frame(notebook)
		notebook.add(div_frame, text="Div")
		
		NoteContent_Text = tk.Text(div_frame, font=("Times New Roman", Note__fontsize_array[Note__fontsize_array_index]), wrap='word')
		NoteContent_Text_scrollbar = tk.Scrollbar(div_frame)
		NoteContent_Text.config(yscrollcommand=NoteContent_Text_scrollbar.set) ## 設定讀條(scrolling-bar)調比例與內容相同
		NoteContent_Text_scrollbar.config(command=NoteContent_Text.yview) ## 設定讀條(scrolling-bar)可以做用在textbox上
		NoteContent_Text.grid(column=1, row=1, columnspan=4, sticky=align_mode)
		NoteContent_Text_scrollbar.grid(column=5, row=1, columnspan=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)

		# button1 = tk.ttk.Button(div_frame, text="Button 1")
		# button2 = tk.ttk.Button(div_frame, text="Button 2")
		# combobox1 = tk.ttk.Combobox(div_frame, values=["Option 1", "Option 2"])
		# combobox2 = tk.ttk.Combobox(div_frame, values=["Option A", "Option B"])
		# button1.pack(padx=10, pady=5)
		# button2.pack(padx=10, pady=5)
		# combobox1.pack(padx=10, pady=5)
		# combobox2.pack(padx=10, pady=5)

		size_label = tk.Label(div_frame, text="Width: 300, Height: 200")
		# size_label.pack(padx=20, pady=10)
		size_label.grid(column=0, row=2, columnspan=2, sticky=align_mode)

		sub_window1.bind("<Configure>", lambda x: on_sub_window_resize(sub_window1, size_label))
	else:
		# sub_window1.grab_set()  # Prevent interactions with main window
		flash_sub_window(sub_window1)
def open_sub_window_2():
	global window
	global sub_window2
	global global_font_usable_list
	global global_color_list
	global subwindow2_font
	global subwindow2_fontcolor
	global subwindow2_fontsize_index
	if sub_window2 is None or not sub_window2.winfo_exists():
		open_sub_window_button2.config(text="<顯示>\n歸納式查經")
		sub_window2 = tk.Toplevel(window)
		sub_window2.title("歸納式查經區")
		
		sub_window2.protocol("WM_DELETE_WINDOW", lambda: on_sub_window_close(sub_window_id=2))  # Set up detection

		notebook = tk.ttk.Notebook(sub_window2)
		notebook.pack(fill="both", expand=True)
		
		div_frame = tk.ttk.Frame(notebook)
		notebook.add(div_frame, text="Div")
		
		NoteContent_Text = tk.Text(div_frame, font=("Times New Roman", Note__fontsize_array[subwindow2_fontsize_index]), wrap='word')
		NoteContent_Text_scrollbar = tk.Scrollbar(div_frame)
		NoteContent_Text.config(yscrollcommand=NoteContent_Text_scrollbar.set) ## 設定讀條(scrolling-bar)調比例與內容相同
		NoteContent_Text_scrollbar.config(command=NoteContent_Text.yview) ## 設定讀條(scrolling-bar)可以做用在textbox上
		NoteContent_Text.grid(row=3, column=1, columnspan=6, sticky=align_mode)
		NoteContent_Text_scrollbar.grid(row=3, column=7, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)

		# button1 = tk.ttk.Button(div_frame, text="Button 1")
		# button2 = tk.ttk.Button(div_frame, text="Button 2")
		NoteContent__fontsize_add_button = tk.ttk.Button(div_frame, text="+", style="Square.TButton", command=lambda :NoteContent__font_size_increase(NoteContent_Text, 2, subwindow2_font))
		NoteContent__fontsize_add_button.grid(row=1, column=1, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
		NoteContent_Empty_button = tk.Button(div_frame, text="空白筆記頁", command=lambda :NoteContent__NewPage(NoteContent_Text, 2, 'Empty'))
		NoteContent_Empty_button.grid(row=1, column=2, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
		NoteContent_New_button = tk.Button(div_frame, text="新筆記", command=lambda :NoteContent__NewPage(NoteContent_Text, 2, 'New'))
		NoteContent_New_button.grid(row=1, column=3, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
		NoteContent_Example_button = tk.Button(div_frame, text="新筆記與範例", command=lambda :NoteContent__NewPage(NoteContent_Text, 2, 'Examples'))
		NoteContent_Example_button.grid(row=1, column=4, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
		NoteContent_Save_button = tk.Button(div_frame, text="儲存筆記", command=lambda :NoteContent__SaveContent(NoteContent_Text, 2))
		NoteContent_Save_button.grid(row=1, column=5, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
		NoteContent__fontsize_minus_button = tk.ttk.Button(div_frame, text="-", style="Square.TButton", command=lambda :NoteContent__font_size_decrease(NoteContent_Text, 2, subwindow2_font))
		NoteContent__fontsize_minus_button.grid(row=1, column=6, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)


		# combobox1 = tk.ttk.Combobox(div_frame, values=["Option 1", "Option 2"])
		# combobox2 = tk.ttk.Combobox(div_frame, values=["Option A", "Option B"])
		newFont__Com = tk.ttk.Combobox(div_frame, width=10, height=5, values=global_font_usable_list)
		newFont__Com.grid(row=2, column=1, columnspan=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
		newFont__Com.set("字體字型")
		newColor__Com = tk.ttk.Combobox(div_frame, width=10, height=5, values=global_color_list)
		newColor__Com.grid(row=2, column=5, columnspan=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
		newColor__Com.set("字體顏色")


		size_label = tk.Label(div_frame, text="Width: 300, Height: 200")
		size_label.grid(row=2, column=3, columnspan=2, sticky=align_mode)


		sub_window2.bind("<Configure>", lambda x: on_sub_window_resize(sub_window2, size_label))
		# Bind the selection event to the on_item_selected function
		newFont__Com.bind("<<ComboboxSelected>>", lambda x: str__ChangeFont(NoteContent_Text, newFont__Com.get(), 2))
		newColor__Com.bind("<<ComboboxSelected>>", lambda x: str__ChangeColor(NoteContent_Text, newColor__Com.get(), 2))
	else:
		flash_sub_window(sub_window2)

def flash_sub_window(window, flashes=7, delay=20):
	if flashes >= 0:
		window.after(delay, lambda: window.lower() if flashes % 2 else window.lift())
		window.after(delay * 2, lambda: flash_sub_window(window, flashes - 1, delay))

## func
def define_layout(obj, cols=1, rows=1):
	def method(trg, col, row):
		for c in range(cols):    
			trg.columnconfigure(c, weight=1)
		for r in range(rows):
			trg.rowconfigure(r, weight=1)
	if type(obj)==list:
		[ method(trg, cols, rows) for trg in obj ]
	else:
		trg = obj
		method(trg, cols, rows)

def hcf(num1, num2):
	ans = 1
	if num1 > num2:
		smaller = num2
	else:
		smaller = num1
	for i in range(1,smaller + 1):
		if((num1 % i == 0) and (num2 % i == 0)):
			ans = i
	return ans

def UpdateDisplayStyle():
	global Content__fontsize_array_index
	global Content__fontsize_array
	global default_font
	font_style = (default_font, Content__fontsize_array[Content__fontsize_array_index])
	BibleContent_Text.tag_configure("custom_font", font=font_style)
	BibleContent_Text.tag_add("custom_font", "1.0", tk.END)
def displayScript(title, data):
	global BibleTitle_Text
	global global_is_editable

	if not global_is_editable.get():
		if title!=None:
			BibleTitle_Text.set(title)
		BibleContent_Text.config(state='normal')
		BibleContent_Text.delete(1.0, tk.END)
		BibleContent_Text.insert(tk.INSERT, '\n'.join(data))
		# global_word_content.set('\n'.join(data))
		BibleContent_Text.config(state='disabled')
		UpdateDisplayStyle()

## controler
def TextBoxStatusChanging(global_is_editable):
	global global_debug_mode

	if global_debug_mode:
		print('可編輯' if global_is_editable.get() else '不可編輯')
	if global_is_editable.get():
		BibleContent_Text.config(state='normal')
	else:
		BibleContent_Text.config(state='disabled')
def List1_Select(event):
	global global__list_text1
	global global__chapter_num_choice
	global global_debug_mode
	# global timmer_count_

	try: ## because when selecting over another ListBox, will cause and out-of-range error
		selection = bookname__LP1.get(event.widget.curselection()[0])
		# print(selection+'@ %d'%bookname_choices.index(selection))
		# selection_index_LB1 = event.widget.curselection()[0]
		# print(selection_index_LB1, BDR.list_[selection_index_LB1].bookname)
		selection_index_LB1 = bookname_choices.index(selection)
		# print(selection_index_LB1, BDR.list_[bookname_choices.index(selection)].bookname)
		global__list_text1 = BDR.list_[selection_index_LB1].bookname
		window.title('靈修輔助工具 v2'+' --- 查找 %s'%global__list_text1)
		global__chapter_num_choice = [i+1 for i in range(BDR.list_[selection_index_LB1].chapter)]
		if global_debug_mode:
			print("%s[%d]" % (global__list_text1, global__chapter_num_choice[-1]))
		chapter_num__LP2.delete(0, "end")
		for i in global__chapter_num_choice:
			chapter_num__LP2.insert("end", i)
		# if not timmer_count_==-707:
		# 	timmer_count_ = BDR.int_RunTimer()
	except:
		print('', end='')
def List2_Select(event):
	global global__list_text1, global__list_text2
	global global_debug_mode
	global global__verse_num_choice_S, global__verse_num_choice_E
	global global_cur_script
	global timmer_count_
	global timer_readtime

	try: ## because when selecting over another ListBox, will cause and out-of-range error
		selection_index_LB2 = event.widget.curselection()[0]
		## listbox still have an error: "multiple-click" when "dragging" in the box
		# chapter_num__LP2.config(state='disabled')
		global__list_text2 = selection_index_LB2+1
		if global_debug_mode:
			print('Item Selection = [%d]' % global__list_text2)
	except:
		print('', end='')
		return ;
	
	try:
		sum_ = 0
		tmp = None
		for bdr in BDR.list_:
			if bdr.bookname==global__list_text1:
				tmp=bdr
				break
			else:
				sum_ = sum_ + bdr.chapter
		if global__list_text2>tmp.chapter:
			print('[失敗] 查找章節第%d章 大於 %r總章節數%d' % (global__list_text2, global__list_text1, tmp.chapter))
		else:
			window.title('靈修輔助工具 v2'+' --- 查找 %s 第%d章'%(global__list_text1, global__list_text2))
			print('[查找 %s 第%d章]' % (global__list_text1, global__list_text2))
			try:
				global_cur_script = BDR.getScriptContent('https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(global__list_text2+sum_)+'&ver=big5&ft=0&temp=-1&tight=0', False)
			except requests.exceptions.ConnectionError as e:
				print("Error: Could not connect to the website.")
				print("ConnectionError", e)
				traceback.print_exc()
				return ;
			if global_debug_mode:
				print(' --- START --- ', end='')
				BDR.printScript(global_cur_script[0], global_cur_script[1])
				print(' --- END --- ')
			if timmer_count_ == -707:
				record_update('ADD', global_cur_script[0]) ## record the searching result
				UpdateHistory('ADD', ['?']+[[global__list_text1, global__list_text2]]) ## record the searching result
			else:
				if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
					record_update('ADD', global_cur_script[0]) ## record the searching result
					UpdateHistory('ADD', ['?']+[[global__list_text1, global__list_text2]]) ## record the searching result
				else:
					# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
					# 	record_update('ADD', global_cur_script[0]) ## record the searching result
					# else:
					record_update('COVER-LAST', global_cur_script[0]) ## record the searching result
					UpdateHistory('COVER-LAST', ['?']+[[global__list_text1, global__list_text2]]) ## delete the last searching result
			timmer_count_ = BDR.int_RunTimer()
			displayScript(global_cur_script[0], global_cur_script[1])
	except:
		print('', end='')
		return ;
	# chapter_num__LP2.config(state='normal')
	
	try: ## because when selecting over another ListBox, will cause and out-of-range error
		selection_index_LB2 = event.widget.curselection()[0]
		global__list_text3 = selection_index_LB2+1
		if global_debug_mode:
			print('Item Selection = [%d]' % global__list_text3)
		global__verse_num_choice = [i+1 for i in range(len(global_cur_script[1]))]
		## no changes
		global__verse_num_choice_S = global__verse_num_choice_E = global__verse_num_choice
		# verse_num__LP3.delete(0, "end")
		# verse_num__LP4.delete(0, "end")
		# for i in global__verse_num_choice:
		# 	verse_num__LP3.insert("end", i)
		# 	verse_num__LP4.insert("end", i)
		## new edit
		verse_num__Com3["values"] = global__verse_num_choice_S
		verse_num__Com3.set("Select Start Verse")
		verse_num__Com4["values"] = global__verse_num_choice_E
		verse_num__Com4.set("Select End Verse")
	except:
		print('', end='')
		return ;

	# global BibleTitle_Text
	# BibleTitle_Text = global__list_text1+' 第'+str(global__list_text2)+'章'
	# cn_box.delete(0, 'end')
	# cn_box.insert('end', BibleTitle_Text)
	# lbl_quote.text = BibleTitle_Text

## new edit
# def List3_Select(event):
def Combo3_Select(selected_index):
	global global__list_text1, global__list_text2, global__list_text3
	global global_debug_mode
	global timmer_count_
	global timer_readtime

	try: ## because when selecting over another ListBox, will cause and out-of-range error
		## new
		# selection_index_LB3 = event.widget.curselection()[0]
		# global__list_text3 = selection_index_LB3+1
		global__list_text3 = selected_index
		if global_debug_mode:
			print('Item Selection = [%d]' % global__list_text3)
	except:
		print('', end='')
		return ;

	try:
		window.title('靈修輔助工具 v2'+' --- 查找 %s 第%d章 第%d節 開始'%(global__list_text1, global__list_text2, global__list_text3))
		print('[查找 %s 第%d章 第%d節 開始]' % (global__list_text1, global__list_text2, global__list_text3))
		if global_debug_mode:
			print(' --- START --- ', end='')
			BDR.printScript(None, global_cur_script[1][global__list_text3::])
			print(' --- END --- ')
		if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
			record_update('ADD', '%s 第%d章 第%d節 開始'%(global__list_text1, global__list_text2, global__list_text3))
			UpdateHistory('ADD', ['?']+[[global__list_text1, global__list_text2, global__list_text3]]) ## record the searching result
		else:
			if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
				record_update('ADD', '%s 第%d章 第%d節 開始'%(global__list_text1, global__list_text2, global__list_text3))
				UpdateHistory('ADD', ['?']+[[global__list_text1, global__list_text2, global__list_text3]]) ## record the searching result
			else:
				# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
				# 	record_update('ADD', '%s 第%d章 第%d到%d節'%(global__list_text1, global__list_text2, global__list_text3, global__list_text4)) ## record the searching result
				# else:
				record_update('COVER-LAST', '%s 第%d章 第%d節 開始'%(global__list_text1, global__list_text2, global__list_text3))
				UpdateHistory('COVER-LAST', ['?']+[[global__list_text1, global__list_text2, global__list_text3]]) ## delete the last searching result
		displayScript('%s 第%d章 第%d節 開始'%(global__list_text1, global__list_text2, global__list_text3), global_cur_script[1][global__list_text3-1::])
	except:
		print('', end='')
		return ;
# def List4_Select(event):
def Combo4_Select(selected_index):
	global global__list_text1, global__list_text2, global__list_text3,  global__list_text4
	global global_debug_mode
	global timmer_count_
	global timer_readtime

	try: ## because when selecting over another ListBox, will cause and out-of-range error
		## new
		# selection_index_LB4 = event.widget.curselection()[0]
		# global__list_text4 = selection_index_LB4+1
		global__list_text4 = selected_index
		if global_debug_mode:
			print('Item Selection = [%d]' % global__list_text4)
	except:
		print('', end='')
		return ;

	try:
		window.title('靈修輔助工具 v2'+' --- 擷取 %s 第%d章 第%d到%d節'%(global__list_text1, global__list_text2, global__list_text3, global__list_text4))
		print('[擷取 %s 第%d章 第%d到%d節]' % (global__list_text1, global__list_text2, global__list_text3, global__list_text4))
		if global_debug_mode:
			print(' --- START ---', end='')
			BDR.printScript(None, global_cur_script[1][global__list_text3-1:global__list_text4])
			print(' --- END ---')
		if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
			record_update('ADD', '%s 第%d章 第%d到%d節'%(global__list_text1, global__list_text2, global__list_text3, global__list_text4)) ## record the searching result
			UpdateHistory('ADD', ['?']+[[global__list_text1, global__list_text2, global__list_text3, global__list_text4]]) ## record the searching result
		else:
			# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
			# 	record_update('ADD', '%s 第%d章 第%d到%d節'%(global__list_text1, global__list_text2, global__list_text3, global__list_text4)) ## record the searching result
			# else:
			record_update('COVER-LAST', '%s 第%d章 第%d到%d節'%(global__list_text1, global__list_text2, global__list_text3, global__list_text4)) ## record the searching result
			UpdateHistory('COVER-LAST', ['?']+[[global__list_text1, global__list_text2, global__list_text3, global__list_text4]]) ## delete the last searching result
		timmer_count_ = BDR.int_RunTimer()
		displayScript('%s 第%d章 第%d到%d節'%(global__list_text1, global__list_text2, global__list_text3, global__list_text4), global_cur_script[1][global__list_text3-1:global__list_text4])
	except:
		print('', end='')
		return ;

## new edit
def Verse_Combo3(event):
	selected_item = verse_num__Com3.get()
	# print("Selected:", selected_item)
	Combo3_Select(int(selected_item))

def Verse_Combo4(event):
	selected_item = verse_num__Com4.get()
	# print("Selected:", selected_item)
	Combo4_Select(int(selected_item))

Content__fontsize_array_index = 1
Content__fontsize_array = [12, 14, 16, 18, 20]
default_font = "TkDefaultFont"
def BibleContent__font_size_increase():
	global Content__fontsize_array_index
	global Content__fontsize_array
	global default_font
	tmp_Content__fontsize_array_index = Content__fontsize_array_index + 1
	if tmp_Content__fontsize_array_index>=len(Content__fontsize_array):
		result = tkm.askyesno("提示~", "字體最大 = %d"%Content__fontsize_array[Content__fontsize_array_index])
		Content__fontsize_array_index = len(Content__fontsize_array) - 1
	else:
		Content__fontsize_array_index = tmp_Content__fontsize_array_index
	print('Change Text Font-Size To %d' % Content__fontsize_array[Content__fontsize_array_index])
	font_style = (default_font, Content__fontsize_array[Content__fontsize_array_index])
	BibleContent_Text.tag_configure("custom_font", font=font_style)
	BibleContent_Text.tag_add("custom_font", "1.0", tk.END)
def BibleContent__font_size_decrease():
	global Content__fontsize_array_index
	global Content__fontsize_array
	global default_font
	tmp_Content__fontsize_array_index = Content__fontsize_array_index - 1
	if tmp_Content__fontsize_array_index<0:
		result = tkm.askyesno("提示~", "字體最小 = %d"%Content__fontsize_array[Content__fontsize_array_index])
		Content__fontsize_array_index = 0
	else:
		Content__fontsize_array_index = tmp_Content__fontsize_array_index
	print('Change Text Font-Size To %d' % Content__fontsize_array[Content__fontsize_array_index])
	font_style = (default_font, Content__fontsize_array[Content__fontsize_array_index])
	BibleContent_Text.tag_configure("custom_font", font=font_style)
	BibleContent_Text.tag_add("custom_font", "1.0", tk.END)
Title__fontsize_array_index = 1
Title__fontsize_array = [16, 20, 24, 26, 30, 32]
MenuElement__fontsize_array_index = 1
MenuElement__fontsize_array = [10, 12, 14, 16, 18, 20]
def increase(text, value, arr):
	value += 1
	if value>=len(arr):
		value = len(arr) - 1
		result = tkm.askyesno("提示~", "%s = %d"%(text[0], arr[-1]))
	print('Change %s Text Font-Size To %d' % (text[1], arr[value]))
	return value
def decrease(text, value, arr):
	value -= 1
	if value<0:
		value = 0
		result = tkm.askyesno("提示~", "%s = %d"%(text[0], arr[0]))
	print('Change %s Text Font-Size To %d' % (text[1], arr[value]))
	return value
def BibleTitle__font_size_increase():
	global default_font
	global Title__fontsize_array_index
	global Title__fontsize_array
	global MenuElement__fontsize_array_index
	global MenuElement__fontsize_array
	Title__fontsize_array_index = increase(
		['字體最大', 'Title'],
		Title__fontsize_array_index, Title__fontsize_array
	)
	lbl_quote.config(font=(default_font, Title__fontsize_array[Title__fontsize_array_index]))

	MenuElement__fontsize_array_index = increase(
		['清單字體最大', 'Menu Element'],
		MenuElement__fontsize_array_index, MenuElement__fontsize_array
	)
	new_font_size = MenuElement__fontsize_array[MenuElement__fontsize_array_index]
	bookname__LP1.config(font=(default_font, new_font_size))
	chapter_num__LP2.config(font=(default_font, new_font_size))
	verse_num__Com3.config(font=(default_font, new_font_size))
	verse_num__Com4.config(font=(default_font, new_font_size))

	lbl_random_title.config(font=(default_font, new_font_size))
	select_list1.config(font=(default_font, new_font_size))
def BibleTitle__font_size_decrease():
	global default_font
	global Title__fontsize_array_index
	global Title__fontsize_array
	global MenuElement__fontsize_array_index
	global MenuElement__fontsize_array
	Title__fontsize_array_index = decrease(
		['字體最小', 'Title'],
		Title__fontsize_array_index, Title__fontsize_array
	)
	lbl_quote.config(font=(default_font, Title__fontsize_array[Title__fontsize_array_index]))

	MenuElement__fontsize_array_index = decrease(
		['清單字體最小', 'Menu Element'],
		MenuElement__fontsize_array_index, MenuElement__fontsize_array
	)
	new_font_size = MenuElement__fontsize_array[MenuElement__fontsize_array_index]
	bookname__LP1.config(font=(default_font, new_font_size))
	chapter_num__LP2.config(font=(default_font, new_font_size))
	verse_num__Com3.config(font=(default_font, new_font_size))
	verse_num__Com4.config(font=(default_font, new_font_size))

	lbl_random_title.config(font=(default_font, new_font_size))
	select_list1.config(font=(default_font, new_font_size))
def checkFontusale(arr):
	arr_ = []
	for font_name in arr:
		try:
			tk_font = font.Font(font=font_name)
			arr_.append(font_name)
		except tk.TclError:
			print('', end='')
	return arr_
def ChangeFont(event):
	global Content__fontsize_array_index
	global Content__fontsize_array
	global default_font
	tmp_default_font = newFont__Com.get()
	if tmp_default_font:
		default_font = tmp_default_font
		print('Change Text Font To %r' % newFont__Com.get())
		font_style = (default_font, Content__fontsize_array[Content__fontsize_array_index])
		BibleContent_Text.tag_configure("custom_font", font=font_style)
		BibleContent_Text.tag_add("custom_font", "1.0", tk.END)
		lbl_quote.config(font=(default_font, Title__fontsize_array[Title__fontsize_array_index]))
def ChangeTheme(event):
	tmp_default_font = newTheme__Com.get()
	## change color ##

# view_history = [("Item 1", "blue"), ("Item 2", "red"), ("Item 3", "green")]
def updateViewHistory_LP():
	global view_history
	view_history_LP.delete(0, "end")
	for history, color in view_history: #[::-1]:
		view_history_LP.insert("end", history)
		view_history_LP.itemconfig(tk.END, {'fg': color})
def Del_History():
	selected_index = view_history_LP.curselection()[0]
	if selected_index:
		view_history_LP.delete(selected_index)
def Finish_History():
	global timmer_count_
	global view_history
	selected_index = view_history_LP.curselection()[0]
	if selected_index==0:
		timmer_count_ = -707
	# view_history_LP.delete(selected_index)
	# new_name = view_history[selected_index][0].replace('▪️', '✓').replace('✗', '✓')
	# view_history_LP.insert("end", new_name)
	# view_history_LP.itemconfig(tk.END, {'fg': "green"})
	view_history[selected_index] = (view_history[selected_index][0].replace('▪️', '✓').replace('✗', '✓'), "green")
	updateViewHistory_LP()
def LoadHistory(event):
	global timmer_count_
	global timer_readtime
	try:
		selection = view_history_LP.get(event.widget.curselection()[0])
		print(selection)
	except:
		return ;
	print(selection)
	if True:
		# "(state)%s 第%d章 第%d-%d節 @ %d+n"
		data = selection[1::].replace('@ ', '').split(' ')[1::]
		newbo, newch, newver, end_verse, sum_ = None, None, None, None, None
		if len(data)==3:
			newbo, newch, sum_ = data
			newch = newch.replace('第', '').replace('章', '')
			data = [newbo, newch]
		if len(data)==4:
			newbo, newch, newver, sum_ = data
			newch = newch.replace('第', '').replace('章', '')
			newver = newver.replace('第', '').replace('節', '')
			data = [newbo, newch, newver]
			if '-' in newver:
				newver, end_verse = newver.split('-')
				data = [newbo, newch, newver, end_verse]
			print(newbo, newch, newver, end_verse, sum_)
		
		try:
			history_script = BDR.getScriptContent('https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(sum_)+'&ver=big5&ft=0&temp=-1&tight=0', False)
		except requests.exceptions.ConnectionError as e:
			print("Error: Could not connect to the website.")
			print("ConnectionError", e)
			traceback.print_exc()
			return ;
		if global_debug_mode:
			print(' --- START --- ', end='')
			BDR.printScript(history_script[0], history_script[1])
			print(' --- END --- ')

		## final content
		text_ = None
		content_ = None
		if len(data)==2:
			text_ = '%s 第%s章'%(data[0], data[1])
			content_ = history_script[1]
		elif len(data)==3:
			text_ = '%s 第%s章 第%s節 開始'%(data[0], data[1], data[2])
			content_ = global_cur_script[1][int(newver)-1::]
		elif len(data)==4:
			text_ = '%s 第%s章 第%s到%s節'%(data[0], data[1], data[2], data[3])
			content_ = global_cur_script[1][int(newver)-1:int(end_verse)]
		else:
			print('ERROR')
		if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
			record_update('ADD', text_) ## record the searching result
		else:
			# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
			# 	record_update('ADD', history_script[0]+' 第%d節'%int(newver)) ## record the searching result
			# else:
			record_update('COVER-LAST', text_) ## record the searching result
		timmer_count_ = BDR.int_RunTimer()
		displayScript(text_, content_)
def UpdateHistory(mode, data):
	global view_history
	## gen new
	state, detail = data ## detail = ['bookname', 'chapter_num', 'start_verse', 'end_verse']
	curbo = detail[0] ## global__list_text1
	curch = detail[1] ## global__list_text2
	sum_ = 0
	for bdr in BDR.list_:
		if bdr.bookname==curbo:
			break
		else:
			sum_ = sum_ + bdr.chapter
	curver = detail[2] if len(detail)>2 else 1 ## global__list_text3
	curver_end = detail[3] if len(detail)>3 else curver ## global__list_text4
	_record_ = ''
	# print(curbo, curch, curver, curver_end)
	len_ = len(detail)
	if len_==2:
		_record_ = '▪️ ' + "%s 第%d章 @ %d" % (curbo, curch, sum_+curch)
	elif len_==3:
		_record_ = '▪️ ' + "%s 第%d章 第%d節 @ %d+%d" % (curbo, curch, curver, sum_+curch, curver)
	elif len_==4:
		_record_ = '▪️ ' + "%s 第%d章 第%d-%d節 @ %d+(%d-%d)" % (curbo, curch, curver, curver_end, sum_+curch, curver, curver_end-curver)
	## clear old
	# '✓' '✘' '✗' '▪️'
	last_ = view_history[0][0] if len(view_history)>0 else None
	print(last_)
	if last_:
		print(last_)
		if ' '.join(_record_.split(' ')[1::])==' '.join(last_.split(' ')[1::]):
			return ;
		elif any(' '.join(_record_.split(' ')[1::])==' '.join(ll_[0].split(' ')[1::]) for ll_ in view_history):
			return ;
		else:
			if mode=='ADD':
				if '▪️' in last_:
					last_ = last_.replace('▪️', '✓')
				elif '✗' in last_:
					last_ = last_.replace('✗', '✓')
				# else:
				# 	# view_history.append('')
				# 	view_history = [None] + view_history
			elif mode=='COVER-LAST':
				if '▪️' in last_:
					last_ = last_.replace('▪️', '✗')
				else:
					# view_history.append('')
					view_history = [None] + view_history
		# print(last_)
		# view_history = view_history[0:-1]
		view_history = view_history[1::]
		# print((last_[0], 'green' if '✓' in last_ else 'red' if '✗' in last_ else 'black'))
		# view_history.append((last_, 'green' if '✓' in last_ else 'red' if '✗' in last_ else 'black'))
		view_history = [(last_, 'green' if '✓' in last_ else 'red' if '✗' in last_ else 'black')]+view_history
		print(view_history)
	print('view_history=', view_history)
	if _record_!='':
		view_history = [(_record_, 'black')] + view_history
		updateViewHistory_LP()
def record_update(mode, data):
	global global_record_directory
	# filename = str(datetime.today().strftime("%Y-%m-%d"))+'[][][].txt'
	filename = str(datetime.today().strftime("%Y-%m-%d"))+'.txt'
	if not os.path.exists(global_record_directory+filename):
		with open(global_record_directory+filename, 'w', encoding='utf-8') as file:
			for i in range(9):
				file.writelines('\n')
			file.writelines('# ----- Daily Search Record ----- #\n')
			# data = '#i <BOOK> 第<CHAP>章 第<VERSE>節 @ INDEX'
			file.writelines('\t'+data+'\n')
	else:
		with open(global_record_directory+filename, 'r', encoding='utf-8') as file:
			content = file.readlines()
			with open(global_record_directory+filename, 'w', encoding='utf-8') as rfile:
				if len(content)!=0:
					end_ = (len(content) if mode=='ADD' else len(content)-1) if mode=='COVER-LAST' else len(content)
					for i in content[0:end_]:
						rfile.writelines(i)
				if not '# ----- Daily Search Record ----- #\n' in content:
					rfile.writelines('# ----- Daily Search Record ----- #\n')
				# data = '#i <BOOK> 第<CHAP>章 第<VERSE>節 @ INDEX'
				rfile.writelines('\t'+data+'\n')

def random_script_update(b_file_existence, filename):
	global global_record_directory

	my_new_options = []

	list_ = []
	list_.append('# ----- Daily Random Script ----- #')
	for i in range(4):
		sel = random.choice(listbox_options)
		newbo = sel.bookname
		newch = 0
		sum_ = 0
		for bdr in BDR.list_:
			if bdr.bookname==newbo:
				newch = random.randint(1, sel.chapter)
				break
			else:
				sum_ = sum_ + bdr.chapter
		rand_text = "#%d - %s 第%d章 @ %d" % (i+1, newbo, newch, sum_+newch)
		if global_debug_mode:
			print(rand_text)
		list_.append("%s 第%d章 @ %d" % (newbo, newch, sum_+newch))
		my_new_options.append(rand_text)
	for i in range(4):
		sel = random.choice(listbox_options)
		newbo = sel.bookname
		newch = 0
		sum_ = 0
		for bdr in BDR.list_:
			if bdr.bookname==newbo:
				newch = random.randint(1, sel.chapter)
				break
			else:
				sum_ = sum_ + bdr.chapter
		rand_script = BDR.getScriptContent('https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(newch+sum_)+'&ver=big5&ft=0&temp=-1&tight=0', False)
		newver = random.randint(1, len(rand_script[-1]))
		rand_text = "#%d - %s 第%d章 第%d節 @ %d" % (i+5, newbo, newch, newver, sum_+newch)
		if global_debug_mode:
			print(rand_text)
		list_.append("%s 第%d章 第%d節 @ %d" % (newbo, newch, newver, sum_+newch))
		my_new_options.append(rand_text)
	my_new_options.append("#9 - 隨機經文 -- 1章 @ 1")
	my_new_options.append("#9 - 隨機經文 -- 1節 @ 2")
	my_new_options.append("#9 - 隨機經文 -- 5節 @ 3")
	if b_file_existence:
		with open(global_record_directory+filename, 'r', encoding='utf-8') as file:
			[list_.append(x) for x in [f.replace('\n', '') for f in file.readlines()]]
	with open(global_record_directory+filename, 'w', encoding='utf-8') as file:
		for i in range(len(list_)):
			if i==0 or i>=9:
				file.writelines(list_[i]+'\n')
			else:
				file.writelines('\t'+list_[i]+'\n')
	return my_new_options
def options_update(b_options_update):
	global global_debug_mode
	global global_record_directory
	global option_menu_item_list_var

	my_new_options = []
	if not b_options_update:
		b_options_update = True
	else:
		print('@@ Error : recall -- [options_update]')
		return ;

	# print(os.getcwd())
	filename = str(datetime.today().strftime("%Y-%m-%d"))+'.txt'
	# print(global_record_directory+filename, os.path.exists(global_record_directory+filename))
	if not os.path.exists(global_record_directory+filename):
		my_new_options = random_script_update(False, filename)
	else:
		with open(global_record_directory+filename, 'r', encoding='utf-8') as file:
			data = file.readlines()
			if not '# ----- Daily Random Script ----- #\n' in data:
				my_new_options = random_script_update(True, filename)
			else:
				# print(data, len(data), len(data)==0)
				if len(data)!=0:
					# print(len(data)) --> 9
					tmp = [l.replace('\n', '').replace('\t', '') for l in data[1:9]] ## get 9 data
					for i in range(len(tmp)):
						my_new_options.append('#%d - %s' % (i+1, tmp[i]))
					my_new_options.append("#9 - 隨機經文 -- 1章 @ 1")
					my_new_options.append("#9 - 隨機經文 -- 1節 @ 2")
					my_new_options.append("#9 - 隨機經文 -- 5節 @ 3")
					if global_debug_mode:
						print('<從%r中發現今日經文>' % (global_record_directory+filename))
						for mno in my_new_options:
							print(mno)
				else:
					b_options_update = False
					os.remove(global_record_directory+filename)
					options_update()
	if len(my_new_options)==0:
		print('@@ Error At Adding New Option @@')
		exit()
	option_menu_item_list_var.set(my_new_options[0])
	select_list1["menu"].delete(0, "end")
	for option in my_new_options:
		select_list1["menu"].add_command(label=option, command=lambda value=option: (option_menu_item_list_var.set(value), RandomChapterSelection(value)))
		# select_list1["menu"].add_command(label=option, command=lambda option: (option_menu_item_list_var.set(option), RandomChapterSelection(option_menu_item_list_var.get())))
		# select_list1["menu"].add_command(label=option, command=lambda value=option: option_menu_item_list_var.set(value))
		# select_list1 = tk.OptionMenu(div3, var, *options, command=lambda x: RandomChapterSelection(var.get()))
def RandomChapterSelection(selection):
	global global_debug_mode
	global b_options_update
	global option_menu_options
	global timmer_count_
	global timer_readtime

	if global_debug_mode:
		print(selection)
	if selection=="#0 - 取得今日隨機經文":
		print('['+selection.split(' - ')[-1]+']')
		options_update(b_options_update)
	else:
		print('[#? - <經文>]')
		print('\t擷取經文 '+selection)
		if 1<=int(selection[1]) and int(selection[1])<=4:
			# "#%d - %s 第%d章 @ %d"
			newbo, newch, sum_ = selection.replace('@ ', '').split(' - ')[-1].split(' ')
			if global_debug_mode:
				newch = newch.replace('第', '').replace('章', '')
				print(newbo, newch, sum_)
			try:
				random_script = BDR.getScriptContent('https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(sum_)+'&ver=big5&ft=0&temp=-1&tight=0', False)
			except requests.exceptions.ConnectionError as e:
				print("Error: Could not connect to the website.")
				print("ConnectionError", e)
				traceback.print_exc()
				return ;
			if global_debug_mode:
				print(' --- START --- ', end='')
				BDR.printScript(random_script[0], random_script[1])
				print(' --- END --- ')
			if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
				record_update('ADD', random_script[0]) ## record the searching result
			else:
				if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
					record_update('ADD', random_script[0]) ## record the searching result
				else:
					# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
					# 	record_update('ADD', '%s 第%d章 第%d到%d節'%(global__list_text1, global__list_text2, global__list_text3, global__list_text4)) ## record the searching result
					# else:
					record_update('COVER-LAST', random_script[0]) ## record the searching result
			timmer_count_ = BDR.int_RunTimer()
			displayScript(random_script[0], random_script[1])
		elif 5<=int(selection[1]) and int(selection[1])<=8:
			# "#%d - %s 第%d章 第%d節 @ %d"
			newbo, newch, newver, sum_ = selection.replace('@ ', '').split(' - ')[-1].split(' ')
			if global_debug_mode:
				newch = newch.replace('第', '').replace('章', '')
				newver = newver.replace('第', '').replace('章', '').replace('節', '')
				print(newbo, newch, newver, sum_)
			try:
				random_script = BDR.getScriptContent('https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(sum_)+'&ver=big5&ft=0&temp=-1&tight=0', False)
			except requests.exceptions.ConnectionError as e:
				print("Error: Could not connect to the website.")
				print("ConnectionError", e)
				traceback.print_exc()
				return ;
			if global_debug_mode:
				print(' --- START --- ', end='')
				BDR.printScript(random_script[0], random_script[1])
				print(' --- END --- ')
			if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
				record_update('ADD', random_script[0]+' 第%d節'%int(newver)) ## record the searching result
			else:
				# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
				# 	record_update('ADD', random_script[0]+' 第%d節'%int(newver)) ## record the searching result
				# else:
				record_update('COVER-LAST', random_script[0]+' 第%d節'%int(newver)) ## record the searching result
			timmer_count_ = BDR.int_RunTimer()
			displayScript(random_script[0]+' 第%d節'%int(newver), [random_script[1][int(newver)-1]])
		elif 9==int(selection[1]):
			mode = int(selection.split(' @ ')[-1])
			print(selection, mode)
			if mode==1: # 1 random chapter
				sel = random.choice(listbox_options)
				newbo = sel.bookname
				newch = 0
				sum_ = 0
				for bdr in BDR.list_:
					if bdr.bookname==newbo:
						newch = random.randint(1, sel.chapter)
						break
					else:
						sum_ = sum_ + bdr.chapter
				rand_script = BDR.getScriptContent('https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(newch+sum_)+'&ver=big5&ft=0&temp=-1&tight=0', False)
				if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
					record_update('ADD', '隨機1章經文 ['+rand_script[0]+']') ## record the searching result
				else:
					# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
					# 	record_update('ADD', '隨機1章經文 ['+rand_script[0]+']') ## record the searching result
					# else:
					record_update('COVER-LAST', '隨機1章經文 ['+rand_script[0]+']') ## record the searching result
				timmer_count_ = BDR.int_RunTimer()
				displayScript('隨機1章經文 ['+rand_script[0]+']', rand_script[1])
			elif mode==2: # 1 random verse
				sel = random.choice(listbox_options)
				newbo = sel.bookname
				newch = 0
				sum_ = 0
				for bdr in BDR.list_:
					if bdr.bookname==newbo:
						newch = random.randint(1, sel.chapter)
						break
					else:
						sum_ = sum_ + bdr.chapter
				rand_script = BDR.getScriptContent('https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(newch+sum_)+'&ver=big5&ft=0&temp=-1&tight=0', False)
				newver = random.randint(1, len(rand_script[-1]))
				if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
					record_update('ADD', '隨機1節經文 ['+rand_script[0]+" 第%d節]"%int(newver)) ## record the searching result
				else:
					# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
					# 	record_update('ADD', '隨機1節經文 ['+rand_script[0]+" 第%d節]"%int(newver)) ## record the searching result
					# else:
					record_update('COVER-LAST', '隨機1節經文 ['+rand_script[0]+" 第%d節]"%int(newver)) ## record the searching result
				timmer_count_ = BDR.int_RunTimer()
				displayScript('隨機1節經文 ['+rand_script[0]+" 第%d節]"%int(newver), [rand_script[1][newver-1]])
			elif mode==3: # 5 random verse
				list_ = []
				rere_list = []
				for i in range(5):
					sel = random.choice(listbox_options)
					newbo = sel.bookname
					newch = 0
					sum_ = 0
					for bdr in BDR.list_:
						if bdr.bookname==newbo:
							newch = random.randint(1, sel.chapter)
							break
						else:
							sum_ = sum_ + bdr.chapter
					rand_script = BDR.getScriptContent('https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(newch+sum_)+'&ver=big5&ft=0&temp=-1&tight=0', False)
					newver = random.randint(1, len(rand_script[-1]))
					list_.append('['+rand_script[0]+" 第%d節]"%int(newver))
					rere_list.append('['+rand_script[0]+" 第%d節]"%int(newver))
					list_.append(rand_script[1][newver-1])
					list_.append('\n')
				if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
					record_update('ADD', '隨機5節經文 :: { '+' ,. '.join(rere_list)+' }') ## record the searching result
				else:
					# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
					# 	record_update('ADD', '隨機5節經文 :: { '+' ,. '.join(rere_list)+' }') ## record the searching result
					# else:
					record_update('COVER-LAST', '隨機5節經文 :: { '+' ,. '.join(rere_list)+' }') ## record the searching result
				timmer_count_ = BDR.int_RunTimer()
				displayScript('隨機5節經文', list_)
		else:
			print('not develop yet')

def switch_script(cmd):
	global global__list_text1
	global global__list_text2
	global global_cur_script
	global timmer_count_
	global timer_readtime

	tag = ''
	window.title('靈修輔助工具 v2'+' --- 查找 %s 第%d章 的%r一章'%(global__list_text1, global__list_text2, str('前' if cmd=='previous' else '後')))
	if cmd=='previous':
		global__list_text2 = int(global__list_text2)-1
		sum_ = 0
		pre = None
		cur = None
		for bdr in BDR.list_:
			if cur==None:
				cur = bdr
			else:
				sum_ = sum_ + cur.chapter
				pre = cur
				cur = bdr
			if cur.bookname==global__list_text1:
				break
		if pre==None: # global__list_text1 is the first book
			if global__list_text2<1: ## want previous book, but there is no previous
				print('ERROR :: no previous book found')
				tag = '[FIRST]'
				global__list_text2 = int(global__list_text2)+1 ## back to the first book first chapter
		else: # global__list_text1 is not the first book
			if global__list_text2<1: ## want previous book
				global__list_text1 = pre.bookname
				global__list_text2 = pre.chapter
				sum_ = sum_ - pre.chapter
			## want previous chapter, same book --> nothing to change
	elif cmd=='next':
		global__list_text2 = int(global__list_text2)+1
		sum_ = 0
		bash = 0
		pre = None
		cur = None
		for bdr in BDR.list_:
			if pre==None:
				pre = bdr
				continue;
			sum_ = sum_ + pre.chapter
			if pre.bookname==global__list_text1:
				cur = bdr
				bash = cur.chapter
				break
			pre = bdr
		if cur==None: # global__list_text1 is the last book
			if global__list_text2>pre.chapter: ## want next, but there is no next
				print('ERROR :: no next book found')
				tag = '[LAST]'
				global__list_text2 = int(global__list_text2)-1 ## back to the last book last chapter
		else: # global__list_text1 is not the last book
			if global__list_text2>pre.chapter: ## want next book
				global__list_text1 = cur.bookname
				global__list_text2 = global__list_text2 - pre.chapter
				sum_ = sum_
			else: ## want next chapter, same book
				global__list_text2 = global__list_text2
				sum_ = sum_ - pre.chapter
	# try:
	print('[查找 %s 第%d章]' % (global__list_text1, global__list_text2))
	try:
		global_cur_script = BDR.getScriptContent('https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(global__list_text2+sum_)+'&ver=big5&ft=0&temp=-1&tight=0', False)
	except requests.exceptions.ConnectionError as e:
		print("Error: Could not connect to the website.")
		print("ConnectionError", e)
		traceback.print_exc()
		return ;
	if global_debug_mode:
		print(' --- START --- ', end='')
		BDR.printScript(global_cur_script[0], global_cur_script[1])
		print(' --- END --- ')
	if timmer_count_ == -707:
		record_update('ADD', global_cur_script[0]) ## record the searching result
		UpdateHistory('ADD', ['?']+[[global__list_text1, global__list_text2]]) ## record the searching result
	else:
		if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
			record_update('ADD', global_cur_script[0])
			UpdateHistory('ADD', ['?']+[[global__list_text1, global__list_text2]])
		else:
			if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
				record_update('ADD', global_cur_script[0])
				UpdateHistory('ADD', ['?']+[[global__list_text1, global__list_text2]])
			else:
				record_update('COVER-LAST', global_cur_script[0])
				UpdateHistory('COVER-LAST', ['?']+[[global__list_text1, global__list_text2]])
	timmer_count_ = BDR.int_RunTimer()
	displayScript(global_cur_script[0]+'  '+tag, global_cur_script[1])
	# except:
	# 	print('', end='')
	# 	return ;


## next update
## 1. a button for 'global_debug_mode' on/off
## 2. a slection_box for style of text in textbox
## 3. provide daily random script * 4
## 4. record the searching result for daily management


## init
global_debug_mode = True
result = tkm.askyesno("Alert", "This Program Now Is Intended For Searching Bible Script.\nThe Textbox Do Not Suport Saving Function !!\n(y):got it, continue\t(n):got it, leave")
if not result:
	exit()
window = tk.Tk()
window.title('靈修輔助工具 v2 -- '+datetime.today().strftime('%Y/%m/%d'))
align_mode = 'nswe'
pad = 5
div_size = 200  ## table-sets
window.geometry("950x750")

## variables
global_record_directory = 'ｒｅｃｏｒｄｓ\\'
global_note_directory = '靈修存檔\\'
# global_record_directory = 'records\\' ##'ｒｅｃｏｒｄｓ\\'
global_is_editable = tk.BooleanVar()
global_is_editable.set(False) ## init -- not editable
global_word_content = tk.StringVar()
listbox_options = BDR.list_
global__list_text1 = ''
global__list_text2 = ''
global__list_text3 = ''
global__list_text4 = ''
global_cur_script = [] ## [title<str>, data<arr>]
BibleTitle_Text = tk.StringVar()

b_options_update = False
option_menu_options = ["#0 - 取得今日隨機經文"] # + options_update(b_options_update) ## failed to load in the init
# print(options)
option_menu_item_list_var = tk.StringVar(value="Select an option")
option_menu_item_list_var.set(option_menu_options[0])

timmer_count_ = -707
timer_readtime = 90 #/90*5  ## readtime -- 90 seconds
# im = cv2.imread('pic.png')
# h, w, co = im.shape
# co = hcf(h,w)
# print(h, w, co)
# ans = 10 if co==1 else co
# img_size = div_size * 2
# img_h = int(div_size * h/ans)
# img_w = int(div_size * w/ans)
# img_size = div_size * 2
# div1 = tk.Frame(window,  width=img_size , height=img_size , bg='blue')
div1 = tk.Frame(window,  width=div_size , height=div_size , bg='blue')
# div1 = tk.Frame(window,  width=img_w , height=img_h , bg='blue')
div2 = tk.Frame(window,  width=div_size , height=div_size , bg='yellow')
div3 = tk.Frame(window,  width=div_size , height=div_size , bg='green')
div4 = tk.Frame(window,  width=div_size , height=div_size , bg='purple')
div1_toolpack = tk.Frame(div1,  width=div_size , height=div_size , bg='gray')

window.update()
win_size = min( window.winfo_width(), window.winfo_height())
# print(win_size)

div1.grid(column=0, row=0, padx=pad, pady=pad, rowspan=2, sticky=align_mode)
div2.grid(column=1, row=0, padx=pad, pady=pad, sticky=align_mode)
div3.grid(column=1, row=1, padx=pad, pady=pad, sticky=align_mode)
div4.grid(column=0, row=2, padx=pad, pady=pad, columnspan=2, sticky=align_mode)
div1_toolpack.grid(column=2, row=2, padx=pad, pady=pad, columnspan=2, sticky=align_mode)

define_layout(window, cols=2, rows=2)
define_layout([div1, div2, div3, div4, div1_toolpack])

## new add
window.columnconfigure(0, weight=70)
window.columnconfigure(1, weight=80)
window.columnconfigure(2, weight=0)
window.columnconfigure(3, weight=0)
# window.rowconfigure(2, weight=10)
# window.rowconfigure(3, weight=1)
# window.columnconfigure(0, weight=4)
# window.columnconfigure(1, weight=2)
# window.columnconfigure(2, weight=1)
# window.columnconfigure(3, weight=1)
# window.columnconfigure(4, weight=0)


## items
# im = Image.open('pic.png')
# imTK = ImageTk.PhotoImage( im.resize( (img_size, img_size) ) )

# image_main = tk.Label(div1, image=imTK)
# image_main['height'] = img_size
# image_main['width'] = img_size

# image_main.grid(column=0, row=0, sticky=align_mode)

# lbl_title1 = tk.Label(div2, text='Hello', bg='orange', fg='white')
# lbl_title2 = tk.Label(div2, text="World", bg='orange', fg='white')
lbl_quote = tk.Label(div4, textvariable=BibleTitle_Text, bg='#E7A10A', fg='#70FA0A', font=("微軟黑正體", 14, "bold"))
lbl_random_title = tk.Label(div3, text="每日經文", height=3, bg='green', fg='white', font=("微軟黑正體", MenuElement__fontsize_array[MenuElement__fontsize_array_index], "italic underline"))  # "bold italic underline overstrike"
previous_script = tk.Button(div4, text='Previous Script', bg='blue', fg='white', command=lambda: switch_script('previous'))
next_script = tk.Button(div4, text='Next Script', bg='blue', fg='white', command=lambda: switch_script('next'))

# lbl_title1.grid(column=0, row=0, sticky=align_mode)
# lbl_title2.grid(column=0, row=1, sticky=align_mode)
lbl_quote.grid(column=1, row=0, sticky=align_mode)
lbl_random_title.grid(column=0, columnspan=2, row=1, sticky=align_mode)
previous_script.grid(column=0, row=0, sticky=align_mode)
next_script.grid(column=2, row=0, sticky=align_mode)

# bt1 = tk.Button(div3, text='Button 1', bg='green', fg='white')
# bt2 = tk.Button(div3, text='Button 2', bg='green', fg='white')
# bt3 = tk.Button(div3, text='Button 3', bg='green', fg='white')
# bt4 = tk.Button(div3, text='Button 4', bg='green', fg='white')

# bt1.grid(column=0, row=0, sticky=align_mode)
# bt2.grid(column=0, row=1, sticky=align_mode)
# bt3.grid(column=0, row=2, sticky=align_mode)
# bt4.grid(column=0, row=3, sticky=align_mode)

checkbox1 = tk.Checkbutton(div4, text="Edit Text", variable=global_is_editable)
checkbox1.grid(column=4, row=0, sticky=align_mode)
# checkbox1.state(("disabled",)) ## for ttk.Checkbutton
checkbox1.configure(state=tk.DISABLED)

BibleContent_Text = tk.Text(div4, font=("Times New Roman", Content__fontsize_array[Content__fontsize_array_index]), wrap='word')
BibleContent_Text_scrollbar = tk.Scrollbar(div4)

BibleContent_Text.config(yscrollcommand=BibleContent_Text_scrollbar.set) ## 設定讀條(scrolling-bar)調比例與內容相同
BibleContent_Text_scrollbar.config(command=BibleContent_Text.yview) ## 設定讀條(scrolling-bar)可以做用在textbox上
BibleContent_Text.grid(column=0, row=1, columnspan=4, sticky=align_mode)
BibleContent_Text_scrollbar.grid(column=4, row=1, columnspan=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
select_list1 = tk.OptionMenu(div3, option_menu_item_list_var, *option_menu_options, command=lambda x: RandomChapterSelection(option_menu_item_list_var.get()))
select_list1.config(width=45)
select_list1.config(height=3)
select_list1.config(font=("微軟黑正體", MenuElement__fontsize_array[MenuElement__fontsize_array_index]))
select_list1.grid(column=0, row=2, columnspan=2, sticky=align_mode)


## Searching Bar
def OnBookSearch(book_search_entry, searching_text_var, reason):
	global bookname_choices
	filtered_books = []
	[print("Entry value changed:%r"%x) for x in searching_text_var.get()]
	searching_text = searching_text_var.get()
	if searching_text!='':
		filtered_books = [book for book in bookname_choices if searching_text in book]
	else:
		filtered_books = bookname_choices
	print('SEARCH REASULT:', filtered_books)
	bookname__LP1.delete(0, "end")
	for filtered_book in filtered_books:
		bookname__LP1.insert("end", filtered_book)
	if filtered_books:
		book_search_entry.config(foreground="dark orange2", font=(default_font, MenuElement__fontsize_array[MenuElement__fontsize_array_index], "bold"))
	else:
		book_search_entry.config(foreground="red", font=(default_font, MenuElement__fontsize_array[MenuElement__fontsize_array_index], "normal"))
## Create a custom style for the Entry widget
style = tk.ttk.Style()
style.configure("Better.TEntry", foreground="gray", font=("Helvetica", 12))
## Main Assume
# searching_text = tk.StringVar(value='Input Book Name...')
searching_text = tk.StringVar(value='搜尋..')
book_search_entry = tk.ttk.Entry(div1, style="Better.TEntry", textvariable=searching_text)
book_search_entry.grid(row=0, column=0, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
searching_text.trace_add("write", lambda *args: OnBookSearch(book_search_entry, searching_text, "write"))

# bookname_choices = [booknames_ch[index]+'    '+booknames_en[index] for index in range(len(booknames_ch))]
bookname_choices = [name.bookname for name in BDR.list_]
bookname__LP1 = tk.Listbox(div1, listvariable=tk.StringVar(value=bookname_choices), width=16)
bookname__LP1.grid(row=1, column=0, rowspan=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
global__chapter_num_choice = [-1]
chapter_num__LP2 = tk.Listbox(div1, listvariable=tk.StringVar(value=global__chapter_num_choice), width=17)
chapter_num__LP2.grid(row=1, column=1, rowspan=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)


## newly edit
# '✓' '✘' '✗' '▪️'
view_history = []
view_history_LP = tk.Listbox(div2, listvariable=tk.StringVar(value=view_history), width=16)
view_history_LP.grid(row=0, column=0, rowspan=2, padx=int(pad/2), pady=int(pad/2), sticky=tk.E+tk.W+tk.N+tk.S)
## add new button with different function
style = tk.ttk.Style()
## Define a custom style
style.configure("Square.TButton", font=("Arial", 14), width=4, height=5)
Del_History_btn = tk.ttk.Button(div2, text="DEL", style="Square.TButton", command=Del_History)
Del_History_btn.grid(row=0, column=1, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
Finish_History_btn = tk.ttk.Button(div2, text="DONE", style="Square.TButton", command=Finish_History)
Finish_History_btn.grid(row=1, column=1, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)


# Create a Combobox widget
# verse_num__Com3 = tk_combo.Combobox(div1, values=["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"])
global__verse_num_choice_S = [-1]
verse_num__Com3 = tk.ttk.Combobox(div1, values=global__verse_num_choice_S, width=15)
verse_num__Com3.grid(row=1, column=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
# Set an initial value
# verse_num__Com3.set("Select Start Verse")
verse_num__Com3.set("開始小節")

# verse_num__Com4 = tk_combo.Combobox(div1, values=["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"])
global__verse_num_choice_E = [-1]
verse_num__Com4 = tk.ttk.Combobox(div1, values=global__verse_num_choice_E, width=15)
# verse_num__Com4.grid(row=2, column=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
verse_num__Com4.grid(row=1, column=3, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
# verse_num__Com4.set("Select End Verse")
verse_num__Com4.set("結束小節")

# global__verse_num_choice_S = [-1]
# verse_num__LP3 = tk.Listbox(div1, listvariable=tk.StringVar(value=global__verse_num_choice_S))
# verse_num__LP3.grid(row=1, column=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
# global__verse_num_choice_E = [-1]
# verse_num__LP4 = tk.Listbox(div1, listvariable=tk.StringVar(value=global__verse_num_choice_E))
# verse_num__LP4.grid(row=2, column=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)


## add new button with different function
style = tk.ttk.Style()
## Define a custom style
style.configure("Square.TButton", font=("Arial", 16), width=4, height=5)
BibleTitle__fontsize_add_button = tk.ttk.Button(div1_toolpack, text="+", style="Square.TButton", command=BibleTitle__font_size_increase)
BibleTitle__fontsize_add_button.grid(row=1, column=1, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
BibleTitle__fontsize_minus_button = tk.ttk.Button(div1_toolpack, text="-", style="Square.TButton", command=BibleTitle__font_size_decrease)
BibleTitle__fontsize_minus_button.grid(row=1, column=2, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)


BibleContent__fontsize_add_button = tk.ttk.Button(div1_toolpack, text="+", style="Square.TButton", command=BibleContent__font_size_increase)
BibleContent__fontsize_add_button.grid(row=2, column=1, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
BibleContent__fontsize_minus_button = tk.ttk.Button(div1_toolpack, text="-", style="Square.TButton", command=BibleContent__font_size_decrease)
BibleContent__fontsize_minus_button.grid(row=2, column=2, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)

global_font_usable_list = checkFontusale([
	'Arial', 
	'Times New Roman', 
	'Calibri', 
	'Segoe UI', 
	'Verdana', 
	'SimSun', 
	'Microsoft YaHei', 
	'KaiTi', 
	'FangSong', 
	'SimHei', 
	'NSimSun', 
	'WenQuanYi Zen Hei', 
	'Noto Sans CJK', 
	'AR PL ZenKai Uni', 
	'AR PL KaitiM Uni', 
	'Droid Sans Fallback'
])
newFont__Com = tk.ttk.Combobox(div1_toolpack, width=10, height=5, values=global_font_usable_list)
newFont__Com.grid(row=1, column=3, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
newFont__Com.set("可用字體") # (若為空白，則不支援其他預設)")

global_theme = ['Default']
newTheme__Com = tk.ttk.Combobox(div1_toolpack, width=10, height=5, values=global_theme)
newTheme__Com.grid(row=1, column=4, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
newTheme__Com.set("主題顏色")


sub_window = None
sub_window1 = None
open_sub_window_button1 = tk.Button(div1_toolpack, text="<開啟>\n靈修筆記區", command=open_sub_window_1)
# open_sub_window_button.pack(padx=20, pady=10)
open_sub_window_button1.grid(row=2, column=3, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
sub_window2 = None
open_sub_window_button2 = tk.Button(div1_toolpack, text="<開啟>\n歸納式查經", command=open_sub_window_2)
open_sub_window_button2.grid(row=2, column=4, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)


div1.rowconfigure(0, weight=1)
div1.rowconfigure(1, weight=5)
div1.rowconfigure(2, weight=15)
div1.rowconfigure(3, weight=1)
div1.columnconfigure(0, weight=8)
div1.columnconfigure(1, weight=4)
div1.columnconfigure(2, weight=1)
div1.columnconfigure(3, weight=1)
div1.columnconfigure(4, weight=0)

div3.rowconfigure(0, weight=0)
div3.rowconfigure(1, weight=0)
div3.rowconfigure(2, weight=0)
div3.columnconfigure(0, weight=1)
div3.columnconfigure(1, weight=1)
div3.columnconfigure(2, weight=0)

div4.columnconfigure(0, weight=1)
div4.columnconfigure(1, weight=50)
div4.columnconfigure(2, weight=1)
div4.columnconfigure(3, weight=0)
div4.columnconfigure(4, weight=0)

div1_toolpack.rowconfigure(0, weight=0)
div1_toolpack.rowconfigure(1, weight=1)
div1_toolpack.rowconfigure(2, weight=1)
div1_toolpack.rowconfigure(3, weight=0)
div1_toolpack.columnconfigure(0, weight=0)
div1_toolpack.columnconfigure(1, weight=1)
div1_toolpack.columnconfigure(2, weight=1)
div1_toolpack.columnconfigure(3, weight=4)
div1_toolpack.columnconfigure(4, weight=4)
div1_toolpack.columnconfigure(5, weight=0)

## usage
BibleTitle_Text.set("[ 聖經查找 ]")
# bt1['command'] = lambda : get_size(window, image_main, im)
checkbox1['command'] = lambda: TextBoxStatusChanging(global_is_editable)
# select_list1['command'] = lambda: selection(var.get())
# listbox1.bind('<<ListboxSelect>>', lambda event: ChapterSelection1(1, event.widget.get(event.widget.curselection())))
# listbox2.bind('<<ListboxSelect>>', lambda event: ChapterSelection2(2, event.widget.get(event.widget.curselection())))
bookname__LP1.bind("<<ListboxSelect>>", List1_Select)
# chapter_num__LP2.bind("<<ListboxSelect>>", List2_Select)
chapter_num__LP2.bind("<ButtonRelease-1>", List2_Select)
# view_history_LP.bind("<<ListboxSelect>>", LoadHistory)
view_history_LP.bind("<ButtonRelease-1>", LoadHistory)

## newly edit
# Bind the selection event to the on_item_selected function
verse_num__Com3.bind("<<ComboboxSelected>>", Verse_Combo3)
verse_num__Com4.bind("<<ComboboxSelected>>", Verse_Combo4)
newFont__Com.bind("<<ComboboxSelected>>", ChangeFont)
newTheme__Com.bind("<<ComboboxSelected>>", ChangeTheme)

# verse_num__LP3.bind("<<ListboxSelect>>", List3_Select)
# verse_num__LP4.bind("<<ListboxSelect>>", List4_Select)

## layout management
define_layout(window, cols=2, rows=2)
define_layout(div1)
define_layout(div2, rows=2)
define_layout(div3, rows=4)
define_layout(div4, rows=4)

def on_closing():
	global timmer_count_
	global timer_readtime
	# if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
	if BDR.int_RunTimer() - timmer_count_ > timer_readtime or timmer_count_==-707:
		window.destroy()
	else:
		if tk.messagebox.askokcancel("Notice !!", "The Reading Time Of Last Script You Found Did Not More Than \'ReadTime = {timer_readtime}s\'.\nLeaving Will Make The Record Be Deleted...\nSure To Leave ?"):
			record_update('COVER-LAST', '')
			window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()






## information
# https://www.rs-online.com/designspark/python-tkinter-cn#_Toc61529916

