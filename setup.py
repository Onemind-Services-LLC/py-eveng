from pathlib import Path
from setuptools import find_packages, setup


README = (Path(__file__).parent / "README.md").read_text()
REQUIRES = [
    "click>=7.1.1,<8.1.0",
    "requests>=2.20.0",
    "python-dotenv",
    "pyyaml>=5.3,<7.0",
    "Jinja2>=2.10.3,<3.1.0",
    "rich==10.16.2",
    "jsonschema==4.3.3",
]


def get_version():
    global_vars = {}
    exec(Path("src/evengsdk/cli/version.py").read_text(), global_vars)
    return global_vars["__version__"]


setup(
    name="eve-ng",
    keywords=["eve-ng", "eveng", "unetlab", "evengsdk"],
    license="MIT license",
    version=get_version(),
    author="Abhimanyu Saharan",
    author_email="asaharan@onemindservices.com",
    maintainer="Onemind Services LLC",
    maintainer_email="developers@onemindservices.com",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    description=(
        "Python SDK and command line utilities to work with the EVE-NG REST API"
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Onemind-Services-LLC/evengsdk.git",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=REQUIRES,
    entry_points={
        "console_scripts": [
            "eve-ng=evengsdk.cli.cli:main",
            "eveng=evengsdk.cli.cli:main",
        ],
    },
    include_package_data=True,
)
