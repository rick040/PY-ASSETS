"""Gedeelde kit voor het partnerprogramma: tokens, tekst, atoms, QR, render en tests."""
import importlib.util


def load(path, name):
    """Laad een ontwerp.py uit een visual-map onder een eigen naam (alle mappen noemen hun script hetzelfde)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
