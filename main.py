import tempfile
from get_spn import get_spn
import pygame
import requests

def pygame_visual(toponym_longitude, toponym_lattitude):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    spn = get_spn(corners)
    show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude)
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
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude)
                    elif event.key == pygame.K_PAGEDOWN:
                        spn[0] = str(float(spn[0]) - 0.05)
                        spn[1] = str(float(spn[1]) - 0.05)
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude)
                    elif event.key == pygame.K_UP:
                        toponym_lattitude = str(float(toponym_lattitude) + 0.05)
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude)
                    elif event.key == pygame.K_DOWN:
                        toponym_lattitude = str(float(toponym_lattitude) - 0.05)
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude)
                    elif event.key == pygame.K_RIGHT:
                        toponym_longitude = str(float(toponym_longitude) + 0.05)
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude)
                    elif event.key == pygame.K_LEFT:
                        toponym_longitude = str(float(toponym_longitude) - 0.05)
                        show_map(",".join(spn), screen, toponym_longitude, toponym_lattitude)
                except Exception:
                    print("Упс! Что-то пошло не так")
    pygame.quit()


def show_map(spn, screen, toponym_longitude, toponym_lattitude):
    geocoder_api_server = "http://static-maps.yandex.ru/1.x/?"
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": spn,
        "l": "map"
    }
    response = requests.get(geocoder_api_server, params=map_params)
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(response.content)
        fp.seek(0)
        screen.blit(pygame.image.load(fp), (0, 0))
        pygame.display.flip()


toponym_to_find = ",".join(input().split())
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

