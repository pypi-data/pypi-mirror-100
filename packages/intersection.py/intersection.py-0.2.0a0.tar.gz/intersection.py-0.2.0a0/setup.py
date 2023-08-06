from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: 3"
]

setup(
    name="intersection.py",
    version="v0.2.0-alpha",
    description="A simple API Wrapper for IC",
    long_description=open("README.txt").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Feeeeddmmmeee/intersection.py',
    author='Feeeeddmmmeee',
    author_email='',
    license='MIT',
    classifiers=classifiers,
    keywords='api',
    packages=find_packages(),
    install_requires=['requests']
)