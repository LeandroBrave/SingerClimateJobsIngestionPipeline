from setuptools import setup, find_packages

setup(
    name="tap-openmeteo",
    version="0.1.0", 
    description="Singer tap to extract weather data from OpenMeteo API",
    author="Leandro Valente",
    packages=find_packages(), 
    install_requires=[
        "singer-python",
        "requests",
        "python-dotenv",
        "click",

    ],
    entry_points={
        "console_scripts": [
            "tap-openmeteo=tap_openmeteo.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
