# FEMAG-Optimizer
## Kurzfassung
Die folgende Arbeit befasst sich mit der Optimierung der Auslegungsparameter von numerischen Analysen komplexer Systeme. Hierbei ist das Kernthema, die Defizite der klassischen Optimierungsverfahren in der Handhabung rechenaufwendiger Systeme zu umgehen.
Das dafür angewandte Verfahren ist die Response Surface Methode (RSM). Mit Hilfe der RSM wird eine Approximation, auch Metamodell genannt, erstellt. Dieses Metamodell ersetzt die rechenaufwendige Systemanalyse und wird für die Optimierung der Auslegungsparameter verwendet. 
Als Simulationsmodell wird ein Finite-Elemente-Programm (“FEMAG DC“) zur Berech-nung zweidimensionaler und achsensymmetrischer Magnet- und Wirbelstromfelder verwendet. Die Implementierung der Simulation in das RSM Programm wird mit der Programmiersprache Python realisiert. Es werden die Approximation und die anschließende Optimierung mit den gängigen Bewertungskriterien analysiert. 
Diese Arbeit ist ein Bespiel dafür, wie die RSM umgesetzt wird und kann helfen eigene Projekte in diesem Bereich zu realisieren. 

## Entwurfsparameter

Die Entwurfsvariablen sind folgende:
- DA: Außen Durchmesser (m.yoke_diam) 
- H: Nuttiefe (m.slot_height)
- TW: Zahnbreite (m.tooth_width)
- RA: Magnet außen Radius (m.mag_rad)
- BT: Bautiefe (m.arm_lenght)
- HM: Magnethöhe (m.mag_height)
