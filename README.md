# Interactive_swing

Simple electric network dynamic simulator for interactive transient visualization (swing dynamics for synchronous machines and Kuramoto dynamics for loads). This simulator displays live frequency and voltage phases plots. Gui interactions allow to modify transmission line and bus parameters.

The folder "/network_data" contains a non exhausitve set of sample networks (in *.csv format) to choose from.

To run: "python swing_app.py"

Runs on: Python 2.7

Module requirements:

numpy = 1.14.0
scipy = 0.17.0
networkx = 2.0
pyqtgraph = 0.10.0
PyQt4

