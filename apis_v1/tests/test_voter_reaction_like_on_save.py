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
    
    def test_save_with_no_voter_device_id(self):
        response = self.client.post(self.voter_reaction_like_on_save_url)
        json_data = json.loads(response.content.decode())
        
        self.assertEqual('status' in json_data, True, "status expected in the json response, and not found")
        self.assertEqual('voter_device_id' in json_data, False,
                         "False expected for voter_device_id in the voterReactionLikeOnSaveView json response, and not found")
        
        self.assertEqual(json_data['status'].strip(), 
                        "VALID_VOTER_ID_MISSING",
            "status: {status} ('VALID_VOTER_ID_MISSING' expected)".format(status=json_data['status']))
            
        self.assertEqual(json_data['success'], 
                        False,
            "success: {success} ('False' expected)".format(success=json_data['success']))
    
    