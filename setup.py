from setuptools import setup, find_packages

HYPHEN_E = ". -e"

def get_requirement(file_path):
    requirements = []

    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.replace("\n","") for req in requirements]

    if HYPHEN_E in requirements:
        requirements.remove(HYPHEN_E)

    return requirements

setup(
    name="Weather-Classification",
    version="0.0.1",
    author="Manpreet",
    author_email="bhatia.manpreet1224@gmail.com",
    packages=find_packages(),
    requires=get_requirement("requirements.txt")
)