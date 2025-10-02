from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = "-e ."
def get_requiremnts(file_path:str)->List[str]:
    requirements = []
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements


setup(
    name = "Weather Classification",
    version="0.0.1",
    author="Manpreet",
    author_email="bhatia.manpreet1224@gmail.com",
    packages=find_packages(),
    install_requires=get_requiremnts("requirements.txt")
)