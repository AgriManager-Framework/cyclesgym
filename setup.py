import os
import setuptools
from setuptools.command.install import install

install_requires = [
    'requests',
    'numpy',
    'pandas',
    'matplotlib',
    'gym',
    'ipykernel',
    'pyglet',
]

solve_requires = [
    'torch>=1.8.1',
    'stable-baselines3',
    'tensorboard',
    'wandb',
    ]


class NewInstall(install):
    """Post-installation for installation mode."""
    def run(self):
        super().run()
        if os.environ.get("CYCLES_GYM_SKIP_INSTALL") == "1":
            print("POST INSTALL skipped (CYCLES_GYM_SKIP_INSTALL=1)")
            return
        print('POST INSTALL')
        from install_cycles import install_cycles

        install_cycles()


setuptools.setup(
    name='cyclesgym',
    version='0.1.0',
    description='Open AI gym interface to the cycles crop simulator',
    url='https://github.com/koralabs/cyclesgym',
    author='Matteo Turchetta',
    author_email='matteo.turchetta@inf.ethz.ch',
    keywords='Crop growth simulator',
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
            "SOLVERS": solve_requires
        },
    cmdclass={'install': NewInstall},
)
