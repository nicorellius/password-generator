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
# Note that this API key is not secure, and you should request your own!!!
API_KEY = '59052bc4-840b-4923-96b7-90332167bc8c'
CHARACTERS = 'abcdefghijklmnopqrstuvwxyz' \
             'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
             '1234567890!@#$%^&*()_+=-?~'


# 'click' is Python tool for making clean CLIs
@click.command()
@click.argument('data_type', required=True)
@click.argument('password_length', required=True)
@click.option('-n', '--number-rolls', default=5,
              help="Number of times you want to roll the dice.")
def generate_password(number_rolls, how_many=1, data_type='words',
                      password_length=20):
    """
    Generate a password or passphrase with either random characters, words,
    or numbers. Optionally, choose number of dice rolls for passphrase
    word selection. See https://www.eff.org/dice.\n
    Returns unencrypted passphrase or password.
    """

    # Keyword arguments:
    #     data_type: words, mixed, numbers
    #     how_many: how many passwords do you want
    #     password_length: default 20, enter number

    roc = RandomOrgClient(API_KEY)

    chars = CHARACTERS
    tmp_length = password_length
    factor = 1

    if int(password_length) > 20:
        remainder = int(password_length) % 20
        factor = int(password_length) // 20
        tmp_length = 20
        print('temp length: {0}\nfactor: {1}\nremainder: {2}'.format(
            tmp_length, 
            factor,
            remainder)
        )

    # TODO -- figure out how to add args for dice in generate password function
    # TODO -- figure out how to add args for dice in generate password function

    number_list = roll_dice()
    # print(number_list)
    # pprint.pprint(list(chunks(number_list, number_rolls)))
    # pprint.pprint([number_list[i:i + 5] for i in range(1, 6)])

    if data_type == 'words':

        for line in request.urlopen(WORDLIST_URL):
            # print(line)
            pass

        print("This will eventually print passphrase")

    elif data_type == 'numbers':
        chars = '1234567890'

    print(''.join(roc.generate_strings(factor * how_many,
                                       tmp_length,
                                       chars)))


def roll_dice(number_rolls=5, number_dice=5, number_sides=6):
    """
    Get some randomness using random.org API: https://api.random.org

    :param number_sides: choose a die type and number of sides
    :param number_rolls: how many rolls determines how long your password is
    :param number_dice: how many dice do you want to roll
    :return: string, concatenated numbers (consider list?)
    # :return: list, rolled numbers
    """

    roc = RandomOrgClient(API_KEY)

    return roc.generate_integers(number_rolls * number_dice, 0, number_sides)


def chunks(input_list, size):

    """Yield successive n-sized chunks from input_list.
    
    :param input_list: list you want to chunk
    :param size: size of chunks
    """

    for i in range(0, len(input_list), size):
        yield input_list[i:i + size]


# main call to command line function
if __name__ == '__main__':

    generate_password()
