from setuptools import setup

setup(name='Ant Colony Optimization Example',
      version='1.0',
      description='A small visual example of the ant colony optimization '
                  'algorithm initially proposed by Marco Dorigo. It is '
                  'based in real-time ant behavior as opposed to '
                  'analysis after every iteration.',
      url='https://github.com/bc-townsend/aco_example',
      author='Brandon Townsend',
      author_email='bc_townsend@outlook.com',
      packages=['aco_example'],
      install_requires=[
          'pygame'
      ],
      )
