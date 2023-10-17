from django.test import TestCase, SimpleTestCase

from flow.helpers import DigitalGreenCertificateHelper


class GenericDGCTestCase:

    helper = DigitalGreenCertificateHelper

    def setUp(self):
        self.header = self.helper.get_default_header()
        self.key = self.helper.get_random_key()

    def test_encode_decode_verify(self):
        payload = self.helper.dgc_encode(self.data, key=self.key, header=self.header)
        data = self.helper.dgc_decode(payload)
        self.assertEqual(self.data, data["payload"])


class SimplePayloadDGC(GenericDGCTestCase, SimpleTestCase):
    data = {"firstname": "Jean", "lastname": "Landercy", "age": 40, "note": "package owner"}

# class VaccinationDGC(GenericDGCTestCase, SimpleTestCase):
#
#     #              NC instead of 6B (why?)
#     payload = "HC1:6BF/Y4P8QPO0DO3EIUU*H%34OTC%*8KE9%$VV%P6+JG28O%DSX27VJJJS3-FZ+P84Q88SD3QYI39:0VY9IE1 B87SMUL5ACEKNM2/6GPOV97%8P/8K:2UV$G:FS.5N7+0+ E9.KBV56:RGA0GO69%3M MC-R6UM4PDG5R/3PPHKEN5:5DC24-H4OAHOV0TV2JU6A 9XB298AMMU$S5AYJQXC+IMJE19T55YNQ7G663DZTT$PK9ANS02SD9I66YDEDGQUD+VH CB87DEI5ZF0+8BZHIB9IH/9DPHRU58VT+12YTIIP16YG2Q53912IO7358Z9TJU38MS10N90:D0.CC9K1PHFT08DO6X*PRX12:MRYK.-A -BYR61 57GJ ECN57CVEG*14+B*-LKT5$.AX-EEMS+JF5D3STL7U8GEE/RQDBM758I%IYOJ+9DKX4* A1R5$.U29K.RKYURTHDC692DR1$UOM9V:7EHCT9WYMB+MDZ%FB+FPK288VG-1 9MM7PI3VACP4/T*5TTYVXLC6+DJVLTYE7QII801:PD3"
#     data = {'protected_header': b'\xa2\x01&\x04H\x0e\x1b)\x96VcIV', 'unprotected_header': {}, 'payload': {1: 'NL', 4: 1637307800, 6: 1621755800, -260: {1: {'ver': '1.0.0', 'nam': {'fn': 'Achternaam', 'fnt': 'ACHTERNAAM', 'gn': 'Voornaam', 'gnt': 'VOORNAAM'}, 'dob': '1963', 'v': [{'tg': '840539006', 'vp': '1119305005', 'mp': 'CVnCoV', 'ma': 'ORG-100032020', 'dn': 1, 'sd': 6, 'dt': '2021-02-18', 'co': 'GR', 'is': 'Ministry of Health Welfare and Sport', 'ci': 'urn:uvci:01:NL:74827831729545bba1c279f592f2488a'}]}}}, 'signature': b'!\xd7\xdcs<\x139\xea\x9b\x1c;\n\x17\x8e\xdc+\xe3\x14t\x97\x9an\xc9\x1bq\xe8\x020\x0f\x8c\xd1\xe7\xda\xc8 \xc2\x91K\x93\xa7\xac\xf6=E\xd7/\xeb\xecQ>}\xc7\x11\x85ET\x0fy\xf3\x13q\xa9\ng'}

