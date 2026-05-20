import pygame
import random
import winsound

pygame.init()

# الشاشة
genislik = 800
yukseklik = 600

ekran = pygame.display.set_mode((genislik, yukseklik))
pygame.display.set_caption("SUPER CAR GAME")

clock = pygame.time.Clock()

# الألوان
beyaz = (255, 255, 255)
siyah = (0, 0, 0)
sari = (255, 255, 0)
yesil = (0, 255, 0)
kirmizi = (255, 0, 0)
mavi = (0, 120, 255)

# تحميل الصور
araba1 = pygame.image.load("araba.png")
araba2 = pygame.image.load("dusman.png")

# تغيير الحجم
araba1 = pygame.transform.scale(araba1, (80, 120))
araba2 = pygame.transform.scale(araba2, (80, 120))

# الخطوط
font = pygame.font.SysFont(None, 45)
buyuk_font = pygame.font.SysFont(None, 80)

# اختيار السيارة
secili_araba = araba1

# متغيرات
high_score = 0
pause = False
game_over = False
oyun_basladi = False
blur_effect = 0

# المطر
yagmur = []

for i in range(120):

    x = random.randint(0, 800)
    y = random.randint(0, 600)
    hiz = random.randint(5, 15)

    yagmur.append([x, y, hiz])

# إعادة اللعبة
def reset_game():

    global araba_x
    global araba_y
    global dusmanlar
    global puan
    global dusman_hiz
    global game_over

    araba_x = 360
    araba_y = 450

    puan = 0

    dusman_hiz = 7

    dusmanlar = []

    # سيارات الأعداء
    for i in range(3):

        x = random.randint(170, 550)
        y = random.randint(-700, -100)

        dusmanlar.append([x, y])

    game_over = False

reset_game()

# حركة الطريق
yol_kayma = 0

calisiyor = True

while calisiyor:

    clock.tick(60)

    ekran.fill((20, 20, 20))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            calisiyor = False

        if event.type == pygame.KEYDOWN:

            # بداية اللعبة
            if not oyun_basladi and event.key == pygame.K_SPACE:
                oyun_basladi = True

            # اختيار السيارة
            if not oyun_basladi:

                if event.key == pygame.K_1:
                    secili_araba = araba1

                if event.key == pygame.K_2:
                    secili_araba = araba2

            # إعادة التشغيل
            if game_over and event.key == pygame.K_r:
                reset_game()

            # Pause
            if event.key == pygame.K_ESCAPE:
                pause = not pause

    # شاشة البداية
    if not oyun_basladi:

        basla = buyuk_font.render("PRESS SPACE TO START", True, sari)
        ekran.blit(basla, (90, 180))

        secim = font.render("1 RED CAR   |   2 BLUE CAR", True, beyaz)
        ekran.blit(secim, (180, 300))

        pygame.display.update()
        continue

    # Pause
    if pause:

        pause_yazi = buyuk_font.render("PAUSED", True, sari)
        ekran.blit(pause_yazi, (260, 250))

        pygame.display.update()
        continue

    tuslar = pygame.key.get_pressed()

    # رسم الشارع
    pygame.draw.rect(ekran, (70, 70, 70), (150, 0, 500, 600))

    # خطوط الطريق
    yol_kayma += dusman_hiz

    if yol_kayma >= 80:
        yol_kayma = 0

    for y in range(-80, 600, 80):
        pygame.draw.rect(ekran, beyaz, (390, y + yol_kayma, 20, 40))

    # المطر
    for damla in yagmur:

        pygame.draw.line(
            ekran,
            mavi,
            (damla[0], damla[1]),
            (damla[0], damla[1] + 10),
            1
        )

        damla[1] += damla[2]

        if damla[1] > 600:
            damla[1] = 0
            damla[0] = random.randint(0, 800)

    if not game_over:

        hiz = 7

        # نيترو
        if tuslar[pygame.K_LSHIFT]:

            hiz = 14
            blur_effect = 10

            winsound.Beep(500, 10)

        else:
            blur_effect = 0

        # حركة السيارة
        if tuslar[pygame.K_LEFT] and araba_x > 160:
            araba_x -= hiz
            winsound.Beep(200, 10)

        if tuslar[pygame.K_RIGHT] and araba_x < 560:
            araba_x += hiz
            winsound.Beep(200, 10)

        # ظل السيارة
        pygame.draw.ellipse(
            ekran,
            (40, 40, 40),
            (araba_x + 10, araba_y + 100, 60, 20)
        )

        # رسم سيارة اللاعب
        ekran.blit(secili_araba, (araba_x, araba_y))

        # سيارات الأعداء
        for dusman in dusmanlar:

            dusman[1] += dusman_hiz

            if dusman[1] > 700:

                dusman[1] = random.randint(-700, -100)
                dusman[0] = random.randint(170, 550)

                puan += 1

                if puan % 5 == 0:
                    dusman_hiz += 1

                if puan > high_score:
                    high_score = puan

            # ظل العدو
            pygame.draw.ellipse(
                ekran,
                (40, 40, 40),
                (dusman[0] + 10, dusman[1] + 100, 60, 20)
            )

            # رسم سيارة العدو بالصورة
            ekran.blit(araba2, (dusman[0], dusman[1]))

            # التصادم
            if araba_y < dusman[1] + 120 and araba_y + 120 > dusman[1]:
                if araba_x < dusman[0] + 80 and araba_x + 80 > dusman[0]:

                    winsound.Beep(1000, 700)

                    game_over = True

        # تأثير السرعة
        if blur_effect > 0:

            for i in range(5):

                pygame.draw.rect(
                    ekran,
                    (150, 150, 150),
                    (
                        random.randint(150, 650),
                        random.randint(0, 600),
                        2,
                        20
                    )
                )

        # النقاط
        puan_yazi = font.render("Score: " + str(puan), True, yesil)
        ekran.blit(puan_yazi, (20, 20))

        high_yazi = font.render("High: " + str(high_score), True, sari)
        ekran.blit(high_yazi, (20, 60))

    else:

        # انفجار
        for i in range(40):

            pygame.draw.circle(
                ekran,
                random.choice([kirmizi, sari]),
                (
                    araba_x + random.randint(0, 80),
                    araba_y + random.randint(0, 120)
                ),
                random.randint(5, 20)
            )

        ekran.blit(secili_araba, (araba_x, araba_y))

        over = buyuk_font.render("GAME OVER", True, kirmizi)
        ekran.blit(over, (170, 220))

        score = font.render("YOUR SCORE: " + str(puan), True, sari)
        ekran.blit(score, (250, 320))

        restart = font.render("PRESS R TO RESTART", True, beyaz)
        ekran.blit(restart, (210, 390))

    pygame.display.update()

pygame.quit()