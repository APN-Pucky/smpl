import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "uncertainties",
    "numpy",
    "matplotlib",
    "scipy",
    "sympy",
    "tqdm",
    "pandas",
    # "requests",
]
dev_requirements = [
    "build",
    "pytest",
    "sphinx",
    "sphinx-math-dollar",
    "jupyterlab",
    "numpydoc",
    "sphinx",
    "nbsphinx",
    "sphinx-rtd-theme",
    "pandas",
    "ipython"
]

setuptools.setup(
    name="smpl",
    setup_requires=['setuptools-git-versioning'],
    author="APN",
    author_email="APN-Pucky@no-reply.github.com",
    description="simple plotting and fitting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/APN-Pucky/smpl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    extra_require={
        'dev': dev_requirements
    },
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}.{ccount}",
        "dirty_template": "{tag}.{ccount}+dirty",
        "starting_version": "0.0.0",
        "version_callback": None,
        "version_file": None,
        "count_commits_from_version_file": False
    },
    python_requires='>=3.6',
)
