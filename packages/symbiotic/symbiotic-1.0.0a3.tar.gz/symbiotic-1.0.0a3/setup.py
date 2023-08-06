import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='symbiotic',
    version='1.0.0-alpha3',
    author='Stefano Frazzetto',
    author_email='stefano+symbiotic@hey.com',
    license='Apache-2.0',
    description='Connect your smart devices and sensors to create complex, schedulable actions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/StefanoFrazzetto/symbiotic',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware',
    ],
    keywords=[
        'automation',
        'dependency-injection',
        'event-bus',
        'iot',
        'schedule',
        'security',
        'smart-devices',
    ],
    install_requires=[
        'dependency-injector>=4.11',
        'event-bus',
        'gpiozero',
        'pigpio',
        'pydantic',
        'schema',
        'requests'
    ],
    extras_require={
        'dev': [
            'autopep8',
            'flake8',
        ],
        'test': [
            'pytest',
            'pytest-mock',
            'freezegun',
        ],
        'yaml': ['PyYAML>=5.4']
    },
    project_urls={
        'Bug Reports': 'https://github.com/StefanoFrazzetto/symbiotic/issues',
        'Source': 'https://github.com/StefanoFrazzetto/symbiotic',
    },
)
