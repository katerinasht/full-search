import tempfile
from get_spn import get_spn
import pygame
import requests

def pygame_visual(toponym_longitude, toponym_lattitude):
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    spn = get_spn(corners)
    points = []
    text = ""
    l = "map"
    show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                try:
                    if event.key == pygame.K_PAGEUP:
                        spn[0] = str(float(spn[0]) + 0.05)
                        spn[1] = str(float(spn[1]) + 0.05)
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                    elif event.key == pygame.K_PAGEDOWN:
                        spn[0] = str(float(spn[0]) - 0.05)
                        spn[1] = str(float(spn[1]) - 0.05)
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                    elif event.key == pygame.K_UP:
                        toponym_lattitude = str(float(toponym_lattitude) + 0.05)
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                    elif event.key == pygame.K_DOWN:
                        toponym_lattitude = str(float(toponym_lattitude) - 0.05)
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                    elif event.key == pygame.K_RIGHT:
                        toponym_longitude = str(float(toponym_longitude) + 0.05)
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                    elif event.key == pygame.K_LEFT:
                        toponym_longitude = str(float(toponym_longitude) - 0.05)
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                    if len(pygame.key.name(event.key)) == 1:
                        text += to_rus(pygame.key.name(event.key))
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                    elif pygame.key.name(event.key) == "space":
                        text += " "
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                    elif pygame.key.name(event.key) == "backspace" and text != "":
                        text = text[:-1]
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                except Exception:
                    print("Упс! Что-то пошло не так")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 10 and event.pos[0] < 75:
                    if event.pos[1] > 10 and event.pos[1] < 25:
                        l = "map"
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                    elif event.pos[1] > 30 and event.pos[1] < 45:
                        l = "sat"
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                    elif event.pos[1] > 50 and event.pos[1] < 65:
                        l = "sat,skl"
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                if event.pos[0] > 530 and event.pos[0] < 595:
                    if event.pos[1] > 465 and event.pos[1] < 485:
                        toponym_longitude, toponym_lattitude = new_place(text)
                        points.append(",".join([toponym_longitude, toponym_lattitude, "pmlbs"]))
                        text = ""
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
                    if event.pos[1] > 435 and event.pos[1] < 455 and points != []:
                        points = points[:-1]
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude, l, text, points)
    pygame.quit()


def to_rus(text):
    layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                               'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                      "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                      'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
    return text.translate(layout)

def new_place(text):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?"
    response = requests.get(geocoder_request, params={"apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                                                      "geocode": text, "format": "json"})
    if response.ok:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        return str(toponym.split()[0]), str(toponym.split()[1])

def show_map(spn, screen, toponym_longitude, toponym_lattitude, l, text, points):
    geocoder_api_server = "http://static-maps.yandex.ru/1.x/?"
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": spn,
        "l": l,
        "pt": "~".join(points)
    }
    response = requests.get(geocoder_api_server, params=map_params)
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(response.content)
        fp.seek(0)
        screen.blit(pygame.image.load(fp), (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (0, 450, 600, 50))
        pygame.draw.rect(screen, (255, 255, 255), (530, 465, 65, 20))
        font = pygame.font.SysFont(None, 27)
        img = font.render('Искать', True, (0, 0, 0))
        screen.blit(img, (530, 465))
        pygame.draw.rect(screen, (255, 255, 255), (530, 435, 65, 20))
        font = pygame.font.SysFont(None, 27)
        img = font.render('Отмена', True, (0, 0, 0))
        screen.blit(img, (530, 435))
        img = font.render(text, True, (255, 255, 255))
        screen.blit(img, (10, 465))
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, 65, 15))
        font = pygame.font.SysFont(None, 24)
        img = font.render('схема', True, (0, 0, 0))
        screen.blit(img, (10, 10))
        pygame.draw.rect(screen, (255, 255, 255), (10, 30, 65, 15))
        font = pygame.font.SysFont(None, 24)
        img = font.render('спутник', True, (0, 0, 0))
        screen.blit(img, (10, 30))
        pygame.draw.rect(screen, (255, 255, 255), (10, 50, 65, 15))
        font = pygame.font.SysFont(None, 24)
        img = font.render('гибрид', True, (0, 0, 0))
        screen.blit(img, (10, 50))
        pygame.display.flip()


toponym_to_find = "33,44"  # ",".join(input().split())
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    print("Упс! Что-то пошло не так")
else:
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    corners = toponym["boundedBy"]["Envelope"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    pygame_visual(toponym_longitude, toponym_lattitude)

