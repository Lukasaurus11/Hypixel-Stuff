from setuptools import setup, find_packages
from utils.helper_functions import dictToJSON


dictToJSON({"hypixel-token": "<Your Hypixel API Token>"}, "data/secrets.json")

setup(
    name="Hypixel-Skyblock-Project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        'numpy',
        'NBT'
    ],
    author='Lukasaurus11',
    description="A project to deal with different aspects of Hypixel Skyblock",
    url="https://github.com/Lukasaurus11/Hypixel-Stuff",
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)