__author__ = 'Nikola Ravnjak'

#Batch and online search algorithms for adaptive neuro-fuzzy inference system (ANFIS)

import math
import random

samples = {}
def load_data():
    for x in xrange(-4, 5):
        for y in xrange(-4, 5):
            z = (((x+2)**2) - ((y-1)**2) + (5 * x * y) - 2) * (math.sin(x/5.0))**2
            samples[(x, y)] = z

load_data()


def fja(x, y):
    return samples[(x, y)]

m = 16
eta = 0.01
a, b, c, d, p, q, r = ([] for i in range(7))

for i in xrange(m):
    a.append(random.randint(1, 5))
    b.append(random.randint(1, 5))
    c.append(random.randint(1, 5))
    d.append(random.randint(1, 5))
    p.append(random.randint(1, 5))
    q.append(random.randint(1, 5))
    r.append(random.randint(1, 5))


def w(i, x, y):
    a = alfa(i, x)
    b = beta(i, y)
    return a*b


def alfa(i, x):
    pom1 = b[i] * (x - a[i])
    pom2 = 1+math.exp(pom1)
    return 1.0 / pom2


def beta(i, y):
    pom1 = d[i] * (y - c[i])
    pom2 = 1+math.exp(pom1)
    return 1.0 / pom2


# sum zi*alfa*beta / sum alfa*beta
def o(x, y):
    num = 0
    denum = 0
    for m_i in xrange(m):
        num += w(m_i, x, y) * (p[m_i] * x + q[m_i] * y + r[m_i])
        denum += w(m_i, x, y)
    return num / denum


def parc_o_po_w(i, x, y):
    num = 0
    denum = 0
    for m_i in xrange(m):
        num += w(m_i, x, y) * (x*(p[i] - p[m_i]) + y*(q[i]-q[m_i]) + r[i]-r[m_i])
        denum += w(m_i, x, y)
    return num / (denum*denum)


def parc_E_po_p(i, x, y):
    return parc_E_po_o(x, y) * parc_o_po_p(i, x, y)


def parc_E_po_r(i, x, y):
    return parc_E_po_o(x, y) * parc_o_po_r(i, x, y)


def parc_E_po_q(i, x, y):
    return parc_E_po_o(x, y) * parc_o_po_q(i, x, y)


def parc_E_po_a(i, x, y):
    return parc_E_po_o(x, y) * parc_o_po_w(i, x, y) * parc_w_po_alfa(i, x, y) * parc_alfa_po_a(i, x, y)

def parc_E_po_b(i, x, y):
    return parc_E_po_o(x, y) * parc_o_po_w(i, x, y) * parc_w_po_alfa(i, x, y) * parc_alfa_po_b(i, x, y)


def parc_E_po_c(i, x, y):
    return parc_E_po_o(x, y) * parc_o_po_w(i, x, y) * parc_w_po_beta(i, x, y) * parc_beta_po_c(i, x, y)


def parc_E_po_d(i, x, y):
    return parc_E_po_o(x, y) * parc_o_po_w(i, x, y) * parc_w_po_beta(i, x, y) * parc_beta_po_d(i, x, y)


def parc_o_po_p(i, x, y):
    denum = 0
    for m_i in xrange(m):
        denum += w(m_i, x, y)
    return w(i, x, y) * x / denum


def parc_o_po_q(i, x, y):
    denum = 0
    for m_i in xrange(m):
        denum += w(m_i, x, y)
    return w(i, x, y) * y / denum

def parc_o_po_r(i, x, y):
    denum = 0
    for m_i in xrange(m):
        denum += w(m_i, x, y)
    return w(i, x, y) / denum


def parc_E_po_o(x, y):
    return o(x, y) - fja(x, y)


def parc_w_po_alfa(i, x, y):
    return beta(i, y)


def parc_w_po_beta(i, x, y):
    return alfa(i, x)


def parc_alfa_po_a(i, x, y):
    pom = b[i] * (x+a[i])
    pom2 = b[i]*x
    pom3 = b[i]*a[i]
    pom4 = math.exp(pom2) + math.exp(pom3)
    num = b[i] * math.exp(pom)
    denum = pom4*pom4
    return num / denum


