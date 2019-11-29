test:
	cd tests && python3 -m unittest -v

publish:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

coverage:
	pytest --cov=seriesbr

lint:
	flake8 seriesbr

clean:
	rm -rf build dist .egg *.egg-info
