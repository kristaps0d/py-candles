from widgets.counter import CounterModule

from widgets.interface.gui import RunGui
from widgets.interface.windows.main import Main

import threading, sys

def main(src, args):

	if (len(args) > 2) and (args[2] == '--dev'):
		src='./materials/material.mp4'

	if (len(args) > 1) and (args[1] == '--nogui'):
		CounterModule(src, 'dbUri')
		quit()

	RunGui(Main, 'dbUri', src)
	
if __name__ == '__main__':
	src='./materials/candles_full-colored-tr.mp4'
	src='./materials/material4.mp4'
	main(src, sys.argv)