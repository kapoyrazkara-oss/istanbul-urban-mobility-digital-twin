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
- Fixed-Time ve Adaptive butonlari controller replay'ini degistirir.
- Pause/Play, Reset ve hiz secimi replay akisini yonetir.
- Mouse sol tus orbit, tekerlek zoom, sag tus pan icindir.
- Overview, Street ve North kamera presetleridir.
- Bir kavsaga tiklayinca secilen intersection adi ve tipi sol panelde gorunur. Sahne, four-way, T-junction, roundabout ve offset junction formlarini karisik kullanir.

DUZENLEME
- Renkler, bina boyutlari ve sahne elemanlari viewer.html icindeki buildCity, buildIntersection ve tree fonksiyonlarinda bulunur.
- Replay verileri data/v2_fixed.json ve data/v2_local.json dosyalaridir.
- Yeni veri eklemek icin DATA nesnesine yeni bir JSON yolu ve LABELS nesnesine gorunen ad ekleyin.
- vendor klasorundeki dosyalari silmeyin; bunlar local Three.js runtime'idir.

PROJE BAGLANTISI
Bu viewer, Istanbul Urban Mobility Digital Twin Build projesindeki 5x5 / 25 sinyalli SUMO deneylerinin replay'lerini gorsellestirir. Ana dogrulanmis sonuclar README/article klasorlerindeki multi-seed dokumantasyondadir; viewer bir sunum ve inceleme arayuzudur.

TRAFIK SENARYOSU GUNCELLEME
Viewer icindeki Traffic profile / time window seceneginden Rush-hour demand veya Balanced demand secilebilir. Bu secim sadece UI rengi degildir; ilgili SUMO replay JSON dosyalari yeniden yuklenir ve araclar, kuyruklar, sinyaller, heatmap ve grafik yeni veriyle guncellenir.

Yeni bir sabah, aksam veya gece senaryosu icin once advanced/routes altinda ilgili SUMO route dosyasini tanimlayin ve advanced/export_3d_v2.py icindeki ROUTES sozlugune ekleyin. Ornek exporter komutlari:
python advanced/export_3d_v2.py --controller fixed --scenario balanced --steps 600 --output advanced/final3d/data/balanced_fixed.json
python advanced/export_3d_v2.py --controller coordinated-adaptive --scenario rush-hour --steps 600 --output advanced/final3d/data/v2_coordinated.json
Daha sonra viewer.html icindeki PATHS sozlugune yeni scenario adini ve uc controller JSON yolunu ekleyin.

YOGUNLUK VE KUYRUK RENKLERI
Her kavsagin etrafindaki halka o anki queue degerine gore yesil, sari veya kirmizi olur. Heatmap ayni veriyi 5x5 gridde gosterir. Yesil dusuk, sari orta, kirmizi yuksek kuyruk baskisini ifade eder.

KAVSAK BAZLI KURALLAR
Roundabout kavsaklarda sinyal direkleri yerine yield-on-entry isaretleri kullanilir. T-junction formlarinda ana yol onceligi ve yan koldan yield mantigi kullanilir. Four-way ve offset kavsaklarda iki asamali sinyal fazlari gosterilir: NS green, NS transition, EW green ve EW transition. Signal phase paneli aktif fazi gosterir.

SIMULASYON ZAMANI
Replay time, SUMO'nun saniye cinsinden simulasyon saatidir. Gercek sabah 08:00 veya aksam 18:00 davranisi route dosyasindaki talep dagilimi ile tanimlanir; viewer bu talebi sonradan uydurmaz.
