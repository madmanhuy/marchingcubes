from setuptools import setup

with open('README.md') as file_object:
    description = file_object.read()

setup(name='marching-cubes',
      version='0.0.1',
      author='Mandeep Bhutani, Huy Ha, Maddy Placik',
      author_email='mandeep@users.noreply.github.com',
      url='https://github.com/madmanhuy/marching-cubes',
      long_description=description,
      description='Build a 3D model from 2D image slices',
      license='MIT',
      packages=['marchingcubes'],
      install_requires=[
          'click>=7.0',
          'imageio==2.5.0',
          'numpy==1.16.3',
          'opencv-python==4.1.0.25',
          'pydicom==1.2.2',
      ],
      entry_points='''
          [console_scripts]
          marching-cubes=marchingcubes.cli:cli
          ''',
      classifiers=[
          'Development Status :: 5 - Production/Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
      ],
      )
