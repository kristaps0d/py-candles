from modules.counter import CounterModule

def main():
	c = CounterModule('./material.mp4')
	# c = CounterModule('./marker.jpg')
	# c = CounterModule(0)

	try:
		c.run()
	except KeyboardInterrupt:
		del c

if __name__ == '__main__':
	main()