import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wiperf_chat_bot",
    version="0.0.7",
    author="WLAN Pi Team",
    author_email="infol@wlanpi.com",
    description="Telegram chatbot for the WLAN Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WLAN-Pi/wlanpi-chat-bot",
    packages=setuptools.find_packages(),
    install_requires=['timeout_decorator'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: POSIX :: Linux",
    ],
    include_package_data=True,
    python_requires='>=3.7',
)