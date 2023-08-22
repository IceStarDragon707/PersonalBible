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


##### ------------------------- next update : astract ------------------------- #####


class Theme:
	colors = [] ## different color including: 'BibleContent', 'BibleTitle', 'div', 'button', ...
	def __init__(color_panel):
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
		selection_index_LB1 = event.widget.curselection()[0]
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
			else:
				if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
					record_update('ADD', global_cur_script[0]) ## record the searching result
				else:
					# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
					# 	record_update('ADD', global_cur_script[0]) ## record the searching result
					# else:
					record_update('COVER-LAST', global_cur_script[0]) ## record the searching result
			timmer_count_ = BDR.int_RunTimer()
			displayScript(global_cur_script[0], global_cur_script[1])
	except:
		print('', end='')
		return ;
	
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
def List3_Select(event):
	global global__list_text3
	global global_debug_mode
	global timmer_count_
	global timer_readtime

	try: ## because when selecting over another ListBox, will cause and out-of-range error
		selection_index_LB3 = event.widget.curselection()[0]
		global__list_text3 = selection_index_LB3+1
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
		else:
			if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
				record_update('ADD', '%s 第%d章 第%d節 開始'%(global__list_text1, global__list_text2, global__list_text3))
			else:
				# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
				# 	record_update('ADD', '%s 第%d章 第%d到%d節'%(global__list_text1, global__list_text2, global__list_text3, global__list_text4)) ## record the searching result
				# else:
				record_update('COVER-LAST', '%s 第%d章 第%d節 開始'%(global__list_text1, global__list_text2, global__list_text3))
		displayScript('%s 第%d章 第%d節 開始'%(global__list_text1, global__list_text2, global__list_text3), global_cur_script[1][global__list_text3-1::])
	except:
		print('', end='')
		return ;
def List4_Select(event):
	global global__list_text1, global__list_text2, global__list_text3,  global__list_text4
	global global_debug_mode
	global timmer_count_
	global timer_readtime

	try: ## because when selecting over another ListBox, will cause and out-of-range error
		selection_index_LB4 = event.widget.curselection()[0]
		global__list_text4 = selection_index_LB4+1
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
		else:
			# if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
			# 	record_update('ADD', '%s 第%d章 第%d到%d節'%(global__list_text1, global__list_text2, global__list_text3, global__list_text4)) ## record the searching result
			# else:
			record_update('COVER-LAST', '%s 第%d章 第%d到%d節'%(global__list_text1, global__list_text2, global__list_text3, global__list_text4)) ## record the searching result
		timmer_count_ = BDR.int_RunTimer()
		displayScript('%s 第%d章 第%d到%d節'%(global__list_text1, global__list_text2, global__list_text3, global__list_text4), global_cur_script[1][global__list_text3-1:global__list_text4])
	except:
		print('', end='')
		return ;

## new edit
def Verse_Combo3(event):
	selected_item = verse_num__Com3.get()
	print("Selected:", selected_item)
def Verse_Combo4(event):
	selected_item = verse_num__Com4.get()
	print("Selected:", selected_item)
font_array_index = 0
font_array = [12, 14, 16, 18, 20]
default_font = "TkDefaultFont"
def BibleContent__font_size_increase():
	global font_array_index
	global font_array
	global default_font
	tmp_font_array_index = font_array_index + 1
	if tmp_font_array_index>=len(font_array):
		result = tkm.askyesno("提示~", "字體最大 = %d"%font_array[font_array_index])
		font_array_index = len(font_array) - 1
	else:
		font_array_index = tmp_font_array_index
	print('Change Text Font-Size To %d' % font_array[font_array_index])
	font_style = (default_font, font_array[font_array_index])
	BibleContent_Text.tag_configure("custom_font", font=font_style)
	BibleContent_Text.tag_add("custom_font", "1.0", tk.END)
