#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt, pow, ceil

from collections import Counter

import sys


def parse_header(f):
    return map(int, f.readline().strip().split())


def parse_products(f):
    np = int(f.readline().strip())
    products = map(int, f.readline().strip().split())

    return np, products


def parse_warehouses(f):
    nw = int(f.readline().strip())

    warehouses = []
    for i in range(nw):
        x, y = map(int, f.readline().strip().split())
        ps = map(int, f.readline().strip().split())
        warehouses.append({'x': x, 'y': y, 'ps': ps})

    return nw, warehouses


def parse_orders(f):
    no = int(f.readline().strip())

    orders = []
    for i in range(no):
        x, y = map(int, f.readline().strip().split())
        n = int(f.readline().strip())
        ps = Counter(map(int, f.readline().strip().split()))
        orders.append({'id': i, 'x': x, 'y': y, 'n': n, 'ps': ps})

    return no, orders

def calculate_cost(order, warehouse, payload):
    from binpack import pack

    x, y = order['x'], order['y']
    x_warehouse, y_warehouse = warehouse['x'], warehouse['y']

    distance = ceil(sqrt(pow(x-x_warehouse, 2) + pow(y-y_warehouse, 2)))

    values_to_pack = []
    for key in order['ps'].keys():
        weight = products[key]
        for i in xrange(order['ps'][key]):
            values_to_pack.append((key, weight))
    trips = pack(values_to_pack, payload)

    for trip in trips:
        trip.write_command()

    c = Counter()
    for trip in trips:
        c = c + Counter(map(lambda el: el[0], trip.items))
    cost = sum(c.values()) + (distance * len(trips))

    number_of_turns = len(trips)*2*distance + sum(c.values())
    return cost, number_of_turns, trips


def print_load(f, d_id, w_id, p_id, p_n):
    f.write('{0} L {1} {2} {3}\n'.format(d_id, w_id, p_id, p_n))


def print_deliver(f, d_id, o_id, p_id, p_n):
    f.write('{0} D {1} {2} {3}\n'.format(d_id, o_id, p_id, p_n))


def print_wait(f, d_id, t):
    f.write('{0} W {1}\n'.format(d_id, t))


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]



def do_load(drone_id, warehouse_id, prod_type_id):
    pass

if __name__ == '__main__':
    f = open(sys.argv[1])
    global products

    out = open("tmp.txt", "w")

    rows, cols, drones, turns, payload = parse_header(f)
    np, products = parse_products(f)
    nw, warehouses = parse_warehouses(f)
    no, orders = parse_orders(f)

    result = {}
    for order in orders:
        result[order['id']] = calculate_cost(order, warehouses[0], payload)

    result = sorted(result.items(), key=lambda x: x[1][0])

    for chunk in chunks(result, drones):
        longest_order = max([x[1][1] for x in chunk])
        for i, order in enumerate(chunk):
            for trip in order[1][2]:
                for item, value in trip.c.iteritems():
                    print_load(out, i, 0, item, value)
                for item, value in trip.c.iteritems():
                    print_deliver(out, i, order[0], item, value)                   

            if order[1][1] != longest_order:
                print_wait(out, i, int(ceil(longest_order-order[1][1])))

    out.close()

    # count lines
    file = open("tmp.txt", "r")
    solution = open("win.txt", "w")
    lines = file.readlines()
    solution.write(str(len(lines)) + '\n')
    for line in lines:
        solution.write(line)
    solution.close()






    # print '{0} rows, {1} columns, {2} drones, {3} turns, max payload is {4}u'.format(rows, cols, drones, turns, payload)

    # print 'There are {0} different product types.'.format(np)
    # print 'The product types weigh: {0}.'.format(', '.join(str(p) + 'u' for p in products))

    # print 'There are {0} warehouses.'.format(nw)
    # for i, w in enumerate(warehouses):
    #     print 'Warehouse #{0} is located at [{1}, {2}].'.format(i, str(w['x']), str(w['y']))
    #     print 'It stores {0}.'.format(' and '.join(str(i) + ' of product ' + str(p) for i, p in enumerate(w['ps'])))

    # print 'There are {0} orders.'.format(no)
    # for i, o in enumerate(orders):
    #     print 'Order #{0} to be delivered to [{1}, {2}].'.format(i, str(o['x']), str(o['y']))
    #     print 'Order #{0} contains {1} items.'.format(i, str(o['n']))
    #     print 'Items of product types: {0}.'.format(', '.join(map(str, reversed(sorted(o['ps'].elements())))))
