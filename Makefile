run:
	@if command -v mise >/dev/null 2>&1 && mise env status | grep -q active; then mise deactivate; fi; \
	. venv/bin/activate; \
	export MIOPEN_FIND_MODE=FAST; \
	export CUDA_VISIBLE_DEVICES=""; \
	uvicorn api:api --reload
