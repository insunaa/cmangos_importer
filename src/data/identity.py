# BSD 3-Clause License.
#
# Copyright (c) 2025, cmangos_importer contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Character identity lookups -- slots, races, classes, factions, starting positions."""

slotMap = {
    "head": 0,
    "neck": 1,
    "shoulder": 2,
    "chest": 4,
    "waist": 5,
    "legs": 6,
    "feet": 7,
    "wrist": 8,
    "hands": 9,
    "finger1": 10,
    "finger2": 11,
    "trinket1": 12,
    "trinket2": 13,
    "back": 14,
    "main_hand": 15,
    "off_hand": 16,
    "relic": 17,
    "tabard": 18,
}

slots = [
    "head",
    "neck",
    "shoulder",
    "shirt",
    "chest",
    "waist",
    "legs",
    "feet",
    "wrist",
    "hands",
    "finger1",
    "finger2",
    "trinket1",
    "trinket2",
    "back",
    "main_hand",
    "off_hand",
    "relic",
    "tabard",
]

startPosMap = {
    0: {
        "horde": ["1629.36", "-4373.4", "31.26", "1"],
        "alliance": ["-8833.38", "628.62", "94", "0"],
    },
    1: {
        "horde": ["-1817.69", "5321.56", "-12.4282", "530"],
        "alliance": ["-1817.69", "5321.56", "-12.4282", "530"],
    },
    2: {
        "horde": ["5804.14", "624.77", "647.8", "571"],
        "alliance": ["5804.14", "624.77", "647.8", "571"],
    },
}

factions = {
    "Human": "alliance",
    "Orc": "horde",
    "Dwarf": "alliance",
    "Night Elf": "alliance",
    "Undead": "horde",
    "Tauren": "horde",
    "Gnome": "alliance",
    "Troll": "horde",
    "Blood Elf": "horde",
    "Draenei": "alliance",
}

races = {
    "Human": 1,
    "Orc": 2,
    "Dwarf": 3,
    "Night Elf": 4,
    "Undead": 5,
    "Tauren": 6,
    "Gnome": 7,
    "Troll": 8,
    "Blood Elf": 10,
    "Draenei": 11,
}

classes = {
    "warrior": 1,
    "paladin": 2,
    "hunter": 3,
    "rogue": 4,
    "priest": 5,
    "shaman": 7,
    "mage": 8,
    "warlock": 9,
    "druid": 11,
    "deathknight": 12,
}

genericPetModelMap = {
    "Bat": 7894,
    "Bear": 706,
    "Boar": 4714,
    "Carrion Bird": 20348,
    "Cat": 9954,
    "Crab": 699,
    "Crocolisk": 2850,
    "Dragonhawk": 20263,
    "Gorilla": 8129,
    "Hyena": 10904,
    "Nether Ray": 20098,
    "Bird of Prey": 10831,
    "Raptor": 19758,
    "Ravager": 20063,
    "Scorpid": 15433,
    "Serpent": 4312,
    "Spider": 17180,
    "Sporebat": 17751,
    "Tallstrider": 38,
    "Turtle": 5027,
    "Warp Stalker": 19998,
    "Wind Serpent": 3204,
    "Wolf": 741,
}
