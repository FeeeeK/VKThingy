try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="VKSlaves",
    version="1.0.0",
    author="FeeeeK (@f_ee_k)",
    license="gpl-3.0",
    description="Asynchronous api wrapper for the game from vk.com called 'slaves'",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=["vkslaves", "vkslaves.models"],
    keywords=["vk-slaves", "slaves", "vk", "vkslaves_bot"],
    install_requires=open('./requirements.txt').read().split()
)
