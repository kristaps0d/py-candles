from modules.counter import CounterModule

def main():
	# c = CounterModule('./material.mp4')
	c = CounterModule(1)

	try:
		c.run()
	except KeyboardInterrupt:
		del c

if __name__ == '__main__':
	main()