import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="aipo-project",
    version="1.0",
    authors="Radosław Leluk, Piotr Litwin",
    description="AIPO project - people detection and counting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rleluk/AIPO",
    install_requires=[
        "opencv-contrib-python",
        "numpy",
        "imutils",
        "requests",
        "python-decouple"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
)