import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="npc-shopify-cli",  # Replace with your own username
    version="0.0.5",
    author="Newspaper Club Ltd",
    author_email="services@newspaperclub.com",
    description="A cli for working with Shopify",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/newspaperclub/npc-shop-cli",
    project_urls={
        "Bug Tracker": "https://github.com/newspaperclub/npc-shop-cli/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    executables=[
        "npc-theme"
    ]
)
