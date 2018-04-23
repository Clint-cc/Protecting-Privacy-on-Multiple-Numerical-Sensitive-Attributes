import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)
import sklearn
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

        row_total.append(len(te))

    for i in xrange(len(col_total)):
        col_total[i]=len(col_total[i])
    print "row count: "
    print (row_total)
    print "column count: "
    print(col_total)

    return d

db=MySQLdb.connect('localhost','root','balu','project')
cursor=db.cursor()

sql = "select * from micro_data_three"

cursor.execute(sql)

i=[]
l=[]
bo=[]

print "Table present in data base: "
results = cursor.fetchall()
for row in results:
    name = row[0]
    #ID = row[0]
    # age = row[1]
    # zip = row[2]
    income = row[1]
    i.append(int(income))
    loan = row[2]
    l.append(int(loan))
    bonus = row[3]
    bo.append(int(bonus))
    # print name, gender, age, postcode, income, loan
    print name, income, loan, bonus

db.close()

# print i
# print l
# plt.scatter(i,l)
# plt.show()
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


colors = ["g.","r.","c.","y.","b.","m."]
t=[]
t2=[]
l=[[[] for i in xrange(no_of_clusters)] for i in xrange(no_of_clusters)]
# print(l)


# ax.scatter(X[:, 0], X[:, 1], X[:, 2])

for i in range(len(X)):
    t=X[i]
    t2.append(t)
    l[labels[i]][labels[i]].append("t"+str(i+1))

    ax.scatter(X[:, 0], X[:, 1], X[:, 2])
    # print("coordinate:",X[i], "label:", labels[i])
    # plt.plot(X[i][0], X[i][1], X[i][2], colors[labels[i]], markersize = 10)
    # print t

ax.scatter(centroids[:, 0],centroids[:, 1], centroids[:, 2], marker = "x", s=150, linewidths = 5, zorder = 10)
ax.set_xlabel('Income')
ax.set_ylabel('Loan')
ax.set_zlabel('Bonus')
plt.show()

print("\nResult :- ")
for i in l:
    print i

dict_count = {}
for i in xrange(len(X)):
    dict_count["t"+str(i+1)]=len(l[labels[i]][labels[i]])

print "\n"
print "Cell count: "
print dict_count

calculate_totals(l, dict_count)
