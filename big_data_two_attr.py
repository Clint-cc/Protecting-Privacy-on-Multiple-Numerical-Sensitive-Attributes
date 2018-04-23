import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
import sklearn
from sklearn.cluster import KMeans

no_of_clusters = int(raw_input("enter the no.of clusters: "))

def print_table(X):
    t=[]
    l = [[[] for i in xrange(no_of_clusters)] for i in xrange(no_of_clusters)]
    for i in range(len(X)):
        t = X[i]
        l[labels[i]][labels[i]].append("t" + str(i + 1))
    print("\nResult :- ")
    for i in l:
        print i
    print "\nfinal groups are: "
    dict_count = {}
    for i in xrange(len(X)):
        dict_count["t" + str(i + 1)] = len(l[labels[i]][labels[i]])
    ans = []
    while len(dict_count) != 0:
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
                        dict_count[x] = len(cell)
                    flag = False
                    break
            if flag is False:
                break
        calculate_totals(l, dict(dict_count))
    return ans

def calculate_totals(l, d):
    row_total = []
    col_total = [[] for i in xrange(len(l))]

    for row in l:
        te=[]
        for i in xrange(len(row)):
            te+=row[i]
            col_total[i]+=row[i]

        row_total.append(len(te))

    for i in xrange(len(col_total)):
        col_total[i]=len(col_total[i])
    return d

db=MySQLdb.connect('localhost','root','balu','project')
cursor=db.cursor()

sql = "select * from big_data"
cursor.execute(sql)

i=[]
l=[]
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
    print age, btravel, dept, gender, jobrole, hrate, drate

db.close()

print "\n"
a = np.array(i)
b = np.array(l)
X = np.dstack((a,b))[0]
print "Two dimensional array X: "
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
print(len(centroids))
print "Labels: "
print labels
print(len(labels))


cc = ["g.","r.","c.","y.","b.","m."]
colors = []
for i in range(len(X)):
    colors.append(cc[i%6])
t=[]
t2=[]
l=[[[] for i in xrange(no_of_clusters)] for i in xrange(no_of_clusters)]
print(len(l))
for i in range(len(X)):
    t=X[i]
    t2.append(t)
    l[labels[i]][labels[i]].append("t"+str(i+1))
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 2)

plt.scatter(centroids[:, 0],centroids[:, 1], marker = "x", s=150, linewidths = 5, zorder = 10)

plt.show()

dict_count = {}
for i in xrange(len(X)):
    dict_count["t"+str(i+1)]=len(l[labels[i]][labels[i]])

ans1 = print_table(X)
print ans1
le =len(ans1)
print "total number of tuples:"
print le
supression_ratio = (cnt-le)/cnt

print "supression ratio: "
print supression_ratio