# TODO

W ramach projektu należy stworzyć program, który będzie renderował złożoną geometrycznie scenę z wieloma źródłami światła wykorzystując tzw. Forward Rendering.
W tym celu należy zaimplementować następujące punkty:

- [x] Przygotować scenę 3d składającą się z paru różnych figur geometrycznych
- [ ] Zaimplementować algorytm Odroczonego Cieniowania (ang. Deffered Shading)
  - [ ] Implementacja render pass do generowania G-Buffera
  - [ ] Wykorzystanie G-bufferów w aplikowaniu cieniowania
- [ ] Cieniowanie powinno obejmować składowe diffuse i specular
- [ ] Cieniowanie powinno uwzględniać głębokość (bufor Z)
- [ ] Cieniowanie powinno wspierać wiele źródeł światła
- [ ] Przetestować scenę dla złożonej geometrycznie sceny (np. wiele obiektów o prostej geometrii)
- [ ] Dodać wiele źródeł światła (Opcjonalnie: zaimplementować opcję dodawania N losowo wygenerowanych źródeł światła).
- [x] Kamerę perspektywiczną - możliwość poruszania się po scenie oraz obrotu
