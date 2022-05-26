from django.core.cache import cache

from LILAGameAPI.celery import app


@app.task(name="increase_game_mode_counter_for_area_code")
def increase_game_mode_counter_for_area_code(area_code, game_mode):
    value = cache.get(f"{area_code}_{game_mode}")
    if value:
        cache.incr(f"{area_code}_{game_mode}", delta=1)
    else:
        cache.set(f"{area_code}_{game_mode}", 1)


@app.task(name="decrease_game_mode_counter_for_area_code")
def decrease_game_mode_counter_for_area_code(area_code, game_mode):
    value = cache.get(f"{area_code}_{game_mode}")
    if value:
        cache.decr(f"{area_code}_{game_mode}", delta=1)


def get_game_mode_counter_for_area_code(area_code, game_mode):
    return cache.get(f"{area_code}_{game_mode}")
