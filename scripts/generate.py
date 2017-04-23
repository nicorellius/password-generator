#!/usr/bin/env python

"""
Dice Roll Optional, Mostly-Random Word, Number, and Mixed Password Generator

[[...DROMoR WoNuM PaG...]]

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

from urllib import request
from urllib.error import HTTPError

import click

import utils
import config


# Set up logging configuration
# TODO: set up proper logging app with handler, formatter, etc...
logging.basicConfig(
    # filename='output.log',
    format='%(levelname)s %(message)s',
    level=logging.DEBUG
)


# 'click' is Python tool for making clean CLIs
@click.command(context_settings=config.CLICK_CONTEXT_SETTINGS['help_options'])
@click.argument('output_type', required=True)
@click.option('-n', '--how-many', 'how_many', default=1)
@click.option('-r', '--number-rolls', default=5,
              help="Number of times you want to roll the dice.")
@click.option('-d', '--number-dice', default=5,
              help="Number of dice you want to roll.")
@click.option('-l', '--password-length', default=20,
              help="Password length: default 20. "
                   "Enter number for `mixed` or `numbers` type.")
def generate_password(number_rolls=5, number_dice=5,
                      how_many=1, output_type='words',
                      password_length=20):
    """
    Generate a password or passphrase with either random characters,
    words, or numbers. Optionally, choose number of dice rolls
    for passphrase word selection. See https://www.eff.org/dice.

    \n
    Returns unencrypted passphrase or password (output type).

    \b
    Available arguments:
        how_many: how many passwords do you want
        output_type: words, mixed, numbers
        number_rolls: (optional) how many times you want to roll the dice
        number_dice: (optional) how many dice you want to roll
        password_length: (optional) length of output type
    """

    # TODO: number of rolls = number of words
    # TODO: number of dice determine which word list

    # roc = "Not connected to Random.org API client..."
    chars = config.CHARACTERS

    factor = 1
    api_max_length = 20
    result = []

    roc = utils.get_roc()

    if output_type == 'words':

        if number_dice == 4:
            word_list = config.WORDLIST_SHORT
            logging.info(
                '[{0}] Using short word list...'.format(utils.get_timestamp()))

        else:
            word_list = config.WORDLIST_LONG
            logging.info(
                '[{0}] Using long word list...'.format(utils.get_timestamp()))

        chunked_list = _prepare_chunks(number_rolls, number_dice)

        try:
            # Initialize list, dict, and variable
            super_list = []
            super_dict = {}
            passphrase = ''

            # with open(word_list, 'r') as words:
            #     lines = words.readlines()
            #     for line in lines:

            for line in request.urlopen(word_list):

                # Take word list and break apart into list
                l = line.decode()
                d = {int(l.split('\t')[0]): l.split('\t')[1].strip('\n')}
                super_list.append(d)

            # Convert list into str and int components
            for k in set(k for d in super_list for k in d):
                for d in super_list:
                    if k in d:
                        super_dict[k] = d[k]

            # Extract the int per roll and map to words for passphrase
            for chunk in chunked_list:
                n = int(''.join(map(str, chunk)))
                passphrase += '{0} '.format(super_dict[n])

            result = passphrase
            password_length = 20

        except HTTPError as e:
            logging.error('[{0}] {1}'.format(utils.get_timestamp(), e))

    elif output_type == 'numbers':
        click.echo(output_type)
        chars = '1234567890'

    else:
        logging.info(
            '[{0}] Output type `mixed` selected...'.format(
                utils.get_timestamp())
        )
        click.echo(chars)

    if password_length < 20:
        result = ''.join(roc.generate_strings(factor * how_many,
                                              password_length, chars))

    elif password_length > 20:
        result = _concatenate_remainder(roc, chars, password_length,
                                        how_many, api_max_length)

    else:
        # TODO: pull out words into function so we can return result/passphrase
        result = result

    click.echo('\nYour password is: {0}'.format(result))


# TODO: refactor words type into function
def _prepare_chunks(number_rolls, number_dice):

    number_list = _roll_dice(number_rolls, number_dice)
    number_dice = _validate_count(number_dice)
    chunks = list(_chunks(number_list, number_dice))

    if config.DEBUG is True:
        logging.info('[{0}] Chunked list:\n  {1}'.format(
            utils.get_timestamp(), chunks)
        )

    return chunks


def _concatenate_remainder(roc, chars, pw_len,
                           how_many=1, max_length=20):
    """
    API limitation is 20 character string, so if CLI input is longer
    than 20 characters, we must concatenate the string in size of reminder.

    :param roc:
    :param chars:
    :param pw_len:
    :param how_many:
    :param max_length:
    :return: concatenated string
    """

    # TODO: This tmp, tmp2 method is only good for 40 chracters

    tmp, tmp2 = '', ''

    if pw_len > 20:

        # TODO: why int is required in outer scope?
        factor = pw_len // 20  # old version was factor = int(pw_len) // 20
        remainder = pw_len % 20  # old version was factor = int(pw_len) % 20

        if config.DEBUG:
            logging.info(
                '[{0}] factor: {1}, remainder: {2}'.format(
                    utils.get_timestamp(),
                    factor,
                    remainder
                    )
                )

        # if factor > 1:
        tmp = ''.join(roc.generate_strings(how_many, remainder, chars))

        # tmp2 = None

    # for _ in range(0, how_many):
    tmp2 = ''.join(roc.generate_strings(how_many, max_length, chars))

    return '{0}{1}'.format(tmp, tmp2)


def _roll_dice(number_rolls=5, number_dice=5, number_sides=6):
    """
    Get some randomness using random.org API: https://api.random.org

    :param number_sides: choose a die type and number of sides
    :param number_rolls: how many rolls determines how long your password is
    :param number_dice: how many dice do you want to roll
    :return: string, concatenated numbers (consider list?)
    """

    try:
        roc = utils.get_roc()
        return roc.generate_integers(number_rolls * number_dice, 1,
                                     number_sides)

    except (ValueError, AttributeError) as e:
        print(e)


def _chunks(input_list, size):

    """Yield successive n-sized chunks from input_list.
    
    :param input_list: list you want to chunk
    :param size: size of chunks
    """

    for i in range(0, len(input_list), size):
        yield input_list[i:i + size]


def _validate_count(value):
    """
    Validate that count is 4 or 5, because EFF lists
    only work for these number of dice.

    :param value: value to validate
    :return: value after it's validated
    """

    # Use `set` ({x, y, z}) here for quickest result
    if value not in {4, 5}:
        raise click.BadParameter(
            'Words in word lists limit number of dice to 4 or 5.'
        )

    return value


# Main call to command line function
if __name__ == '__main__':

    # options = ['', 'words', 'mixed', 'numbers']

    generate_password()
