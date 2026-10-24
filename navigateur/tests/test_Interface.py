"""Validation élémentaire de l'interface graphique sans fenêtre interactive."""
import matplotlib
matplotlib.use("Agg")
from navigateur.classes.Interface import Interface


def test_interface_cree_une_figure():
    interface = Interface()
    assert interface.fig is not None
    import matplotlib.pyplot as plt
    plt.close(interface.fig)
