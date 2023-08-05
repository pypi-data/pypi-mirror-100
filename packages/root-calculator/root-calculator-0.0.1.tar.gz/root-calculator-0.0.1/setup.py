import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="root-calculator",
    version="0.0.1",
    author="Princeton",
    author_email="mprinceton@primerobustics.com",
    description="An Example on Packaging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robustics/Packaging",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
