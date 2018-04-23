import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import math
fig = plt.figure()
ax = Axes3D(fig)

no_of_clusters = int(raw_input("enter the no.of clusters: "))


def pearsonr(x, y):
    sigma_xy = np.dot(x, y)
    sigma_x = np.sum(x)
    sigma_y = np.sum(y)
    num = (len(x) * sigma_xy) - (sigma_x * sigma_y)
    sigma_x_2 = np.sum(x**2)
    sigma_y_2 = np.sum(y**2)
    den1 = ((len(x) * sigma_x_2) - (sigma_x * sigma_x))
    den2 = ((len(y) * sigma_y_2) - (sigma_y * sigma_y))
    den = float(den1) * float(den2)
    return num / math.sqrt(den)


def calculate_totals(l, d):
    row_total = []
    col_total = [[] for i in xrange(len(l))]
    for row in l:
        te=[]
        for i in xrange(len(row)):
            te+=row[i]
            col_total[i]+=row[i]
        for tuple in te:
            d[tuple] += len(te)
        row_total.append(len(te))
    for i in xrange(len(col_total)):
        for tuple in col_total[i]:
            d[tuple] += len(col_total[i])
        col_total[i]=len(col_total[i])

def print_table(X):
    kmeans = KMeans(n_clusters=no_of_clusters, max_iter=100)
    kmeans.fit(X)
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    t=[]
    l = [[[] for i in xrange(no_of_clusters)] for i in xrange(no_of_clusters)]
    for i in range(len(X)):
        t = X[i]
        l[labels[i]][labels[i]].append("t" + str(i + 1))
    print("\nResult :- ")
    for i in l:
        print i
    dict_count = {}
    for i in xrange(len(X)):
        dict_count["t" + str(i + 1)] = len(l[labels[i]][labels[i]])
    ans = []
    while len(dict_count)!=0:
        xl = sorted(dict_count.iteritems(), key=lambda (k, v): (v, k))
        m = xl[len(xl) - 1][0]
        dict_count.pop(m)
        for row in l:
            flag = True
            for cell in row:
                if m in cell:
                    ans.append(m)
                    cell.remove(m)
                    for x in cell:
                        dict_count[x]=len(cell)
                    flag=False
                    break
            if flag is False:
                break
        calculate_totals(l, dict(dict_count))
    return ans

db=MySQLdb.connect('localhost','root','balu','project')
cursor=db.cursor()

sql = "select * from big_data"
cursor.execute(sql)

i=[]
l=[]
bo=[]
print "Table present in data base: "
results = cursor.fetchall()
for row in results:
    age=row[0]
    btravel = row[1]
    dept = row[2]
    gender = row[3]
    jobrole = row[4]
    hrate = row[5]
    i.append(long(hrate))
    drate = row[6]
    l.append(long(drate))
    mincome = row[7]
    bo.append(long(mincome))
    print age, btravel, dept, gender, jobrole, hrate, drate, mincome

db.close()

print "\n"
a = np.array(i)
b = np.array(l)
c = np.array(bo)
X = np.dstack((a,b,c))[0]
print "Three dimensional array X: "
print(X)
cnt= len(X)
print cnt
print "\n"
kmeans = KMeans(n_clusters=no_of_clusters,max_iter=100)
kmeans.fit(X)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_

print "Centroids: "
print centroids
print "Labels: "
print labels

xl = {}
xl['bc']=(pearsonr(b,c))
xl['ab']=(pearsonr(a,b))
xl['ac']=(pearsonr(a,c))
xl = sorted(xl.iteritems(), key=lambda (k,v): (v,k))
ss = xl[len(xl)-1][0]
ss2=xl[len(xl)-2][0]
print xl
print (ss,ss2)
ans1 = print_table(np.dstack((globals()[ss[0]], globals()[ss[1]]))[0])
ans2 = print_table(np.dstack((globals()[ss2[0]], globals()[ss2[1]]))[0])
print "\ngroups of "+ss+" :"
print ans1

print "\ngroups of "+ss2+" :"
print ans2

print "\nfinal groups are: "
delim = int(round(len(a) * 0.33))
final = []
for i in xrange(delim):
    s1 = set(ans1[i*delim:(i+1)*delim])
    s2 = set(ans2[i*delim:(i+1)*delim])
    final.append(list(s1&s2))

print final
le =len(final)
print "total number of tuples:"
print le
supression_ratio = (float)(cnt-le)/cnt

print "supression ratio: "
print supression_ratio