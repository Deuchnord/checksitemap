black:
	poetry run black checksitemap tests.py

tests:
	poetry run pytest tests.py
