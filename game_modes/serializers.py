from rest_framework import serializers

from game_modes.models import GameMode, UserPreference


class GameModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMode
        fields = ["pk", "name"]


class CategorySerializer(serializers.ModelSerializer):
    area_code = serializers.SerializerMethodField()
    game_mode = serializers.SerializerMethodField()

    @staticmethod
    def get_area_code(obj):
        return obj.area_code.area_code if obj.area_code else None

    @staticmethod
    def get_game_mode(obj):
        return obj.game_mode.name if obj.game_mode else None

    class Meta:
        model = UserPreference
        fields = ["area_code", "game_mode"]
