from setuptools import setup

setup(
    name="clean_folder",
    version="1.0",
    description='Sort files in a folder acoord. to their extention',
    url='https://github.com/SergDulin/goit_hw-06',
    author='Serhii Dulin',
    packages=["clean_folder"],
    entry_points={
        "console_scripts": ["clean-folder=clean_folder.clean:main"]
    },
    install_requires=["patool"],
)
