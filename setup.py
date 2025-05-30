from setuptools import setup, find_packages

setup(
    name='google_analytics',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'djangorestframework',
    ],
    description='A reusable Django REST API package.',
    author='Your Name',
    license='MIT',
)