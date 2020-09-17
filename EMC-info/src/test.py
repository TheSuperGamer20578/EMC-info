import unittest
import EMC
import asyncio
data = None


class DataGet(unittest.TestCase):
    def test_sync(self):
        self.assertIsInstance(data := EMC.get_data(), tuple)

    def test_async(self):
        self.assertIsInstance(asyncio.run(EMC.a_get_data()), tuple)


class Residents(unittest.TestCase):
    def test_resident(self):
        res = EMC.Resident("TheSuperGamer205")
        self.assertEqual(res.name, "TheSuperGamer205")
        self.assertFalse(res.townless)
        self.assertEqual(res.town.name, "Dharug")


class Reliability(unittest.TestCase):
    def test_get_data(self):
        for x in range(100):
            self.assertIsInstance(EMC.get_data(), tuple)

    # def test_async_get_data(self):
    #     for x in range(100):
    #         self.assertIsInstance(asyncio.run(EMC.a_get_data()), tuple)


if __name__ == '__main__':
    unittest.main()
