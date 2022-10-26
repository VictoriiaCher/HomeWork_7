from setuptools import setup, find_namespace_packages

setup(
    name="clean-folder",
    version="1.0",
    description="The package sorts the files in the folder specified by the user",
    url="https://github.com/VictoriiaCher/HomeWork_7.git",
    author="Victoriia Cherevchenko",
    author_email="cherevchenko.victoriy@gmail.com",
    license="Free",
    include_package_data=True,
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["clean-folder = clean_folder.clean:main"]},
)