def parc_alfa_po_b(i, x, y):
    pom = b[i] * (a[i] + x)
    pom2 = b[i]*x
    pom3 = b[i]*a[i]
    pom4 = math.exp(pom2) + math.exp(pom3)
    num = (a[i]-x) * math.exp(pom)
    denum = pom4*pom4
    return num / denum


def parc_beta_po_c(i, x, y):
    pom = d[i] * (y+c[i])
    pom2 = d[i]*y
    pom3 = d[i]*c[i]
    pom4 = math.exp(pom2) + math.exp(pom3)
    num = d[i] * math.exp(pom)
    denum = pom4*pom4
    return num / denum


def parc_beta_po_d(i, x, y):
    pom = d[i] * (c[i] + y)
    pom2 = d[i]*y
    pom3 = d[i]*c[i]
    pom4 = math.exp(pom2) + math.exp(pom3)
    num = (c[i]-y) * math.exp(pom)
    denum = pom4*pom4
    return num / denum


def error():
    greska = 0.0
    for x in xrange(xd, xg):
        for y in xrange(xd, xg):
            greska += err(x, y)
    return greska


def err(x, y):
    pom = fja(x,y)-o(x,y)
    return 1/81.0 * (pom**2)

xd = -4
xg = 5


def batch_search():
    with open('error.txt', 'w') as error_output:
        for t in xrange(250):
            for i in xrange(m):
                sumP = 0.0
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        sumP += parc_E_po_p(i, x, y)
                p[i] += - eta * sumP
                sumQ = 0.0
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        sumQ += parc_E_po_q(i, x, y)
                q[i] += - eta * sumQ
                sumR = 0.0
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        sumR += parc_E_po_r(i, x, y)
                r[i] += - eta * sumR

                sumA = 0.0
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        sumA += parc_E_po_a(i, x, y)
                a[i] += - eta * sumA
                sumB = 0.0
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        sumB += parc_E_po_b(i, x, y)
                b[i] += - eta * sumB

                sumC = 0.0
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        sumC += parc_E_po_c(i, x, y)
                c[i] += - eta * sumC
                sumD = 0.0
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        sumD += parc_E_po_d(i, x, y)
                d[i] += - eta * sumD

            print str(t), str(error())
            error_output.write('%s %s\n' % (str(t), str(error())))
            if (error() < 100):
                break


def online_search():
    with open('error.txt', 'w') as error_output:
        for t in xrange(600):
            for i in xrange(m):
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        p[i] += - eta * parc_E_po_p(i, x, y)
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        q[i] += - eta * parc_E_po_q(i, x, y)
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        r[i] += - eta * parc_E_po_r(i, x, y)

                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        a[i] += - eta * parc_E_po_a(i, x, y)
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        b[i] += - eta * parc_E_po_b(i, x, y)

                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        c[i] += - eta * parc_E_po_c(i, x, y)
                for x in xrange(xd, xg):
                    for y in xrange(xd, xg):
                        d[i] += - eta * parc_E_po_d(i, x, y)

            print str(t), str(error())
            error_output.write('%s %s\n' % (str(t), str(error())))
            if (error() < 12):
                break

#batch_search()
online_search()

for x in xrange(-4, 5):
    for y in xrange(-4, 5):
        print('(%s,%s)\t%s\t%s' % (x, y, fja(x,y), o(x,y)))

print '-----------------------'
with open('error_function.txt', 'w') as o_file:
    for x in xrange(xd, xg):
        for y in xrange(xd, xg):
            o_file.write('%s\t%s\t%s\n' % (x, y, (o(x,y) - fja(x,y))))
print '-----------------------'


with open('membership_function_alfa.txt', 'w') as o_file:
    o_file.write('a = %s\nb = %s\n' % (a, b))
    for i in xrange(m):
        o_file.write('%s\n' % (i))
        for x in xrange(xd-4, xg+4):
            o_file.write('%s\t%s\n' % (x, alfa(i, x)))

with open('membership_function_beta.txt', 'w') as o_file:
    o_file.write('c = %s\nd = %s\n' % (c, d))
    for i in xrange(m):
        o_file.write('%s\n' % (i))
        for x in xrange(xd-4, xg+4):
            o_file.write('%s\t%s\n' % (x, beta(i, x)))
