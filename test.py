"""
.. warning::
   Make sure tests are updated when adding or removing stuff

.. note::
   Requires ``pytest``

Run through pytest::

   pytest test.py
"""
import pytest

import emc
from emc.async_ import get_data


class TestData:
    """Tests for retrieving data"""
    def test_data(self):
        """Test of :func:`emc.util.get_data`"""
        data = emc.util.get_data()
        assert isinstance(data, tuple)
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_data_async(self):
        """
        Test of :func:`emc.async_.get_data`

        .. note::
           Requires ``pytest-asyncio``
        """
        data = await get_data()
        assert isinstance(data, tuple)
        assert len(data) == 2


class TestResident:
    """Tests for :class:`emc.Resident`"""
    def test_resident(self):
        """Test of :class:`emc.Resident`"""
        res = emc.Resident("TheSuperGamer205")
        assert res.name == "TheSuperGamer205"
        assert str(res) == res.name
        assert res.town.name == "Dharug"
        assert res.nation.name == "Sudan"
        assert isinstance(res.online, bool)
        assert isinstance(res.hidden, bool)
        assert isinstance(res.position, tuple)
        assert len(res.position) == 3

    def test_all_residents(self):
        """Test of :meth:`emc.Resident.all`"""
        res = emc.Resident.all()
        assert isinstance(res, set)
        assert len(res) > 50

    def test_all_online_residents(self):
        """Test of :meth:`emc.Resident.all_online`"""
        res = emc.Resident.all_online()
        assert isinstance(res, set)
        assert len(res) > 25


class TestTown:
    """Tests for :class:`emc.Town`"""
    def test_town(self):
        """Test of :class:`emc.Town`"""
        town = emc.Town("Dharug")
        assert town.name == "Dharug"
        assert str(town) == town.name
        assert town.nation.name == "Sudan"
        assert town.mayor.name == "TheSuperGamer205"
        assert isinstance(town.flags, dict)
        assert not any([flag not in town.flags for flag in ("pvp", "mobs", "explosions", "fire", "capital")])
        assert isinstance(town.colour, str)
        assert len(town.colour) == 7
        assert town.colour == town.nation.colour
        assert isinstance(town.residents, set)
        assert len(town.residents) > 0

    def test_all_towns(self):
        """Test of :meth:`emc.Town.all`"""
        towns = emc.Town.all()
        assert isinstance(towns, set)
        assert len(towns) > 50


class TestNation:
    """Tests for :class:`emc.Nation`"""
    def test_nation(self):
        """Test of :class:`emc.Nation`"""
        nation = emc.Nation("Sudan")
        assert nation.name == "Sudan"
        assert str(nation) == nation.name
        assert nation.leader.name == "TheSuperGamer205"
        assert nation.capital.name == "Dharug"
        assert nation.leader == nation.capital.mayor
        assert len(nation.colour) == 7
        assert nation.colour == nation.capital.colour
        assert isinstance(nation.towns, set)
        assert len(nation.towns) > 0
        assert isinstance(nation.citizens, set)
        assert len(nation.citizens) > 0

    def test_all_nations(self):
        """Test of :meth:`emc.Nation.all`"""
        nations = emc.Nation.all()
        assert isinstance(nations, set)
        assert len(nations) > 50
