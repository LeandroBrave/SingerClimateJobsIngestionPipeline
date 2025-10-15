from setuptools import setup, find_packages

setup(
    name="tap-caged",
    version="0.1.0", 
    description="Singer tap to extract empregability data from CAGED API",
    author="Leandro Valente",
    packages=find_packages(), 
    install_requires=[
        "singer-python",
        "requests"

    ],
    entry_points={
        "console_scripts": [
            "tap-caged=tap_caged.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
