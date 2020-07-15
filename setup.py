import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="poe_bot", # Replace with your own username
    version="0.0.1",
    author="Joseph Luce",
    author_email="luceCoding@gmail.com",
    description="Path of Exile bot program.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.3',
)