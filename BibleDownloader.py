import random
import time


class Book:
	chaptername = ''
	verse = 0
	def __init__(self, chaptername, verse):
		self.chaptername = chaptername
		self.verse = verse
	def max(self):
		return self.verse
	def name(self):
		return self.chaptername
	def all(self):
		return [self.chaptername, self.verse]


list_ = []
Genesis, Exodus, Leviticus, Numbers = Book('創世紀', 50), Book('出埃及記', 40), Book('利未記', 27), Book('民數記', 36)
Deuteronomy, Joshua, Judges, Ruth = Book('申命記', 34), Book('約書亞記', 24), Book('士師記', 21), Book('路得記', 4)
Samuel_1, Samuel_2, Kings_1, Kings_2 = Book('撒母耳記上', 31), Book('撒母耳記下', 24), Book('列王紀上', 22), Book('列王紀下', 25)
Chronicles_1, Chronicles_2, Ezra, Nehemiah = Book('歷代志上', 29), Book('歷代志下', 36), Book('以斯拉記', 10), Book('尼希米記', 13)
Esther,Job,Psalms,Proverbs, Ecclesiastes = Book('以斯帖記', 10), Book('約伯記', 42), Book('詩篇', 150), Book('箴言', 31), Book('傳道書', 12)
Song_of_Songs, Isaiah, Jeremiah, Lamentations = Book('雅歌', 8), Book('以賽亞書', 66), Book('耶利米書', 52), Book('耶利米哀歌', 5)
Ezekiel, Daniel, Hosea, Joel, Amos = Book('以西結書', 48), Book('但以理書', 12), Book('何西阿書', 14), Book('約珥書', 3), Book('阿摩司書', 9)
Obadiah, Jonah, Micah, Nahum, Habakkuk = Book('俄巴底亞書', 1), Book('約拿書', 4), Book('彌迦書', 7), Book('那鴻書', 3), Book('哈巴谷書', 3)
Zephaniah, Haggai, Zechariah, Malachi = Book('西番雅書', 3), Book('哈該書', 2), Book('撒迦利亞書', 14), Book('瑪拉基書', 4)
Matthew, Mark, Luke, John = Book('馬太福音', 28), Book('馬可福音', 16), Book('路加福音', 24), Book('約翰福音', 21)
Acts, Romans, Corinthians_1, Corinthians_2 = Book('使徒行傳', 28), Book('羅馬書', 16), Book('哥林多前書', 16), Book('哥林多後書', 13)
Galatians, Ephesians, Philippians, Colossians = Book('加拉太書', 6), Book('以弗所書', 6), Book('腓立比書', 4), Book('歌羅西書', 4)
Thessalonians_1, Thessalonians_2, Timothy_1, Timothy_2 = Book('帖撒羅尼迦前書', 5), Book('帖撒羅尼迦後書', 3), Book('提摩太前書', 6), Book('提摩太後書', 4)
Titus, Philemon, Hebrews, James = Book('提多書', 3), Book('腓利門書', 1), Book('希伯來書', 13), Book('雅各書', 5)
Peter_1, Peter_2, John_1, John_2, John_3 = Book('彼得前書', 5), Book('彼得後書', 3), Book('約翰壹書', 5), Book('約翰貳書', 1), Book('約翰參書', 1)
Jude, Revelation = Book('猶大書', 1), Book('啟示錄', 22)
a = [Genesis, Exodus, Leviticus, Numbers] + [Deuteronomy, Joshua, Judges, Ruth] + [Samuel_1, Samuel_2, Kings_1, Kings_2]
b = [Chronicles_1, Chronicles_2, Ezra, Nehemiah] + [Esther,Job,Psalms,Proverbs, Ecclesiastes] + [Song_of_Songs, Isaiah, Jeremiah, Lamentations]
c = [Ezekiel, Daniel, Hosea, Joel, Amos] + [Obadiah, Jonah, Micah, Nahum, Habakkuk] + [Zephaniah, Haggai, Zechariah, Malachi]
d = [Matthew, Mark, Luke, John] + [Acts, Romans, Corinthians_1, Corinthians_2] + [Galatians, Ephesians, Philippians, Colossians]
e = [Thessalonians_1, Thessalonians_2, Timothy_1, Timothy_2] + [Titus, Philemon, Hebrews, James] + [Peter_1, Peter_2, John_1, John_2, John_3]
f = [Jude, Revelation]
list_ = a+b+c+d+e+f
tab = ''

def str_GetHTML(url):
	from bs4 import BeautifulSoup
	import requests
	html = BeautifulSoup(requests.get(url).content, 'html.parser');
	return html
def TextStyleChanger():
	textSize = '24px'
	return -1
def printScript(title, data):
	global tab
	print('\n\t\t\t'+tab+title)
	for d in data:
		print(tab+d)
def getScriptContent(url, print_):
	if url=='':
		url = input('輸入聖經網址 -->')
	# data = [[x.get('value'), x.getText()] for x in str_GetHTML(url).find_all('li')]
	html = str_GetHTML(url)
	data = [str(x.get('value'))+'. '+str(x.getText()).replace('\n', '') for x in html.find_all('li')]
	title = [str(x.getText()).replace('\n', '') for x in str_GetHTML(url).find_all('font')][0]
	if print_:
		printScript(title, data)
	return [title, data]
