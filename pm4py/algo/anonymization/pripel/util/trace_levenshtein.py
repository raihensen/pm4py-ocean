'''
    PM4Py – A Process Mining Library for Python
Copyright (C) 2024 Process Intelligence Solutions UG (haftungsbeschränkt)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see this software project's root or
visit <https://www.gnu.org/licenses/>.

Website: https://processintelligence.solutions
Contact: info@processintelligence.solutions
'''
# This algorithm was copied at 16/Nov/2018 from
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python and applied to activity
# sequences
delimiter = "@"


def length(s):
    return s.count(delimiter) + 1


def enumerateSequence(s):
    list = s.split(delimiter)
    return enumerate(list, 0)


def trace_levenshtein(s1, s2):
    if length(s1) < length(s2):
        return trace_levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if length(s2) == 0:
        return length(s1)

    previous_row = range(length(s2) + 1)
    for i, c1 in enumerateSequence(s1):
        current_row = [i + 1]
        for j, c2 in enumerateSequence(s2):
            insertions = previous_row[
                             j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]
