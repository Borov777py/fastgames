from setuptools import setup, find_packages

version = "0.0.5"


setup(
    name='fastgames',
    version=version,
    description='Fast creation of python games',
    author='Borov777py',
    author_email='kozhushko756@mail.ru',
    url='https://github.com/Borov777py/fastgames',
    packages=find_packages(),
    install_requires=[
        'pydantic',
    ]
)
