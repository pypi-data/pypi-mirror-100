twine:
	pip install twine

build:
	python setup.py sdist bdist_wheel

check:
	twine check dist/*

upload:
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

publish:
	build
	check
	upload