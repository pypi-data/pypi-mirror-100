import setuptools as set
from setuptools import find_packages


long = ["Howdie Programmers\n",
"MaskZ is the library to help you make your python life easier.\n\n",
"Need Help?\n\nIf you are an experienced programmer You guys know you can use help() function in python\n",
"If you are a beginner be sure to keep checking the Github repo for MaskZ and I may upload YouTube videos explaining how MaskZ works\n",
"The docs will be released after the third major update because all the important things will be added by then.\n\n",
"Issues:"
"Want to talk create an issue on github or send an email to the given email located somewhere in the repo."
"Can't Find Email, Here it is: saadyarkhan11@gmail.com"
"I am on Hangouts, but not Discord.\nThanks for Downloading\n"
"1.0.1 Patch Notes  (Changed description mistakes)  (renamed several sub-modules)  (websear has a function now)\n\n",
"1.2.0 Patch Notes: 1.Fixed math functions 2.Modules will be preinstalled        I apologize for the problems"]
l = ""
for i in long:
    l+=i
set.setup(
    name = "MaskZ",
    version = "1.2.3",
    author = "Saad-py",
    author_email = "saadyarkhan11@gmail.com",
    description="MaskZ, a package intended to make all of the python users life easier ",
    long_description=l,
    packages=find_packages(),
    install_requires=["pyttsx3", "playsound", "pywin32", "gtts", "kivy", "pandas", "pathlib"]
)

