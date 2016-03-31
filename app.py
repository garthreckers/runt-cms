"""
Start up Flask/Runt
"""
from runt.trigger import trigger


if __name__ == "__main__":
	trigger.run('0.0.0.0')
