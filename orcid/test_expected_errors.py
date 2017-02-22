import OrcidBaseTest
import pyjavaproperties

class ExpectedErrors(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test.properties'))
        self.orcid_props           = p
        self.client_id             = self.orcid_props['memberClientId']
        self.client_secret         = self.orcid_props['memberClientSecret']        
        self.code                  = self.orcid_props['api1PostUpdateCode']
        self.orcid_id              = self.orcid_props['orcidId']
        self.wrong_orcid_id        = '0000-0002-2619-0514'
        self.wrong_source_id       = '0000-0001-9434-598X'
        self.access,self.refresh   = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
        self.code2                 = self.orcid_props['api2PostUpdateCode']
        self.access2,self.refresh2 = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code2)        
        
    def test_access_wrong_record1(self):
        # TEST 112
        curl_params = ['-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma_work.xml', '-L', '-i', '-k', '-X', 'POST']
        response = self.orcid_curl("http://api.qa.orcid.org/v1.2/" + self.wrong_orcid_id + "/orcid-works", curl_params)
        self.assertTrue("403 Forbidden" in response, "response: " + response)        
        
    def test_access_wrong_record2(self):
        # TEST 113
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma2_work.xml', '-L', '-i', '-k', '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v2.0/" + self.wrong_orcid_id + "/work", curl_params)
        self.assertTrue("401 Unauthorized" in response, "Non 401 returned: " + response)
        
    def test_access_record2_without_token(self):
        # TEST 114
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma2_work.xml', '-L', '-i', '-k', '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v2.0/" + self.orcid_id + "/work", curl_params)
        self.assertTrue("403 Forbidden" in response, "Non 401 returned: " + response)
        
    def test_update_record2_without_token(self):
        # Post the ma test work 2
        response = self.post_activity("work", "ma2_work.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = str(self.get_putcode_from_response(response)).strip()
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # Update the work with JSON
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = "{'put-code':'%s','title':{'title':'APITestTitleUpdated'},'type':'JOURNAL_ARTICLE','external-ids':{'external-id':[{'external-id-value':'1234','external-id-type':'doi','external-id-relationship':'SELF'}]}}" %  str(putcode)
        # TEST 115 
        activity_type = "work"
        update_curl_params = ['-i', '-L', '-k', '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-d', updated_data, '-X', 'PUT']
        update_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s/%d" % (self.orcid_id, activity_type, int(putcode)), update_curl_params)
        self.assertTrue("403 Forbidden" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
        # Delete the work
        delete_response = self.delete_activity(putcode, "work")
        self.assertTrue("204 No Content" in delete_response, "Delete Action Response: " + delete_response + " using putcode [%s]" % str(putcode))
        
    def test_update_record2_from_other_source(self):
        # Post the ma test work 2
        response = self.post_activity("work", "ma2_work.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # TEST 116 Update the work with JSON
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode).strip() + ',"title":{"title":"APITestTitleUpdated"},"type":"JOURNAL_ARTICLE","external-ids":{"external-id":[{"external-id-value":"1234","external-id-type":"doi","external-id-relationship":"SELF"}]}}'
        update_curl_params = ['-i', '-L', '-k', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-d', updated_data, '-X', 'PUT']
        update_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s/%s" % (self.wrong_source_id, "work", str(putcode).strip()), update_curl_params)
        self.assertTrue("401 Unauthorized" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
        # Delete the work
        delete_response = self.delete_activity(putcode, "work")
        self.assertTrue("204 No Content" in delete_response, "Delete Action Response: " + delete_response + " using putcode [%s]" % str(putcode))
        
    def test_check_access_denied_on_deny(self):
        # TODO simulate
        # https://qa.orcid.org/oauth/authorize?client_id=[memberClientId]&response_type=code&scope=/read-limited /activities/update /orcid-bio/update&redirect_uri=https://developers.google.com/oauthplayground
        # click deny
        self.assertTrue(True)

        
                