# FEMAG-Optimizer
## Kurzfassung
Die folgende Arbeit befasst sich mit der Optimierung der Auslegungsparameter von numerischen Analysen komplexer Systeme. Hierbei ist das Kernthema, die Defizite der klassischen Optimierungsverfahren in der Handhabung rechenaufwendiger Systeme zu umgehen.
Das dafür angewandte Verfahren ist die Response Surface Methode (RSM). Mit Hilfe der RSM wird eine Approximation, auch Metamodell genannt, erstellt. Dieses Metamodell ersetzt die rechenaufwendige Systemanalyse und wird für die Optimierung der Aus-legungsparameter verwendet. 
Als Simulationsmodell wird ein Finite-Elemente-Programm (“FEMAG DC“) zur Berech-nung zweidimensionaler und achsensymmetrischer Magnet- und Wirbelstromfelder ver-wendet. Die Implementierung der Simulation in das RSM Programm wird mit der Pro-grammiersprache Python realisiert. Es werden die Approximation und die anschließende Optimierung mit den gängigen Bewertungskriterien analysiert. 
Diese Arbeit ist ein Bespiel dafür, wie die RSM umgesetzt wird und kann helfen eigene Projekte in diesem Bereich zu realisieren. 
