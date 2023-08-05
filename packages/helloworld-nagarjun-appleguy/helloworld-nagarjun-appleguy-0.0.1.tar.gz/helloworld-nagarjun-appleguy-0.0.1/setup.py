from setuptools import setup

with open('README.md','r') as fh:
	long_description = fh.read()

setup(

	name = 'helloworld-nagarjun-appleguy',
	version = '0.0.1',
	description = "Hello World Functionality",
	py_modules = ["helloworld"],
	package_dir = {'': 'src'},
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Nagarjun",
	author_email = "abc@gmail.com",

	)