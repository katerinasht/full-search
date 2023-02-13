import tempfile
from get_spn import get_spn
import pygame
import requests

toponym_to_find = ",".join(input().split())
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    pass
json_response = response.json()
corners = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"]
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
geocoder_api_server = "http://static-maps.yandex.ru/1.x/?"
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join(get_spn(corners)),
    "l": "map"
}
response = requests.get(geocoder_api_server, params=map_params)
with tempfile.NamedTemporaryFile() as fp:
    fp.write(response.content)
    pygame.init()
    fp.seek(0)
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(fp), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()