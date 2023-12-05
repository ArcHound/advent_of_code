# 2023-3
import logging
from lib import vector2d

log = logging.getLogger("aoc_logger")

def parse(in_data):
    state = 'blank'
    num = '' 
    num_start = 0
    symbols = list()
    numbers = list()
    c_line = 0
    for line in in_data.splitlines():
        c_char = 0
        for c in line:
            if c in '0123456789' and (state=='blank' or state=='num'):
                num += c
                if state=='blank':
                    num_start=c_char
                state = 'num'
            elif c == '.' and state=='num':
                state = 'blank'
                numbers.append({'points':[(num_start+i, c_line) for i in range(len(num))], 'val':int(num)})
                num = ''
            elif c not in '0123456789.' and state=='blank':
                symbols.append({'point':(c_char,c_line), 'val':c})
                state = 'blank'
            elif c not in '0123456789.' and state=='num':
                symbols.append({'point':(c_char,c_line), 'val':c})
                numbers.append({'points':[(num_start+i, c_line) for i in range(len(num))], 'val':int(num)})
                num = ''
                state = 'blank'
            else:
                pass
            c_char +=1
        if state == 'num':
            numbers.append({'t':'num','points':[(num_start+i, c_line) for i in range(len(num))], 'len':len(num), 'val':int(num)})
            num = ''
            state = 'blank'
        c_line += 1
    return numbers, symbols 

def part1(in_data):
    numbers, symbols = parse(in_data)
    count = 0
    log.debug(numbers)
    for sym in symbols:
        count += sum([num['val'] for num in numbers if any([vector2d.v_nearbysquare(sym['point'],point) for point in num['points']])])
        log.debug(sym)
        log.debug([num['val'] for num in numbers if any([vector2d.v_nearbysquare(sym['point'],point) for point in num['points']])])
        log.debug('--------')
    return count

def part2(in_data):
    numbers, symbols = parse(in_data)
    count = 0
    log.debug(numbers)
    for sym in symbols:
        if sym['val']!='*':
            continue
        nums = [num['val'] for num in numbers if any([vector2d.v_nearbysquare(sym['point'],point) for point in num['points']])]
        if len(nums) == 2:
            count += nums[0]*nums[1]
    return count
