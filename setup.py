from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="files-organizer",
    version="1.0.1",
    install_requires=["pyfiglet>=0.8", "fire>=0.2.1"],
    extras_require={"win": ["pywin32"]},
    packages=find_packages(),
    description="Move files by date into folders month by month",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alexandre Calil Martins Fonseca",
    author_email="alexandrecalilmf@gmail.com",
    license="MIT",
    python_requires=">=3.6",
    url="https://github.com/xandao6/files-organizer",
    download_url="https://pypi.org/project/files-organizer",
    keywords=[
        "organizer"
        "date to folders",
        "images organizer",
        "images date to folders"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["files-organizer = src.organizer:main"]},
)
