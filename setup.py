from setuptools import setup, find_packages

setup(
    name="derive_eq",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'derive_eq=derive_eq.cli:main',
        ],
    },
    install_requires=['feedparser'],
    python_requires='>=3.11',
    author='Joe Bacchus, Alex, Piotr Toka',
    author_email='',
    description='Command line tool for getting derivation of equations',
    url='https://github.com/joebacchus/mathhack.git',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
