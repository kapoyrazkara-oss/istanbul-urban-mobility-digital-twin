# Final 3D Urban Mobility Viewer — Plan

## Amaç
SUMO replay verisini İstanbul esintili, düzenlenebilir ve Windows üzerinde güvenilir biçimde açılan bir 3D dijital ikiz sunumuna dönüştürmek. Viewer, Fixed-Time, Local Adaptive ve Coordinated Adaptive controller'ları aynı 5×5 / 25 sinyalli kavşak ağı üzerinde karşılaştırır.

## Uygulama yaklaşımı
- `viewer.html`: Three.js ile tamamen prosedürel 3D sahne; harici GLB zorunluluğu yok.
- `data/*.json`: Var olan gerçek SUMO replay dosyalarının yerel kopyaları.
- `vendor/`: Three.js ve OrbitControls yerel kopyaları; CDN/cache bağımlılığı yok.
- `START_FINAL_3D.bat`: Windows'ta klasörü HTTP server ile servis eder ve Chrome'u açar.
- `server.py`: Port çakışması durumunda boş bir yerel port seçen, dosya sunan basit launcher.

## Tasarım

### Stil seçenekleri
- Editorial urban-tech control room (olasılık 0.04)
- Istanbul night mobility atlas (olasılık 0.06)
- Generic neon cyberpunk (olasılık 0.03)

Seçilen yön: **Istanbul night mobility atlas**.

### Design movement
Koyu asfalt üzerinde sıcak İstanbul ışıkları, sakin deniz/yeşil alan tonları ve veri paneli için soğuk cam yüzeyler. Görsel dil “oyuncak şehir” değil, ölçülebilir bir araştırma demonstratörü hissi verecek.

### Core principles
1. Sahne önce okunabilir olacak: yollar ve 25 kavşak net ayrışacak.
2. Dekor, veri akışını örtmeyecek; binalar ve ağaçlar düşük kontrastta kalacak.
3. Işık rengi controller durumunu doğrudan anlatacak.
4. Her paneldeki sayı replay metadata'sından gelecek; uydurma KPI gösterilmeyecek.

### Renk felsefesi
Asfalt lacivert-slate, yol şeritleri soluk kum rengi, zemin koyu zeytin, deniz petrol mavisi. Adaptive controller sıcak amber/cyan vurgularla, Fixed-Time ise daha nötr kırmızı/amber sinyal durumlarıyla ayrılacak.

### Layout paradigm
Sahne ekranın ana alanını kaplar; sol üstte açıklama ve controller seçimi, sağ üstte replay telemetry, altta küçük bir queue grafiği ve 5×5 heatmap bulunur. Kamera serbest orbit ve preset görünüşler sunar.

### Signature elements
- 25 kavşağın üzerinde küçük isim plakaları.
- Her kavşakta dört kollu gerçekçi sinyal direği ve emissive lambalar.
- İstanbul referansı olarak sahil şeridi, kule/landmark ve yoğun yapı adaları.

### Interaction philosophy
Kullanıcı önce sahneyi izler, sonra controller düğmesiyle aynı zaman akışını değiştirir. Kamera orbit, zoom, reset, hız ve duraklatma kontrolleri sunar. Kavşağa tıklamak o kavşağı vurgular.

### Animation
Araçlar replay frame'lerine göre hareket eder. Kamera otomatik dönmez; sunum sırasında kontrol kullanıcıda kalır. Sinyal emissive renkleri frame değiştikçe güncellenir. UI kartları sabit ve sakin kalır.

### Typography system
Başlıklarda system sans / Arial ağırlıklı kompakt grotesk, metriklerde monospace kullanılır. Büyük başlıklar kısa tutulur; yardımcı açıklamalar 11–12px aralığında okunaklıdır.

### Brand essence
Ölçülebilir adaptive-signal deneyini 3D şehir bağlamında gösteren araştırma viewer'ı. Kişilik: teknik, sakin, ikna edici.

## Proje yapısı
- `viewer.html`: UI, scene graph, procedural assets, replay loop.
- `data/`: `v2_fixed.json`, `v2_local.json`, `v2_coordinated.json`.
- `vendor/`: Three.js runtime ve OrbitControls.
- `server.py`: yerel HTTP serving.
- `START_FINAL_3D.bat`: Windows tek tıklama başlangıcı.
- `README_FINAL_3D.txt`: kullanıcı kurulumu ve düzenleme notları.
