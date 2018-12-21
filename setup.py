from setuptools import setup


setup(
    name='hatena_blog',
    version='0.0.1',
    description='Hatena Blog Atom API Wrapper',
    author='Tatsuya Matoba',
    author_email='tatsuya.matoa.wk.jp@gmail.com',
    packages = ['hatena_blog'],
    include_package_data=True,
    install_requires=[
        'requests',
        'bs4'
    ],
)
