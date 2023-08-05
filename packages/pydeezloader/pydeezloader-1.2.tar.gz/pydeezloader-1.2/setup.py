from setuptools import setup

setup(
    name="pydeezloader",
    version="1.2",
    description="Download Songs, Albums and Playlists - from Deezer and Spotify.",
    license="GNU General Public License V3+",
    author="BlackStoneReborn",
    author_email="BlackStoneOfficial3@gmail.com",
    url="https://github.com/TheDeezLoader/pyDeezloader",
    packages=["pydeezloader"],
    install_requires=[
        "Flask",
        "flask-cors",
        "stagger",
        "mutagen",
        "pycryptodome",
        "requests>=2.25.0",
        "spotipy",
        "tqdm",
        "six>=1.15.0",
    ],
    scripts=["pydeezloader/bin/deez-dw.py", "pydeezloader/bin/deez-web.py"],
)
