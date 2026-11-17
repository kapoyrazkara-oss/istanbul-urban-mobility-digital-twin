# Voice message script for the teacher

## English version (about 60–90 seconds)

Hello, I would like to briefly explain what I developed during this week’s Build stage.

In my previous Learn article, I researched how AI and adaptive traffic signal systems could improve urban transportation, especially in Istanbul. For the Build stage, I turned that research question into a working simulation.

I used Eclipse SUMO, Python, and TraCI to create a four-way intersection with north, south, east, and west approaches. I built two controllers: a fixed-time controller and a traffic-responsive adaptive controller.

The fixed-time controller uses the same signal cycle regardless of traffic. The adaptive controller checks the traffic pressure in each direction and can extend the green phase when one direction has more stopped vehicles.

I tested both controllers in two scenarios: balanced traffic and north-south-heavy traffic. In the balanced scenario, the average waiting time decreased from 12.97 seconds with the fixed controller to 9.76 seconds with the adaptive controller. In the north-south-heavy scenario, it decreased from 15.62 seconds to 10.05 seconds.

These are simulation results, so they do not represent all of Istanbul. However, they support my hypothesis under the tested conditions. I also learned that my current system is rule-based adaptive control, not machine learning yet.

My next step is to add a 3D visualization and then improve the model with pedestrians, public transport, and more realistic traffic scenarios.

Thank you for listening.

## Kısa Türkçe anlamı

Bu hafta önceki Learn makalemdeki araştırma sorusunu çalışan bir simülasyona dönüştürdüğünü anlatıyorsun. SUMO, Python ve TraCI ile dört yönlü kavşak oluşturdun. Sabit zamanlı ve trafik yoğunluğuna duyarlı iki kontrolcü yaptın. İki senaryoda adaptif sistemin bekleme süresini azalttığını ölçtün. Bunun küçük bir simülasyon olduğunu ve henüz makine öğrenmesi kullanmadığını belirtiyorsun. Bir sonraki adımın 3D görselleştirme ve daha gerçekçi trafik unsurları eklemek.

## Kayıt önerisi

Metni hızlı okumak yerine doğal konuş. Yaklaşık 70 saniye sürmesi yeterli. Sayıları söylerken “twelve point ninety-seven seconds” ve “nine point seventy-six seconds” diyebilirsin.
