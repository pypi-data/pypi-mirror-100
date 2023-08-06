import setuptools

setuptools.setup(
    name="ffd", # Replace with your own username
    version="0.5.12",
    author="ffd",
    author_email="ffd@example.com",
    description="future frame detection package",
    long_description_content_type="text/plain",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="./src"),
    python_requires=">=3.6",
)