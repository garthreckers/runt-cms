"""
Start up Flask/Runt
"""
from runt.trigger import TRIGGER

if __name__ == "__main__":
	TRIGGER.run('0.0.0.0')
