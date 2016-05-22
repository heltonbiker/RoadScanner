#!/usr/bin/env python
# coding: utf-8

def decodePolylineInteger(point_str):

    coord_chunks = [[]]

    for char in point_str:
        value = ord(char) - 63

        split_after = not (value & 0x20)
        value &= 0x1F

        coord_chunks[-1].append(value)

        if split_after:
                coord_chunks.append([])

    del coord_chunks[-1]

    coords = []

    for coord_chunk in coord_chunks:
        coord = 0

        for i, chunk in enumerate(coord_chunk):
            coord |= chunk << (i * 5)

        if coord & 0x1:
            coord = ~coord
        coord >>= 1

        coords.append(coord)

    points = []
    prev_x = 0
    prev_y = 0
    for i in xrange(0, len(coords) - 1, 2):
        if coords[i] == 0 and coords[i + 1] == 0:
            continue

        prev_x += coords[i + 1]
        prev_y += coords[i]

        x = prev_x
        y = prev_y

        point = (y, x)
        
        points.append(point)
    return points


if __name__ == '__main__':
    print decodePolyline('_p~iF~ps|U_ulLnnqC_mqNvxq`@')