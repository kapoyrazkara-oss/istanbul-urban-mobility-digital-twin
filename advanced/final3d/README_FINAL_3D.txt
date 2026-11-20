ISTANBUL ADAPTIVE MOBILITY ATLAS — FINAL 3D VIEWER

BU PAKETI NASIL ACACAKSINIZ?
1) Bu klasoru ZIP'ten tamamen cikarin.
2) START_FINAL_3D.bat dosyasina cift tiklayin.
3) Siyah komut penceresi acik kalirken Chrome otomatik olarak viewer'i acacaktir.
4) Chrome acilmazsa komut penceresinde yazan http://127.0.0.1:PORT/viewer.html adresini Chrome'a yapistirin.
5) Viewer'i kapatmak icin once Chrome sekmesini, sonra komut penceresinde Ctrl+C'yi kullanin.

ONEMLI
- viewer.html dosyasina cift tiklamayin. file:// modu, JSON replay dosyalarini guvenilir sekilde yuklemez.
- Bu pakette sadece bu klasordeki START_FINAL_3D.bat dosyasini kullanin. Eski digital_twin_v2, safe-mode ve presentation dosyalarini acmayin.
- Internet gerekmez; Three.js kutuphaneleri ve replay verileri paketin icindedir.
- Chrome, Edge veya Firefox guncel surumleri desteklenir.

KONTROLLER
- Fixed-Time, Local Adaptive ve Coordinated Adaptive butonlari controller replay'ini degistirir.
- Pause/Play, Reset ve hiz secimi replay akisini yonetir.
- Mouse sol tus orbit, tekerlek zoom, sag tus pan icindir.
- Overview, Street ve North kamera presetleridir.
- Bir kavsaga tiklayinca secilen intersection adi ve tipi sol panelde gorunur. Sahne, four-way, T-junction, roundabout ve offset junction formlarini karisik kullanir.

DUZENLEME
- Renkler, bina boyutlari ve sahne elemanlari viewer.html icindeki buildCity, buildIntersection ve tree fonksiyonlarinda bulunur.
- Replay verileri data/v2_fixed.json, data/v2_local.json ve data/v2_coordinated.json dosyalaridir.
- Yeni veri eklemek icin DATA nesnesine yeni bir JSON yolu ve LABELS nesnesine gorunen ad ekleyin.
- vendor klasorundeki dosyalari silmeyin; bunlar local Three.js runtime'idir.

PROJE BAGLANTISI
Bu viewer, Istanbul Urban Mobility Digital Twin Build projesindeki 5x5 / 25 sinyalli SUMO deneylerinin replay'lerini gorsellestirir. Ana dogrulanmis sonuclar README/article klasorlerindeki multi-seed dokumantasyondadir; viewer bir sunum ve inceleme arayuzudur.
