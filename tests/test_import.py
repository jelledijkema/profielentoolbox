import sys
sys.path.insert(0, r'/home/jelledijkema/Klanten/Profielentool/src/')  # Add your repo's src dir to Python path
from profielentoolbox.hello_world import hello_world

def test_import():
    result = hello_world()
    assert result == "Hello world again!"
