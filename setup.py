"""Setup the application."""

from pathlib import Path

from setuptools import setup


requirements = (Path(__file__).parent / 'requirements.txt').read_text().split('\n')


setup(
    install_requires=[line for line in requirements if line and not line.startswith('#')]
)
