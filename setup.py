import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smpl", # Replace with your own username
    version="0.0.0",
    author="APN",
    author_email="APN-Pucky@no-reply.github.com",
    description="simple plotting and fitting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/APN-Pucky/simplepy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "uncertainties",
        "numpy",
        "matplotlib"
    ],
    python_requires='>=3.6',
)