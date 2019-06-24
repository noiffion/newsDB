#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import decimal
import psycopg2

# ------------------------------------------------------------------------------


def create_view(sql):
    """Creates a View in the database"""
    dbase = psycopg2.connect(dbname='news')
    cr = dbase.cursor()
    cr.execute(sql)
    dbase.commit()
    dbase.close()


def ps_query(sql):
    """Returns a query from the news database"""
    dbase = psycopg2.connect(dbname='news')
    cr = dbase.cursor()
    cr.execute(sql)
    sql_output = cr.fetchall()
    dbase.close()
    return sql_output

# ------------------------------------------------------------------------------


def carry_on():
    '''Waiting for user input ('Enter') to continue'''
    carryOn = '[Press Enter to continue!]'
    carryOn = italics.format(carryOn)
    input('\n\n\n\t\t\t\t\t\t\t\t{0}'.format(carryOn))


def clear():
    '''Clears the terminal screen'''
    os.system('clear')

# ------------------------------------------------------------------------------


# text decoration variables:
italics = '\033[3;37;40m{0}\033[0m'
blinking = '\033[5;37;40m{0}\33[0m'
yellow = '\033[0;33;40m{0}\033[0m'
red = '\033[0;31;40m{0}\033[0m'


clear()
print('\n\n\n\n\tHi there,')
print('\n\tThis program will help you answer three questions by querying')
print('\tthe news database.')

carry_on()
text = 'Loading data, please wait...'
text = blinking.format(text)
print('\n{0}\n'.format(text))
time.sleep(1)

# Creating the four Views necessary for the questions see README.md
for i in range(4):
    with open('Queries/View_{0}.txt'.format(i+1), 'r') as f:
        create_view(f.read())
        print('{0}. view created'.format(i+1))
time.sleep(1)

#
# Uncomment the 4 lines below if want to see the (unformatted) four views
# views = ['hit_per_page', 'authors_articles', 'ok_200', 'error_404']
# for i in views:
#     print(ps_query("SELECT * FROM {0};".format(i)))
#     print()
#

# ------------------------------------------------------------------------------


def main(t, n):
    '''Clears the screen and displays the three questions. Takes two parameters:
       t -> time delay in secs, n -> colorize nth question'''

    clear()
    print('\n\t\t\t\t  The questions are:')
    print('\t\t\t\t ˘˘˘˘˘˘˘˘˘˘˘˘˘˘˘˘˘˘˘˘\n')

    for i in range(3):
        time.sleep(t)
        if (i+1) == n:
            quest = yellow.format(questions[i])
            print('\t\t{0}\n'.format(quest))
        else:
            print('\t\t{0}\n'.format(questions[i]))

    time.sleep(t)
    print('_'*94)

    if t >= 0.5:
        time.sleep(t-0.5)
    print('\n  For which one do you want the answer?')

# ------------------------------------------------------------------------------


def max_len(header, output):
    '''From a list of tuples of equal element number returns a list with the len
       of the longest element at the same position of the tuples -> we iterate
       vertically (column) not horizontally (row) and check the length of
       the headers too'''

    mxl = []
    for j in range(len(output[0])):  # lst[0] -> all tuples are of equal size
        mxm = 0
        for i in range(len(output)):
            if mxm < len(str(output[i][j])):  # j fix, i is incr -> vertical
                mxm = len(str(output[i][j]))
        mxl.append(mxm)

    for i in range(len(header)):
        if mxl[i] < (len(header[i])):  # check if header is wider than contents
            mxl[i] = (len(header[i]))

    return mxl


def th_sep(n):
    '''Creates thousand separator commas recursively'''
    if len(n) <= 3:
        return n
    elif len(n) % 3 == 1:
        return n[:1] + ',' + th_sep(n[1:])
    elif len(n) % 3 == 2:
        return n[:2] + ',' + th_sep(n[2:])
    else:
        return n[:3] + ',' + th_sep(n[3:])


def print_table(h, o):
    '''Takes a list of headers, and the list of output back from the SQL query
       and prints the table adjusted for width'''

    mxl = max_len(h, o)  # list of largest widths per column
    header = []
    headlength = []
    headline = []
    for i in range(len(h)):
        header.append(' ' + ' ' * ((mxl[i]-len(h[i]))//2) + h[i] +
                      ' ' * (mxl[i]-(((mxl[i]-len(h[i]))//2)+len(h[i]))) + ' ')
        headlength.append(len(header[i]))
        headline.append('-' * headlength[i])
    print('\n{0}'.format('|'.join(header)))
    print('{0}'.format('+'.join(headline)))

    output = []
    for a in range(len(o)):
        line = []
        for j in range(len(o[a])):
            whole = isinstance(o[a][j], int)
            dec = isinstance(o[a][j], decimal.Decimal)
            if whole or dec:  # numbers are aligned to the right
                numb = th_sep(str(o[a][j]))
                line.append(' ' * (headlength[j] - len(numb)-1) +
                            str(numb) + ' ')
            else:  # everything else is on the left side
                text = str(o[a][j])
                line.append(' ' + text + ' ' * (headlength[j] -
                            len(text)-1))
        output.append('{0}'.format('|'.join(line)))
    for o in output:
        print(o)


def answer(a, query_file, question, header):
    '''Displays the formatted output of the question (sql query)'''
    main(0, int(a))
    question = yellow.format(question)
    print('\n\n\t {0}'.format(question))
    with open(query_file, 'r') as f:
        output = ps_query(f.read())
        print_table(header, output)
    carry_on()
    main(0, 0)

# ------------------------------------------------------------------------------


query_files = ['Queries/1.txt',
               'Queries/2.txt',
               'Queries/3.txt']

questions = ['(1) What are the most popular three articles of all time?',
             '(2) Who are the most popular article authors of all time?',
             '(3) On which days did more than 1% of requests lead to errors?']

headers = {'1': ['id', 'title', 'page_view', 'slug'],
           '2': ['author', 'total_pageview'],
           '3': ['dd-mm-yyyy', 'error_ratio_pct']}

main(1, 0)

quit = False
while not quit:
    answ = input('\nPlease choose a question by hitting a number (1, 2 or 3) '
                 'or press "q" to quit: ')

    if answ == '1':
        answer(answ, query_files[0], questions[0], headers['1'])
    elif answ == '2':
        answer(answ, query_files[1], questions[1], headers['2'])
    elif answ == '3':
        answer(answ, query_files[2], questions[2], headers['3'])

    elif answ.lower() == 'q':
        time.sleep(0.2)
        text = '[Goodbye.]'
        text = italics.format(text)
        print('\n\n\t\t\t\t\t\t\t\t\t\t   {0}'.format(text))
        quit = True

    else:
        clear()
        text = 'Wrong input!'
        text = red.format(text)
        print('\n\n\t{0}'.format(text))
        print('  You should press "1", "2" or "3" (or "q") and Enter when '
              'choosing a question!\n')
        carry_on()
        main(0, 0)

