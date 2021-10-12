from pathlib import Path
from distutils.core import setup

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='checksitemap',
    version='v1.0.0',
    packages=[''],
    scripts=['checksitemap'],
    url='https://github.com/Deuchnord/checksitemap',
    license='AGPL-3.0',
    author='Jérôme Deuchnord',
    author_email='jerome@deuchnord.fr',
    description='A tool to verify your sitemaps',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    python_requires=">=3.9",
)
