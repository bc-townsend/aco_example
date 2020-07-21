from setuptools import setup

setup(name='Ant Colony Optimization Example',
    version='1.0',
    description='A small visual example of the ant colony optimization '\
                'algorithm initially proposed by Marco Dorigo. It is '\
                'based in real-time ant behavior as opposed to '\
                'analysis after every iteration.',
    url='https://github.com/bctownsend829/aco_example',
    author='Brandon Townsend',
    author_email='bctownsend829@gmail.com',
    packages=['aco_example'],
    install_requires=[
        'pygame'
    ],
)