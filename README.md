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

<img src="https://github.com/AI-Assistant/FEMAG-Optimizer/blob/main/AddFiles/Geometrie.jpg" width="740px">


## Grenzwerte

Die oberen Grenzen maxj⁡(ξ_i(j)  ) und die unteren Grenzen minj⁡(ξ_i(j)  )   der einzelnen Variablen ξ_i(p)  werden in Python als Abfragefunktion berechnet. Dafür wird die Stützstelle ξ_((p) ) mit der zu bestimmenden Variable i in die Funktion eingelesen. Diese gibt den Maximalwert oder Minimalwert der entsprechenden Variablen zurück. Die folgende Tabelle beinhaltet die Grenzwerte der einzelnen Entwurfsvariablen. 

|ξ_i(p) |	(max)p⁡(ξ_i(p)  )	|(min)p⁡(ξ_i(p)  )|
|--|--|--|
ξ_1(p) =DA|(RA*2)+4mm+H+200mm	|2*(RA+H)+44mm
ξ_2(p) =H	|((DA-390mm))/2-10mm	|30mm
ξ_3(p) =TW	|(π*390mm)/48-10mm	|10mm
ξ_4(p) =RA	|250mm	|153mm
ξ_5(p) =BT	|300mm	|50mm
ξ_6(p) =HM	|RA-140mm	|5mm

[Vollständige Dokumentation](https://github.com/AI-Assistant/FEMAG-Optimizer/blob/main/AddFiles/RSM_FEMAG_Kander_Akinci.pdf)
