from setuptools import setup

f = open("README.md","r").read()

setup(
    name="pytohub",
    version="v0.5-alpha",
    author="mas6y6",
    long_description=f,
    description="This is a module that can connect to your lego RI hub or lego SPIKE PRIME hub and can directly upload modules to your hub"
    
)