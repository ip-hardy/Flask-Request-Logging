from setuptools import setup, find_packages

setup(
    name='Flask-Logging-Request',
    version='0.1',
    author='liuzhiyong',
    author_email='ip_hardy@qq.com',
    description='Logging for Flask Request',
    keywords = ['flask', 'logging'],
    packages=['flask_logging_request'],
    zip_safe=False,
    platforms='any',
    install_requires=['Flask']
)

