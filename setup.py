from setuptools import setup, find_namespace_packages

setup(
    name="cli-anything-topaz-video",
    version="1.0.0",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cli-anything-topaz-video=cli_anything.topaz_video.topaz_video_cli:cli",
        ],
    },
    python_requires=">=3.10",
    package_data={
        "cli_anything.topaz_video": ["skills/*.md"],
    },
)
