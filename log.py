_verbose = False

def verbose(msg):
	if _verbose:
		print(msg)

# Define ANSI escape codes for colors and reset
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m' # Resets color and style

def fail(msg):
	print(f"{RED}  fail >> {msg}{RESET}")

def warn(msg):
	print(f"{YELLOW} warn >> {msg}{RESET}")

def done(msg):
	print(f"{GREEN}󰸞 done >> {msg}{RESET}")
