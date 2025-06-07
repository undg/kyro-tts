activate:
	mise deactivate
	# source venv/bin/activate
	# For AMD GPU you may want to:
	export MIOPEN_FIND_MODE=FAST
	export CUDA_VISIBLE_DEVICES=""
run:
	bash bin/activate
	export MIOPEN_FIND_MODE=FAST
	export CUDA_VISIBLE_DEVICES=""
	uvicorn api:api --reload
