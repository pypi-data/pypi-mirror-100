from setuptools import setup, find_packages


setup(
    name="VKSlaves",
    version="1.0.1",
    author="FeeeeK (@f_ee_k)",
    license="gpl-3.0",
    url="https://github.com/feeeek/vkslaves",
    description="Asynchronous api wrapper for the game from vk.com called 'slaves'",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=["vk-slaves", "slaves", "vk", "vkslaves_bot"],
    include_package_data=True,
)
