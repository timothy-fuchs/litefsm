from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="litefsm",  # Package name
    version="0.1.0",  # Initial release version
    author="Timothy Fuchs",  # Your name or organization
    author_email="your.email@example.com",  # Your email
    description="A lightweight finite state machine library for Python",
    long_description=long_description,  # From README.md
    long_description_content_type="text/markdown",  # Content type for long description
    url="https://github.com/timothy-fuchs/litefsm",  # GitHub repository URL
    project_urls={
        "Bug Tracker": "https://github.com/timothy-fuchs/litefsm/issues",
    },
    classifiers=[  # Optional metadata classifiers
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),  # Automatically finds packages in the litefsm directory
    python_requires=">=3.6",  # Minimum Python version
)
