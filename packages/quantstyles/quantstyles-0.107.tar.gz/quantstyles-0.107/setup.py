from setuptools import setup, find_packages
from subprocess import check_call

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='quantstyles',
    version='0.107',
    description='Matplotlib styles for scientific usage',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Andrii Trelin',
    author_email='andrii.trelin@uni-rostock.de',
    keywords=[],
    url='https://github.com/Trel725/quantstyles',
    download_url='https://pypi.org/project/quantstyles/'
)

install_requires = [
    'matplotlib',
]

if __name__ == '__main__':

    with open("quantstyles/style_installed.flag", "w") as f:
        f.write("0")

    check_call("python generate_quantcmaps.py".split(),
               cwd="quantstyles")

    setup(**setup_args,
          install_requires=install_requires,
          include_package_data=True)
