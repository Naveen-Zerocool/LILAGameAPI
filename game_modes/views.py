from rest_framework import status

from LILAGameAPI.base_api_views import AuthenticatedAPIView
from LILAGameAPI.standard_responses import StandardResponse
from LILAGameAPI.utils import required_params
from game_modes.models import UserPreference, GameMode
from game_modes.serializers import CategorySerializer, GameModeSerializer
from game_modes.utils import increase_game_mode_counter_for_area_code, get_game_mode_counter_for_area_code


class GameModeView(AuthenticatedAPIView):

    def get(self, request):
        game_modes = GameMode.get_all_active_game_modes()
        serialized_data = GameModeSerializer(game_modes, many=True).data
        return StandardResponse(response_data=serialized_data,
                                message="Returned all game modes successfully")


class PreferenceView(AuthenticatedAPIView):

    def get(self, request):
        current_preference = UserPreference.get_current_active_preference_by_user(user=request.user)
        if not current_preference:
            return StandardResponse(response_data={}, http_status=status.HTTP_204_NO_CONTENT,
                                    message="Returned user preference successfully")
        serialized_data = CategorySerializer(current_preference).data
        return StandardResponse(response_data=serialized_data,
                                message="Returned user preference successfully")

    @required_params(params=["area_code", "game_mode_id"])
    def post(self, request):
        gamer = request.user
        data = request.data
        area_code = data.get("area_code")
        game_mode_id = data.get("game_mode_id")
        if not (area_code and game_mode_id):
            return StandardResponse(response_data={}, error={"area_code": f"Game Mode and Area Code are mandatory"},
                                    http_status=status.HTTP_400_BAD_REQUEST,
                                    message="Error while adding User Preference")
        game_mode = None
        if game_mode_id:
            game_mode = GameMode.get_game_mode_by_pk(game_mode_id=game_mode_id)
            if not game_mode:
                return StandardResponse(response_data={}, error={"game_mode_id": f"Game Mode not found"},
                                        http_status=status.HTTP_400_BAD_REQUEST,
                                        message="Error while adding User Preference")
        if len(str(area_code)) != 3:
            return StandardResponse(response_data={}, error={"area_code": f"Area code invalid"},
                                    http_status=status.HTTP_400_BAD_REQUEST,
                                    message="Error while adding User Preference")

        user_preference = UserPreference.add_user_preference(gamer=gamer, area_code=area_code, game_mode=game_mode)

        if not user_preference:
            return StandardResponse(response_data={}, http_status=status.HTTP_503_SERVICE_UNAVAILABLE,
                                    message="Adding User Preference Failed")
        increase_game_mode_counter_for_area_code.delay(area_code=area_code, game_mode=game_mode_id)
        serialized_data = CategorySerializer(user_preference).data
        return StandardResponse(response_data=serialized_data,
                                message="Adding User Preference Success")


class InactivePreferenceView(AuthenticatedAPIView):

    def delete(self, request):
        UserPreference.make_active_user_preference_inactive_by_user_id(user_id=request.user.pk)
        return StandardResponse(response_data={},
                                message="Made user preference inactive")


class PopularGameModeView(AuthenticatedAPIView):

    def get(self, request):
        area_code = request.query_params.get("area_code")
        all_gaming_modes = GameMode.get_all_active_game_modes().values("pk", "name")
        data = {"game_mode": {}, "gamers_count": 0}
        for game_mode in all_gaming_modes:
            counter = get_game_mode_counter_for_area_code(area_code=area_code, game_mode=str(game_mode.get("pk")))
            if counter and data.get("gamers_count") < counter:
                data.update({"game_mode": game_mode.get("name"),
                             "gamers_count": counter})
        if not data.get("game_mode"):
            return StandardResponse(response_data={}, http_status=status.HTTP_204_NO_CONTENT,
                                    message="No popular game mode available on your area")
        return StandardResponse(response_data=data,
                                message="Returned popular game mode for area")
