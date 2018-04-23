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

sql = "select * from micro_data"

cursor.execute(sql)

i=[]
l=[]

print "Table present in data base: "
results = cursor.fetchall()
for row in results:
    name = row[0]
    gender =row[1]
    age = row[2]
    postcode = row[3]
    income = row[4]
    i.append(int(income))
    loan = row[5]
    l.append(int(loan))
    print name, gender, age, postcode, income, loan

db.close()

print "\n"
a = np.array(i)
b = np.array(l)
X = np.dstack((a,b))[0]
print "Two dimensional array X: "
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
for i in range(len(X)):
    t=X[i]
    t2.append(t)
    l[labels[i]][labels[i]].append("t"+str(i+1))
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

plt.scatter(centroids[:, 0],centroids[:, 1], marker = "x", s=150, linewidths = 5, zorder = 10)

plt.show()

dict_count = {}
for i in xrange(len(X)):
    dict_count["t"+str(i+1)]=len(l[labels[i]][labels[i]])

ans1 = print_table(X)
print ans1

# for i in range(len(X)):
#     ax.scatter(X[:, 0], X[:, 1], X[:, 2])
# ax.scatter(centroids[:, 0],centroids[:, 1], centroids[:, 2], marker = "x", s=150, linewidths = 5, zorder = 10)
# ax.set_xlabel('Income')
# ax.set_ylabel('Loan')
# ax.set_zlabel('Bonus')
# plt.show()

# for i in range(len(X)):
#     ax.scatter(X[:, 0], X[:, 1], X[:, 2])
#
# ax.scatter(centroids[:, 0],centroids[:, 1], centroids[:, 2], marker = "x", s=150, linewidths = 5, zorder = 10)
# ax.set_xlabel('Income')
# ax.set_ylabel('Loan')
# ax.set_zlabel('Bonus')
# plt.show()