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

"""Profession skill IDs, maps, and related data."""

professionMap = {
    "alchemy": [3101, 3464, 11611, 28596, 2259, 28677, 28675, 28672, 51304],
    "enchanting": [13262, 7412, 7413, 13920, 28029, 7411, 51313],
    "engineering": [4037, 4038, 12656, 30350, 4036, 20219, 20222, 51306],
    "blacksmithing": [
        9788,
        3100,
        3538,
        9785,
        29844,
        2018,
        17041,
        17040,
        17039,
        9787,
        51300,
    ],
    "jewelcrafting": [25230, 28894, 28895, 28897, 25229, 31252, 51311],
    "leatherworking": [10656, 10658, 3104, 3811, 10662, 32549, 2108, 10660, 51302],
    "tailoring": [26798, 26801, 26797, 3909, 3910, 12180, 26790, 3908, 51309],
    "cooking": [2550, 3102, 3413, 18260, 33359, 51296],
    "firstaid": [3274, 3273, 7924, 10846, 27028, 45542],
    "herbalism": [2366, 2368, 3570, 11993, 28695, 50300],
    "mining": [2575, 2576, 3564, 10248, 29354, 50310],
    "skinning": [8613, 8617, 8618, 10768, 32678, 50305],
    "inscription": [45357, 45358, 45359, 45360, 45361, 45363],
}
all_prof_skill_ids = [v1 for v in professionMap.values() for v1 in v]

professionSkillMap = {
    "alchemy": 171,
    "enchanting": 333,
    "engineering": 202,
    "blacksmithing": 164,
    "jewelcrafting": 755,
    "leatherworking": 165,
    "tailoring": 197,
    "cooking": 185,
    "firstaid": 129,
    "herbalism": 182,
    "mining": 186,
    "skinning": 393,
    "inscription": 773,
}

professionSpellMap = {
    0: {
        "alchemy": 11611,
        "enchanting": 13920,
        "engineering": 12656,
        "blacksmithing": 9785,
        "leatherworking": 10662,
        "tailoring": 12180,
        "cooking": 18260,
        "firstaid": 10846,
        "mining": 10248,
        "skinning": 10768,
        "herbalism": 11993,
    },
    1: {
        "alchemy": 28596,
        "enchanting": 28029,
        "engineering": 30350,
        "blacksmithing": 29844,
        "jewelcrafting": 28897,
        "leatherworking": 32549,
        "tailoring": 26790,
        "cooking": 33359,
        "firstaid": 27028,
        "mining": 29354,
        "skinning": 32678,
        "herbalism": 28695,
    },
    2: {
        "alchemy": 51304,
        "enchanting": 51313,
        "engineering": 51306,
        "blacksmithing": 51300,
        "jewelcrafting": 51311,
        "leatherworking": 51302,
        "tailoring": 51309,
        "cooking": 51296,
        "firstaid": 45542,
        "mining": 50310,
        "skinning": 50305,
        "herbalism": 50300,
        "inscription": 45363,
    },
}

