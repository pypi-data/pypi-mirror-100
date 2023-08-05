import setuptools as set
from setuptools import find_packages

long = open("set.txt", "r")
long = long.read()

set.setup(
    name = "MaskZ",
    version = "1.2.2",
    author = "Saad-py",
    author_email = "saadyarkhan11@gmail.com",
    description="MaskZ, a package intended to make all of the python users life easier ",
    long_description=long,
    packages=find_packages(),
    install_requires=["pyttsx3", "playsound", "pywin32", "gtts", "kivy", "pandas", "pathlib"]
)

