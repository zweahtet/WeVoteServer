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
        self.voter_reaction_like_status_retrieve = reverse("apis_v1:reactionLikeStatusRetrieveView")
    
    def test_save_with_no_voter_device_id(self):
        response = self.client.post(self.voter_reaction_like_on_save_url)
        json_data = json.loads(response.content.decode())
        
        self.assertEqual('status' in json_data, True, "status expected in the json response, and not found")
        self.assertEqual('voter_device_id' in json_data, False,
                         "voter_device_id expected in the voterReactionLikeOnSaveView json response, and not found")
        
        self.assertEqual(json_data['status'].strip(), 
                        "VALID_VOTER_ID_MISSING",
            "status: {status} ('VALID_VOTER_ID_MISSING' expected)".format(status=json_data['status']))
            
        self.assertEqual(json_data['success'], 
                        False,
            "success: {success} ('False' expected)".format(success=json_data['success']))
    
    def test_save_with_voter_device_id(self):
        #######################################
        # Generate the voter_device_id cookie
        response = self.client.get(self.generate_voter_device_id_url)
        json_data = json.loads(response.content.decode())

        # Make sure we got back a voter_device_id we can use
        self.assertEqual('voter_device_id' in json_data, True,
                         "voter_device_id expected in the deviceIdGenerateView json response")
        
        # Now put the voter_device_id in a variable we can use below
        voter_device_id = json_data['voter_device_id'] if 'voter_device_id' in json_data else ''
        
        #######################################
        # Create a voter so we can test retrieve
        response2 = self.client.get(self.voter_create_url, {'voter_device_id': voter_device_id})
        json_data2 = json.loads(response2.content.decode())
        
        self.assertEqual('status' in json_data2, True,
                         "status expected in the voterReactionLikeOnSaveView json response but not found")
        self.assertEqual('voter_device_id' in json_data2, True,
                         "voter_device_id expected in the voterReactionLikeOnSaveView json response but not found")
                         
        # With a brand new voter_device_id, a new voter record should be created
        self.assertEqual(
            json_data2['status'], 'VOTER_CREATED',
            "status: {status} (VOTER_CREATED expected in voterReactionLikeOnSaveView), "
            "voter_device_id: {voter_device_id}".format(
                status=json_data2['status'], voter_device_id=json_data2['voter_device_id']))
                
        #######################################
        # Create a voter like reaction so we can test retrieve
        response2 = self.client.get(self.voter_reaction_like_status_retrieve)
        
        json_data2 = json.loads(response2.content.decode())