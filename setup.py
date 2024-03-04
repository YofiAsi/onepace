import setuptools
setuptools.setup(
    name='onepace',
    version='1.0',
    author='Me',
    description='This runs my script which is great.',
    packages=['onepace'],
    install_requires=[
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'onepace = onepace.cli:main'
        ],
    },
    python_requires='>=3.5'
)