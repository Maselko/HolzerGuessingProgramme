# -*- coding: utf-8 -*-
"""
Part3.py

a little programme to stop using educated guess

Created on Fri Nov 20 15:28:43 2020

@author: Sebastian Tamon Hascilowicz
"""

import os
import csv
import matplotlib.pyplot as plt


def Holzer(imax, omega, Ks, Is, tq, ang):
    """
    Holzer method rotating system calculator using the equation provided
    in Marine Engineering Lecutre 11 slides.

    Parameters
    ----------
    imax : int
        Number of is. Should be integer
    omega : float
        Natural Frequency
    Ks : list of floats
        List of torsional stiffnecess.
    Is : list of floats
        List of moments of inertia.
    tq : float
        Initial torque value.
    ang : float
        Initial angle displacement.

    Returns
    -------
    angs : List
        List of obtained angular displacements
    tqs : List
        List of obtained torques

    """

    angs = []
    tqs = []
    for i in range(imax):
        angout = ang + (tq / Ks[i])
        tqout = -1 * omega ** 2 * Is[i] * ang + \
            (1 - (omega ** 2) * Is[i] / Ks[i]) * tq
        angs.append(angout)
        tqs.append(tqout)
        ang = angout
        tq = tqout
    return angs, tqs


def iterator(sta, end, d, dep, imax, Ks, Is, tq, ang):
    """
    Recursive function that speeds up the calculation. It is not reccomentded
    to go any further than 14 as it really takes some time to calculate and
    our computer really does not like this...
    """

    if d == dep:
        out = [round(sta, dep)]
        angs, tqs = Holzer(imax, sta, Ks, Is, tq, ang)
        out.append(angs)
        out.append(tqs)
        return out
    else:
        inc = 10 ** (-1 * d)
        i = sta
        while i <= end:
            angs1, tqs1 = Holzer(imax, i, Ks, Is, tq, ang)
            angs2, tqs2 = Holzer(imax, i+inc, Ks, Is, tq, ang)
            if tqs1[imax-1] * tqs2[imax-1] <= 0:
                return iterator(i, i+inc, d+1, dep, imax, Ks, Is, tq, ang)
            i = i + inc


def exporter(data):
    """
    This function returns the data in clean way
    """
    plt.clf()
    topstring = ' f(rad/s)'
    fields = ['Freq(rad/s)']
    for i in range(len(data[0][1])):
        fields.append('theta'+str(i+1))
        topstring = topstring + ' |  theta' + str(i+1)
    for j in range(len(data[0][1])):
        fields.append('torque'+str(j+1))
        topstring = topstring + ' | torque' + str(j+1)
    print(topstring)

    # make line
    line = '-' * len(topstring)
    print(line + '-')

    # makes data
    outer = []
    d = ''
    for k in range(len(data)):
        y = data[k][1]
        d = ' '
        if len(str(data[k][0])) < 7:  # corrects the lengh
            spacenum = 7 - len(str(data[k][0]))
            spaces = ' ' * spacenum
            num = spaces + str(data[k][0])
        else:
            num = str(data[k][0])[:7]
        d = d + ' ' + num
        inner = [data[k][0]]
        x = []
        y = data[k][1]
        for ii in range(len(data[k][1])):
            x.append(ii)
            if len(str(data[k][1][ii])) < 7:  # corrects the lengh
                spacenum = 7 - len(str(data[k][1][ii]))
                spaces = ' ' * spacenum
                num = spaces + str(data[k][1][ii])
            else:
                num = str(data[k][1][ii])[:7]
            d = d + ' | ' + num
            inner.append(data[k][1][ii])
        for iii in range(len(data[k][2])):
            if len(str(data[k][2][iii])) < 7:  # corrects the lengh
                spacenum = 7 - len(str(data[k][2][iii]))
                spaces = ' ' * spacenum
                num = spaces + str(data[k][2][iii])
            else:
                num = str(data[k][2][iii])[:7]
            d = d + ' | ' + num
            inner.append(data[k][2][iii])
        print(d)
        outer.append(inner)
        plt.plot(x, y, label="Omega="+str(data[k][0])[:5])
    plt.style.use('bmh')
    plt.grid(b=True, axis='both')
    plt.legend(loc='best')
    plt.ylabel('Deflection(rad)')

    # if saving is required
    option = input('Save Results? (y/n) :  ')
    if option == 'y':
        directory = os.getcwd()
        name = input('Enter filename :  ')
        form = input('plot type (png/pdf/svg) :  ')
        filename = name + '.csv'
        plotname = name + '.' + form
        with open(filename, 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(outer)
        print(filename + ' saved at ' + directory)
        plt.savefig(plotname, format=form)
        print(plotname + ' saved at ' + directory)


def main():
    """
    Main function

    Returns
    -------
    result : List
        Returns the result for part 3.

    """

    # this get's the maximum value for i
    print('This Programme gets natural frequencies of Shafts using lumped')
    print('parameter method iterating through frequencies.')
    print('')
    print('== Input Parameters ==========================================')
    imax = int(input('Enter max value for i :  '))

    # collects the data
    Is = []
    for i in range(imax):
        In = float(input('Enter I' + str(i+1) + '(kgm^2) :  '))
        Is.append(In)
    Ks = [1]
    for j in range(imax-1):
        K = float(input('Enter k' + str(j+2) + ' (MNm/rad) :  ')) * 10 ** 6
        Ks.append(K)

    tq = 0
    ang = 1

    # analysis setup
    print('')
    print('== Analysis Setup ============================================')
    startk = int(input('Enter start freq (rad/sec):  '))
    endk = int(input('Enter end freq (rad/sec):  '))
    decis = int(input('Enter number of decimal places \
(up to 14) :  '))
    # first loop finds roughly how many zero crossings there are.
    # Then it throws to the iterator wich gets more exact value
    result = []
    k = startk
    while k <= endk:
        angs1, tqs1 = Holzer(imax, k, Ks, Is, tq, ang)
        angs2, tqs2 = Holzer(imax, k+1, Ks, Is, tq, ang)
        if tqs1[imax-1] * tqs2[imax-1] <= 0:
            result.append(iterator(k, k+1, 1, decis, imax, Ks, Is, tq, ang))
        k = k + 1

    # data format and export
    print('')
    print('== Exporter ==================================================')
    exporter(result)


main()
