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

import logging

import click

from urllib import request
from urllib.error import HTTPError

from rdoclient import RandomOrgClient

import util

# from config import PROJECT_ROOT
from config import DEBUG
from config import WORDLIST_LONG, WORDLIST_SHORT
from config import API_KEY, CHARACTERS

logging.basicConfig(format='%(levelname)s %(message)s')


# 'click' is Python tool for making clean CLIs
@click.command()
@click.argument('data_type', required=True)
@click.argument('how_many', required=False)
@click.option('-n', '--number-rolls', default=5,
              help="Number of times you want to roll the dice.")
@click.option('-l', '--password-length', default=20,
              help="Password length: default 20. "
                   "Enter number for `mixed` or `numbers` type.")
def generate_password(number_rolls, how_many=1, data_type='words',
                      password_length=20):
    """
    Generate a password or passphrase with either random characters, words,
    or numbers. Optionally, choose number of dice rolls for passphrase
    word selection. See https://www.eff.org/dice.\n
    Returns unencrypted passphrase or password.
    
    \b
    Keyword arguments:
        data_type: words, mixed, numbers
        how_many: how many passwords do you want
    """

    roc = RandomOrgClient(API_KEY)

    chars = CHARACTERS
    tmp_length = password_length
    factor = 1

    number_rolls = validate_count(number_rolls)

    if int(password_length) > 20:

        remainder = int(password_length) % 20
        factor = int(password_length) // 20
        tmp_length = 20

        print('temp length: {0}\nfactor: {1}\nremainder: {2}'.format(
            tmp_length,
            factor,
            remainder)
        )

        # TODO -- Append `remainder` worth characters onto password

    number_list = roll_dice()
    chunked_list = list(chunks(number_list, number_rolls))

    if DEBUG is True:
        import pprint
        pprint.pprint(chunked_list)

    if data_type == 'words':

        if number_rolls == 4:
            word_list = WORDLIST_SHORT

        else:
            word_list = WORDLIST_LONG

        try:
            # Initialize list, dict, and variable
            super_list = []
            super_dict = {}
            passphrase = ''

            # with open(word_list, 'r') as words:
            #     lines = words.readlines()
            #     for line in lines:

            for line in request.urlopen(word_list):

                l = line.decode()
                d = {int(l.split('\t')[0]):l.split('\t')[1].strip('\n')}
                super_list.append(d)

            for k in set(k for d in super_list for k in d):
                for d in super_list:
                    if k in d:
                        super_dict[k] = d[k]

            for chunk in chunked_list:
                n = int(''.join(map(str, chunk)))
                passphrase += '{0} '.format(super_dict[n])

            print(passphrase)

        except HTTPError as e:
            logging.error('[{0}] {1}'.format(util.get_timestamp(), e))

    elif data_type == 'numbers':
        chars = '1234567890'
        print(''.join(roc.generate_strings(factor * how_many,
                                           tmp_length,
                                           chars)))

    else:
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
    """

    roc = RandomOrgClient(API_KEY)

    return roc.generate_integers(number_rolls * number_dice, 1, number_sides)


def chunks(input_list, size):

    """Yield successive n-sized chunks from input_list.
    
    :param input_list: list you want to chunk
    :param size: size of chunks
    """

    for i in range(0, len(input_list), size):
        yield input_list[i:i + size]


def validate_count(value):

    # Use `set` ({x, y, z}) here for quickest result
    if value not in {4, 5}:
        raise click.BadParameter(
            'Word list limitation means that dice rolls can only be 4 or 5.'
        )

    return value


# main call to command line function
if __name__ == '__main__':

    generate_password()
