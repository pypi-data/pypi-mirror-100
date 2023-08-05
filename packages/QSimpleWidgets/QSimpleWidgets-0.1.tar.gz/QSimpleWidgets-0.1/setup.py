import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QSimpleWidgets", # Replace with your own username
    version="0.1",
    author="José Alexsandro || eualexdev",
    author_email="eualex@github.com",
    description="QtSimpleWidgets Adiciona Novos ao PyQt5",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eualexdev/QSimpleWidgets",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
