from profielentoolbox.hello_world import hello_world

def test_import():
    """Test de import van de hello world functie."""
    result = hello_world()
    assert result == "Hello world again!"