def BibleContent__font_size_decrease():
	global font_array_index
	global font_array
	global default_font
	tmp_font_array_index = font_array_index - 1
	if tmp_font_array_index<0:
		result = tkm.askyesno("提示~", "字體最小 = %d"%font_array[font_array_index])
		font_array_index = 0
	else:
		font_array_index = tmp_font_array_index
	print('Change Text Font-Size To %d' % font_array[font_array_index])
	font_style = (default_font, font_array[font_array_index])
	BibleContent_Text.tag_configure("custom_font", font=font_style)
	BibleContent_Text.tag_add("custom_font", "1.0", tk.END)
Title__font_array_index = 0
Title__font_array = [16, 18, 20, 22, 24, 26, 28, 30, 32]
def BibleTitle__font_size_increase():
	global default_font
	global Title__font_array_index
	global Title__font_array
	tmp_font_array_index = Title__font_array_index + 1
	if tmp_font_array_index>=len(Title__font_array):
		result = tkm.askyesno("提示~", "字體最大 = %d"%Title__font_array[Title__font_array_index])
		Title__font_array_index = len(Title__font_array) - 1
	else:
		Title__font_array_index = tmp_font_array_index
	print('Change Title Text Font-Size To %d' % Title__font_array[Title__font_array_index])
	lbl_quote.config(font=(default_font, Title__font_array[Title__font_array_index]))
def BibleTitle__font_size_decrease():
	global default_font
	global Title__font_array_index
	global Title__font_array
	tmp_font_array_index = Title__font_array_index - 1
	if tmp_font_array_index<0:
		result = tkm.askyesno("提示~", "字體最小 = %d"%Title__font_array[Title__font_array_index])
		Title__font_array_index = 0
	else:
		Title__font_array_index = tmp_font_array_index
	print('Change Title Text Font-Size To %d' % Title__font_array[Title__font_array_index])
	lbl_quote.config(font=(default_font, Title__font_array[Title__font_array_index]))
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
	global font_array_index
	global font_array
	global default_font
	tmp_default_font = newFont__Com.get()
	if tmp_default_font:
		default_font = tmp_default_font
		print('Change Text Font To %r' % newFont__Com.get())
		font_style = (default_font, font_array[font_array_index])
		BibleContent_Text.tag_configure("custom_font", font=font_style)
		BibleContent_Text.tag_add("custom_font", "1.0", tk.END)
		lbl_quote.config(font=(default_font, Title__font_array[Title__font_array_index]))
def ChangeTheme(event):
	tmp_default_font = newTheme__Com.get()
	## change color ##


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
	else:
		if BDR.int_RunTimer() - timmer_count_ > timer_readtime:
			record_update('ADD', global_cur_script[0])
		else:
			if tkm.askyesno('[CHECK]', 'Have You Finished Reading This Chapter ?'):
				record_update('ADD', global_cur_script[0])
			else:
				record_update('COVER-LAST', global_cur_script[0])
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
lbl_random_title = tk.Label(div3, text="每日經文", bg='green', fg='white', font=("微軟黑正體", 10, "italic underline"))  # "bold italic underline overstrike"
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

BibleContent_Text = tk.Text(div4, font=("Times New Roman", font_array[font_array_index]), wrap='word')
BibleContent_Text_scrollbar = tk.Scrollbar(div4)

BibleContent_Text.config(yscrollcommand=BibleContent_Text_scrollbar.set) ## 設定讀條(scrolling-bar)調比例與內容相同
BibleContent_Text_scrollbar.config(command=BibleContent_Text.yview) ## 設定讀條(scrolling-bar)可以做用在textbox上
BibleContent_Text.grid(column=0, row=1, columnspan=4, sticky=align_mode)
BibleContent_Text_scrollbar.grid(column=4, row=1, columnspan=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)

select_list1 = tk.OptionMenu(div3, option_menu_item_list_var, *option_menu_options, command=lambda x: RandomChapterSelection(option_menu_item_list_var.get()))
select_list1.grid(column=0, row=2, columnspan=2, sticky=align_mode)


