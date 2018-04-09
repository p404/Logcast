analyze:
	bandit -r ./logcast
init:
	  pip3 install -r requirements.txt
lock: 
	  pipreqs . --force