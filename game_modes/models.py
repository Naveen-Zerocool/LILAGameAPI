from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from LILAGameAPI.base_model import GlobalBaseModel
from LILAGameAPI.utils import get_current_date_time_in_utc


class AreaCode(GlobalBaseModel):
    area_code = models.PositiveSmallIntegerField(validators=[
            MaxValueValidator(999),
            MinValueValidator(000)
        ], unique=True, help_text="3 digit Area Code")

    def __str__(self):
        return f"{self.area_code}"

    class Meta(GlobalBaseModel.Meta):
        verbose_name = "Area Code"
        verbose_name_plural = "Area Codes"
        db_table = "area_codes"


class GameMode(GlobalBaseModel):
    name = models.CharField(max_length=100, help_text="Game Mode Name")

    def __str__(self):
        return self.name

    @staticmethod
    def get_game_mode_by_pk(game_mode_id):
        """
        Used to get an GameMode by passing pk
        :param game_mode_id: UUID
        :return: GameMode
        """
        return GameMode.objects.filter(pk=game_mode_id).first()

    @staticmethod
    def get_all_active_game_modes():
        """
        Used to return all active Game Modes. Filtering will happen at manager level based on is_active field
        :return: GameMode queryset
        """
        return GameMode.objects.all()

    class Meta(GlobalBaseModel.Meta):
        verbose_name = "Game Mode"
        verbose_name_plural = "Game Modes"
        db_table = "game_modes"


class UserPreference(GlobalBaseModel):
    gamer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    area_code = models.ForeignKey(AreaCode, on_delete=models.PROTECT)
    game_mode = models.ForeignKey(GameMode, on_delete=models.PROTECT)
    area_code_mapped_at = models.DateTimeField()
    game_mode_mapped_at = models.DateTimeField()
    is_current_preference = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.gamer} - {self.area_code} - {self.game_mode}"

    @staticmethod
    def make_active_user_preference_inactive_by_user_id(user_id):
        """
        Used to make active preference inactive
        :param user_id: User PK
        """
        UserPreference.objects.filter(is_current_preference=True, gamer_id=user_id).update(is_current_preference=False)

    @staticmethod
    def get_current_active_preference_by_user(user):
        """
        Used to get active preference instance based on user
        :param user: User
        :return: UserPreference
        """
        return UserPreference.objects.filter(gamer=user, is_current_preference=True).first()

    @staticmethod
    def add_user_preference(gamer, area_code, game_mode):
        """
        Add a new User Preference
        :param gamer: User
        :param area_code: int
        :param game_mode: GameMode
        :return: UserPreference
        """
        UserPreference.objects.filter(is_current_preference=True,
                                      gamer_id=gamer.pk).update(is_current_preference=False)
        area_code, created = AreaCode.objects.get_or_create(area_code=area_code)
        data = {"gamer_id": gamer.pk}
        if area_code:
            data.update({"area_code_id": str(area_code.pk)})
        if game_mode:
            data.update({"game_mode_id": str(game_mode.pk)})
        if area_code:
            data.update({"area_code_mapped_at": get_current_date_time_in_utc()})
        if game_mode:
            data.update({"game_mode_mapped_at": get_current_date_time_in_utc()})
        return UserPreference.objects.create(**data)

    class Meta(GlobalBaseModel.Meta):
        verbose_name = "User Preference"
        verbose_name_plural = "User Preferences"
        db_table = "user_preferences"
