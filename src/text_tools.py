#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unicodedata


symbols_to_space = re.compile(u"[/\|\n(\; )|(\: )|( \()|(\) )|( \")|(\" )|( \')|(\' )]")
symbols_to_remove = re.compile(u"[\"\'\$\€\£\(\)\:\[\]\.\,]")
space_repetition = re.compile(u" {2,}")


def strip_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


def canonize_language(text):
    text = strip_accents(str(text).strip().lower())
    text = symbols_to_space.sub(" ", str(text))
    text = symbols_to_remove.sub("", str(text))
    text = space_repetition.sub(" ", str(text))
    return str(text)


def simple_tokenizer(text, min_token_length=0):
    tokens = text.split(" ")
    if min_token_length > 0:
        tokens = list(filter(lambda x: len(x) >= min_token_length, tokens))
    return tokens
