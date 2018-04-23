import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)
from sklearn.cluster import KMeans

no_of_clusters = int(raw_input("enter the no.of clusters: "))

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

    print "\nCounts: "
    print d


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


    calculate_totals(l, dict_count)


db=MySQLdb.connect('localhost','root','balu','project')
cursor=db.cursor()

sql = "select * from microdata3"

cursor.execute(sql)

i=[]
l=[]
bo=[]

print "Table present in data base: "
results = cursor.fetchall()
for row in results:
    # name = row[0]
    ID = row[0]
    age = row[1]
    zip = row[2]
    income = row[3]
    i.append(int(income))
    loan = row[4]
    l.append(int(loan))
    bonus = row[5]
    bo.append(int(bonus))
    # print name, gender, age, postcode, income, loan
    print id, age, zip, income, loan, bonus

db.close()

print "\n"
a = np.array(i)
b = np.array(l)
c = np.array(bo)
X = np.dstack((a,b,c))[0]
print "Three dimensional array X: "
print(X)
print "\n"
kmeans = KMeans(n_clusters=no_of_clusters,max_iter=100)
kmeans.fit(X)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_

print "Centroids: "
print centroids
print "Labels: "
print labels

for i in range(len(X)):
    ax.scatter(X[:, 0], X[:, 1], X[:, 2])

ax.scatter(centroids[:, 0],centroids[:, 1], centroids[:, 2], marker = "x", s=150, linewidths = 5, zorder = 10)
ax.set_xlabel('Income')
ax.set_ylabel('Loan')
ax.set_zlabel('Bonus')
plt.show()


print_table(np.dstack((a,b))[0])
print_table(np.dstack((b,c))[0])
print_table(np.dstack((a,c))[0])