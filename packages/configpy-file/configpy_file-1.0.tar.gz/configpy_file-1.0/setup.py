import setuptools

long_description = '''
Create config file.  
Supports: config.c, config.h, config.cpp, config.hpp, config.py and config.pyc
Use it as this:
```
#!/usr/bin/env python3

from config_py import ConfigPy
config = ConfigPy()
config['number'] = 42.5
config['string'] = 'hello'
config['none'] = None
config['boolean'] = True
config.save('./config.py')
```
'''

setuptools.setup(
    name="configpy_file",
    version="1.0",
    author='Vadim Simakin',
    author_email="sima.vad@yandex.com",
    description="Create config.py or config.h file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['config_py'],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