def ExprotBibleChapter(chapter, font, text_size):
	return -1
def MakeAllBible():
	name = '-1'
	datapack = []
	dictionary = dict()
	num = 45
	while num <= 1189:
		num = num+1
		url = 'https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(num)+'&ver=big5&ft=0&temp=-1&tight=0'
		content = getScriptContent(url, False)
		print(content)
		if name == '-1':
			name = content[0].split(' ')[0]
			datapack.append(content[-1])
		if name == content[0].split(' ')[0]:
			datapack.append(content[-1])
		else:
			dictionary[name] = datapack
			name = content[0].split(' ')[0]
			datapack = []
			datapack.append(content[-1])
			print(dictionary)
			input('stop.')
	return -1
def list_FindChapter(StrongSearch, FilterSearch, name):
	global list_
	collect = []
	if StrongSearch:
		for i in list_:
			for n in name:
				if n in i.name():
					if not i in collect:
						collect.append(i)
	elif FilterSearch:
		for i in list_:
			flag = True
			name_ = i.name()
			for n in name:
				if not n in name_:
					flag = False
					break
			if flag:
				if not i in collect:
					collect.append(i)
	else:
		for i in list_:
			if name in i.name():
				if not i in collect:
					collect.append(i)
	return collect
def runner_code__ch56(b_fastmode, name, len_, return_):
	global list_
	StrongSearch = True
	FilterSearch = True
	collect = []
	in_ = -1
	if name=='':
		name = input(tab+'Chapter Name ------>')
	if len_==-1:
		len_ = int(input(tab+'Verse Number -------->'))
	while in_==-1:
		if FilterSearch:
			print(tab+'[FilterSearch Mode]')
			collect = list_FindChapter(False, True, name)
			FilterSearch = False
		if len(collect)==0:
			print(tab+'[FullName Mode]')
			collect = list_FindChapter(False, False, name)
		if len(collect)==0 and StrongSearch:
			print(tab+'[StrongSearch Mode]')
			collect = list_FindChapter(StrongSearch, False, name)
			FilterSearch = False
		if len(collect)==0:
			print(tab+'[StrongSearch Mode]')
			collect = list_FindChapter(True, False, name)
		if len(collect)>1:
			index = 1
			for c in collect:
				print(index, c.name())
				index=index+1
			in_ = int(input(tab+'Which One ? (-1:nope)_>'))
			if in_!=-1:
				if b_fastmode:
					continue
				ans = input(tab+'Is This What U Want \"' + collect[in_-1].name() + '\" ? (y/n) _>')
				if ans=='y' or ans=='Y':
					continue
				in_ = -1
				collect = []
		elif len(collect)==0:
			print(tab+'查無此關鍵字\"'+name+'\"，在章節名稱中')
		else:
			if b_fastmode:
				in_ = 0
				continue
			ans = input(tab+'Is This What U Want \"' + collect[0].name() + '\" ? (y/n) _>')
			if ans=='y' or ans=='Y':
				in_ = 0
				continue
			in_ = -1
			collect = []
		name = input(tab+'Chapter Name, Again Please... ------>')
		in_ = -1
	selec = collect[in_-1].name()
	sum_ = 0
	for l in list_:
		if l.name()==selec:
			break
		else:
			sum_ = sum_ + l.max()
	if len_>l.max():
		len_ = int(input(tab+'Verse Number, Again Please... ----(<'+str(l.max())+')---->'))
	print(tab+'[查找 %s 第%d章]' % (l.name(), len_))
	if return_:
		tab = tab+'\t'
		return getScriptContent('https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(sum_+len_)+'&ver=big5&ft=0&temp=-1&tight=0', False)
		tab = tab[0:-1]
	tab = tab+'\t'
	getScriptContent('https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(sum_+len_)+'&ver=big5&ft=0&temp=-1&tight=0', True)
	tab = tab[0:-1]


### ----------------------------------   Test Part - 1   ---------------------------------- ###
if not 1:
	url = 'https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap=1168&ver=big5&ft=0&temp=-1&tight=0'
	print(getScriptContent(url, True))
if not 1:
	## usable function -- Number To Script
	url = 'https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+input('------->')+'&ver=big5&ft=0&temp=-1&tight=0'
	getScriptContent(url, True)
def randomBibleScript():
	global tab
	## usable function -- Random Script
	number_ = number = random.randint(1, 1189)
	print(tab+'[隨機號碼，第%d章]' % (number), end=' ----> ')
	index=0
	while number_ > 0:
		number_ = number_ - list_[index].max()
		index = index + 1
	if number_<0:
		number_ = number_ + list_[index-1].max()
		print(list_[index-1].all()[0], number_)
	url = 'https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(number)+'&ver=big5&ft=0&temp=-1&tight=0'
	getScriptContent(url, True)

### ----------------------------------   Test Part - 2   ---------------------------------- ###
if not 2:
	MakeAllBible()

### ----------------------------------   Test Part - 3   ---------------------------------- ###
if not 3:
	SearchBible()
	MakeBiblePDF()

### ----------------------------------   Test Part - 4   ---------------------------------- ###
if not 4:
	## see total
	sum_ = 0
	for i in list_:
		sum_ = sum_ + i.max()
	print(sum_)
if not 4:
	## check match code
	number = int(input('Number ---(<1189)--->'))
	url = 'https://springbible.fhl.net/Bible2/cgic201/read201.cgi?na=0&chap='+str(number)+'&ver=big5&ft=0&temp=-1&tight=0'
	print(getScriptContent(url, False)[0])
	index=0
	while number > 0:
		number = number - list_[index].max()
		index = index + 1
	if number<0:
		number = number + list_[index-1].max()
		print(list_[index-1].all()[0], number)
def checkAllChaperMax():
	global list_
	global tab
	index=0
	print(tab, end='')
	for l in list_:
		index=index+1
		print(l.name(), l.max(), end='\t')
		if index%5==0:
			print('', end='\n'+tab)
		if index==len(list_):
			print('', end='\n')

### ----------------------------------   Test Part - 4   ---------------------------------- ###
# if not 5:
def findBibleScript():
	## usable function -- Find Bible Script
	ans = input(tab+'Less Questions Mode (y/n) ? _>')=='y'
	tab = tab+'\t'
	runner_code__ch56(ans, input(tab+'Chapter Name ------>'), int(input(tab+'Verse Number -------->')), False)
	tab = tab[0:-1]
# if not 6:
def findBibleScript_CNC():
	## usable function -- Find Bible Script
	a, b = input('Chapter Name & Verse Number ----(e.g.: 創世紀 5)---->').split(' ')
	tab = tab+'\t'
	runner_code__ch56(True, a, int(b), False)
	tab = tab[0:-1]
# if not 6:
def findBibleScript_CNCV():
	## usable function -- Find Bible Script Detail To Verse
	a, b, c = input('Chapter Name & Verse Number & VerseNumber ----(e.g.: 啟示錄 5 8-9)---->').split(' ')
	tab = tab+'\t'
	data = runner_code__ch56(True, a, int(b), True)
	tab = tab[0:-1]
	if '-' in c:
		x, y = [int(x) for x in c.split('-')]
	else:
		x, y = [int(x) for x in [c, c]]
	new_data = data[-1][x-1 if x-1>=1 else 0:y if y<=len(data[-1]) else len(data[-1])]
	b_showLine = False
	if x>1:
		if b_showLine:
			index = x-1
			for i in range(x-1):
				new_data = [str(index)+'. ...'] + new_data
				index = index - 1
		else:
			new_data = ['...'] + new_data
	if y<len(data[-1]):
		if b_showLine:
			index = y+1
			for i in range(len(data[-1])-y):
				new_data = new_data + [str(index)+'. ...']
				index = index + 1
		else:
			new_data = new_data + ['...']
	tab = tab+'\t'
	printScript(data[0], new_data)
	tab = tab[0:-1]


print('[Mode]\n\t\'m\' : show menu\t\t\'e\' : exit\n\t\'r\' : random bible script\n\t\'a\' : see all chapter length\n\t\'f\' : find bible script by ChapterName And Chapter\n\t\'fs\' : fast search bible script by ChapterName And Chapter\n\t\'afs\' : advanced fast search bible script by ChapterName And Chapter And VerseNumber\n\t\'cls\' : clear screen')
text = input('Input Mode_>')
while text=='':
	text = input('Input Mode_>')
while text!='':
	if text=='r':
		tab = tab+'\t'
		randomBibleScript()
		tab = tab[0:-1]
	elif text=='a':
		tab = tab+'\t'
		checkAllChaperMax()
		tab = tab[0:-1]
	elif text=='f':
		tab = tab+'\t'
		print('fixing error')
		time.sleep(5)
		findBibleScript()
		tab = tab[0:-1]
	elif text=='fs':
		tab = tab+'\t'
		print('fixing error')
		time.sleep(5)
		findBibleScript_CNC()
		tab = tab[0:-1]
	elif text=='afs':
		tab = tab+'\t'
		print('fixing error')
		time.sleep(5)
		findBibleScript_CNCV()
		tab = tab[0:-1]
	elif text=='cls':
		print('run \'cls\'')
		time.sleep(5)
	elif text=='e' or text=='exit':
		exit()
	elif text=='m' or text=='menu':
		print('[Mode]\n\t\'m\' : show menu\t\t\'e\' : exit\n\t\'r\' : random bible script\n\t\'a\' : see all chapter length\n\t\'f\' : find bible script by ChapterName And Chapter\n\t\'fs\' : fast search bible script by ChapterName And Chapter\n\t\'afs\' : advanced fast search bible script by ChapterName And Chapter And VerseNumber\n\t\'cls\' : clear screen')
	else:
		print('No Mode Found')
	text = input('Input Mode_>')
text = input('\n\n. E N D .\nInput Mode_>')
while text=='':
	text = input('Input Mode_>')

