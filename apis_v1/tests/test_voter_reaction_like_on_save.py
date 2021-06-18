# apis_v1/test_voter_reaction_Like_on_save.py
# Brought to you by We Vote. Be good.
# -*- coding: UTF-8 -*-

from django.urls import reverse
from django.test import TestCase
import json

class WeVoteAPIsV1TestsVoterVoterReactionLikeOnSave(TestCase):
    databases = ["default", "readonly"]

    def setUp(self):
        self.generate_voter_device_id_url = reverse("apis_v1:deviceIdGenerateView")
        self.voter_create_url = reverse("apis_v1:voterCreateView")
        self.voter_reaction_like_on_save_url = reverse("apis_v1:voterReactionLikeOnSaveView")
        