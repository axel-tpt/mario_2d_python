from setuptools import setup, find_packages

setup(
    name='Mario_2D',
    version='1',
    packages=find_packages(),
    install_requires=[
        'pygame==2.5.2',
        'mixer==7.2.2'
    ],
    entry_points={
        'console_scripts': [
            'start=mario_2d.main:main',
        ],
    },
    author='Axel TREPOUT',
    author_email='axel.trepout@outlook.com',
    description='A simple Mario 2D game in Python',
    url='https://github.com/axel-tpt/mario_2d_python.git',
)
