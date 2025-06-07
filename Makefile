activate:
	bash bin/activate
	# For AMD GPU you may want to:
	export MIOPEN_FIND_MODE=FAST
	export CUDA_VISIBLE_DEVICES=""
