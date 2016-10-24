def fuck(n, a,b,c):
	if n == 1:
		print(a,'-->',c)
		return
	fuck(n-1, a, c, b)
	print(a, '-->', c)
	fuck(n-1, b, a, c)
	return
	
def shits(n):
	fuck(n,'a','b','c')