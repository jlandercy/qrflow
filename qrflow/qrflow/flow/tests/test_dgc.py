import pprint

from pycose.messages import Sign1Message

from django.test import SimpleTestCase

from flow import helpers


class VerifiableDGCTestCase:

    helper = None
    data = None

    def setUp(self):
        self.header = self.helper.get_header()
        self.key = self.helper.create_new_key()

    def test_signature(self):
        message = Sign1Message(
            phdr=self.header,
            key=self.key,
            payload=b"Some payload"
        )
        encoded = message.encode()
        decoded = Sign1Message.decode(encoded)
        decoded.key = self.key
        self.assertTrue(decoded.verify_signature())

    def test_encode_decode_verify(self):
        payload = self.helper.encode(self.data, key=self.key, protected_header=self.header)
        data = self.helper.decode(payload, key=self.key)
        self.assertEqual(self.data, data["payload"])
        self.assertTrue(data["checked"] and data["verified"])


class SimplePayloadTestCase:
    data = {"firstname": "Jean", "lastname": "Landercy", "age": 40, "note": "package owner"}


class SimplePayloadCoseDGC(VerifiableDGCTestCase, SimplePayloadTestCase, SimpleTestCase):
    helper = helpers.CoseKeyDGCHelper


class SimplePayloadEC2DGC(VerifiableDGCTestCase, SimplePayloadTestCase, SimpleTestCase):
    helper = helpers.EC2KeyDGCHelper


class UnverifiableDGCTestCase:

    helper = helpers.EC2KeyDGCHelper

    def test_decode(self):
        data = self.helper.decode(self.payload, key=None)


class VaccinationDGC(UnverifiableDGCTestCase, SimpleTestCase):

    #              NC instead of 6B (why?)
    payload = "HC1:NCF/Y4P8QPO0DO3EIUU*H%34OTC%*8KE9%$VV%P6+JG28O%DSX27VJJJS3-FZ+P84Q88SD3QYI39:0VY9IE1 B87SMUL5ACEKNM2/6GPOV97%8P/8K:2UV$G:FS.5N7+0+ E9.KBV56:RGA0GO69%3M MC-R6UM4PDG5R/3PPHKEN5:5DC24-H4OAHOV0TV2JU6A 9XB298AMMU$S5AYJQXC+IMJE19T55YNQ7G663DZTT$PK9ANS02SD9I66YDEDGQUD+VH CB87DEI5ZF0+8BZHIB9IH/9DPHRU58VT+12YTIIP16YG2Q53912IO7358Z9TJU38MS10N90:D0.CC9K1PHFT08DO6X*PRX12:MRYK.-A -BYR61 57GJ ECN57CVEG*14+B*-LKT5$.AX-EEMS+JF5D3STL7U8GEE/RQDBM758I%IYOJ+9DKX4* A1R5$.U29K.RKYURTHDC692DR1$UOM9V:7EHCT9WYMB+MDZ%FB+FPK288VG-1 9MM7PI3VACP4/T*5TTYVXLC6+DJVLTYE7QII801:PD3"

