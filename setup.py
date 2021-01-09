from setuptools import setup, find_packages

setup(
    name = 'SiteTracker',
    version = '1.0',
    long_description = 'Tracks website usage',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
)