## Searching Bar
# initial_text = tk.StringVar(value='Input Text For Book Searching...')
# book_search_text = tk.Entry(div1, textvariable=initial_text)
# book_search_text.grid(row=0, column=0, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)

# bookname_choices = [booknames_ch[index]+'    '+booknames_en[index] for index in range(len(booknames_ch))]
bookname_choices = [name.bookname for name in BDR.list_]
bookname__LP1 = tk.Listbox(div1, listvariable=tk.StringVar(value=bookname_choices))
bookname__LP1.grid(row=1, column=0, rowspan=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
global__chapter_num_choice = [-1]
chapter_num__LP2 = tk.Listbox(div1, listvariable=tk.StringVar(value=global__chapter_num_choice))
chapter_num__LP2.grid(row=1, column=1, rowspan=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)

## newly edit
# Create a Combobox widget
# verse_num__Com3 = tk_combo.Combobox(div1, values=["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"])
global__verse_num_choice_S = [-1]
verse_num__Com3 = tk.ttk.Combobox(div1, values=global__verse_num_choice_S)
verse_num__Com3.grid(row=1, column=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
# Set an initial value
verse_num__Com3.set("Select Start Verse")

# verse_num__Com4 = tk_combo.Combobox(div1, values=["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"])
global__verse_num_choice_E = [-1]
verse_num__Com4 = tk.ttk.Combobox(div1, values=global__verse_num_choice_E)
# verse_num__Com4.grid(row=2, column=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
verse_num__Com4.grid(row=1, column=3, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
verse_num__Com4.set("Select End Verse")

# global__verse_num_choice_S = [-1]
# verse_num__LP3 = tk.Listbox(div1, listvariable=tk.StringVar(value=global__verse_num_choice_S))
# verse_num__LP3.grid(row=1, column=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
# global__verse_num_choice_E = [-1]
# verse_num__LP4 = tk.Listbox(div1, listvariable=tk.StringVar(value=global__verse_num_choice_E))
# verse_num__LP4.grid(row=2, column=2, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)


## add new button with different function
style = tk.ttk.Style()
## Define a custom style
style.configure("Square.TButton", font=("Arial", 16), width=5, height=5)
BibleTitle__fontsize_add_button = tk.ttk.Button(div1_toolpack, text="+", style="Square.TButton", command=BibleTitle__font_size_increase)
BibleTitle__fontsize_add_button.grid(row=1, column=1, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
BibleTitle__fontsize_minus_button = tk.ttk.Button(div1_toolpack, text="-", style="Square.TButton", command=BibleTitle__font_size_decrease)
BibleTitle__fontsize_minus_button.grid(row=1, column=2, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)


BibleContent__fontsize_add_button = tk.ttk.Button(div1_toolpack, text="+", style="Square.TButton", command=BibleContent__font_size_increase)
BibleContent__fontsize_add_button.grid(row=2, column=1, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
BibleContent__fontsize_minus_button = tk.ttk.Button(div1_toolpack, text="-", style="Square.TButton", command=BibleContent__font_size_decrease)
BibleContent__fontsize_minus_button.grid(row=2, column=2, ipadx=int(pad/2), padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)

global_font_usable = checkFontusale([
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
newFont__Com = tk.ttk.Combobox(div1_toolpack, width=10, height=5, values=global_font_usable)
newFont__Com.grid(row=1, column=3, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
newFont__Com.set("可用字體") # (若為空白，則不支援其他預設)")

global_theme = ['Default']
newTheme__Com = tk.ttk.Combobox(div1_toolpack, width=10, height=5, values=global_theme)
newTheme__Com.grid(row=1, column=4, padx=pad, pady=pad, sticky=tk.E+tk.W+tk.N+tk.S)
newTheme__Com.set("選用顏色主題")



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
chapter_num__LP2.bind("<<ListboxSelect>>", List2_Select)

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

