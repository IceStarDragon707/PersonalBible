def collide(i, max_):
	while i<=max_:
		return str(i)
	else:
		ll = 0
		while not i<=max_:
			i = i - 1
			ll = ll + 1
		return str('%d (require %d more chapters)'%(i, ll))

def func(text, i, step, max_):
	step = step - 1
	while i<=max_:
		print(text+' '+'%d-%s'%(i, collide(i+step, max_)))
		i = i + step + 1

chs = input('輸入經文名稱---->')
if '[' in chs and ']' in chs:
	chs = chs[1:-1]
	chs = chs.replace(', ', ',').replace(',', ', ').replace('\'', '').replace('\"', '').split(', ')
if type(chs)==str:
	func(chs, int(input('\t起始章節---->')), int(input('\t每日幾章---->')), int(input('\t結束章節---->')))
else:
	for c in chs:
		print(c)
		func(c, int(input('\t起始章節---->')), int(input('\t每日幾章---->')), int(input('\t結束章節---->')))
input('Press Enter To Leave....')
