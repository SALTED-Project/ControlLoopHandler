from setuptools import setup
import controlloophandler

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='controlloophandler',
    version=controlloophandler.__version__,    
    description='Control Loop handler for control loop mechanism within SALTED.',
    url='https://github.com/SALTED-Project/ControlLoopHandler',
    author='',
    author_email='',
    license='',
    packages=['controlloophandler'],
    install_requires=required,
    # see: https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Python :: 3 :: Only'
    ],
)