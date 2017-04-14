#!/usr/bin/env python

"""
Password Generator

MIT License

Copyright (c) 2017 Nick Vincent-Maloney <nicorellius@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import pprint

import click

from urllib import request

from rdoclient import RandomOrgClient

# Try this first, and then use text file as failover
WORDLIST_URL = 'https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt'
API_KEY = '59052bc4-840b-4923-96b7-90332167bc8c'
CHARACTERS = 'abcdefghijklmnopqrstuvwxyz' \
             'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
             '1234567890!@#$%^&*()_+=-?~'


# 'click' is Python tool for making clean CLIs
@click.command()
@click.argument('data_type', required=True)
# @click.option('--out-file', default='output.txt',
#               help="Path and name to output file")
def generate_password(number=1, data_type='words', length=20):
    """
    Function to generate the actual password or passphrase.

    :param data_type: words, mixed, numbers
    :param number: how many passwords do you want
    :param length: default 20, enter number
    :return: string, unencrypted password
    """
    r = RandomOrgClient(API_KEY)

    chars = CHARACTERS

    # TODO -- figure out how to add args for dice in generate password function
    # TODO -- figure out how to add args for dice in generate password function

    number_list = roll_dice()

    if data_type == 'words':
        for line in request.urlopen(WORDLIST_URL):
            # print(line)
            pass

    # print(number_list)

    pprint.pprint(list(chunks(number_list, 5)))
    # pprint.pprint([number_list[i:i + 5] for i in range(1, 6)])

    return r.generate_strings(number, length, chars)


def roll_dice(number_rolls=5, number_dice=5, number_sides=6):
    """
    Get some randomness using random.org API: https://api.random.org

    :param number_sides: choose a die type and number of sides
    :param number_rolls: how many rolls determines how long your password is
    :param number_dice: how many dice do you want to roll
    :return: string, concatenated numbers (consider list?)
    # :return: list, rolled numbers
    """

    r = RandomOrgClient(API_KEY)

    return r.generate_integers(number_rolls * number_dice, 0, number_sides)


def chunks(l, n):

    """Yield successive n-sized chunks from l."""

    for i in range(0, len(l), n):
        yield l[i:i + n]


# main call to command line function
if __name__ == '__main__':

    generate_password()



