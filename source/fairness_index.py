import csv

doc = []
beta=[0.01, 0.03, 0.1, 0.3, 1, 3]
rho = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for b in beta:
	with open('results_beta'+str(b)+'.csv', 'r') as csvFile:
		#skip header
		next(csvFile)

		reader = csv.reader(csvFile, delimiter=',')
		for row in reader:
			#convert string to float
			floatList = map(float, row)
			doc.append(floatList)
iters = len(doc)/len(beta)/len(rho)

#print doc[0]


#FI of the mean

fairness = []


for b in beta:
	rL = []
	for r in rho:
		sum=[]
		sqSum=[]
		for q in range(len(doc[0])-3):
			sum.append(0)
			sqSum.append(0)
		rL.append([sum,sqSum])
	fairness.append(rL)


#rho=row[0]
#beta=row[1]
for row in doc:
	ir = rho.index(row[0])
	ib = beta.index(row[1])
	for idx in range(len(row[3:])):
		fairness[ib][ir][0][idx]+= row[3+idx]
		fairness[ib][ir][1][idx]+= row[3+idx]**2

# mean of FI
N=len(doc[0][3:])

print "Means of the FIs"
FIs = []
for row in doc:
	num = 0
	denom = 0
	for cell in row[3:]:
		num += cell
		denom += cell**2
	FI = (num**2)/(N*denom)
	FIs.append([row[0],row[1], FI])
#print FIs
mediaFIs = []
for b in beta:
	for r in rho:
		mediaFIs.append([b,r,0])
for b in beta:
	for r in rho:
		for fi in FIs:
			if fi[0] == r and fi[1] == b:
				for mfi in mediaFIs:
					if mfi[0] == b and mfi[1] == r:
						mfi[2]+=fi[2]/iters

f = open('meansFI.csv', 'w')
for fi in mediaFIs:
	fi[2] = round(fi[2],3)
	print fi
	f.write(",".join(str(x) for x in fi))
	f.write('\n')
f.close()
print "FI of the means"

means = []

for b in beta:
	for r in rho:
		row = [b,r]
		for i in range(N):
			row.append(0)
		means.append(row)
for b in beta:
	for r in rho:
		for row in doc:
			if row[0] == r and row[1] == b:
				for m in means:
					if m[0] == b and m[1] == r:
						for i in range(N):
							m[2+i]+=row[2+i]/iters
FIsMeans = []
for row in means:
	num = 0
	denom = 0
	for cell in row[3:]:
		num += cell
		denom += cell**2
	FI = (num**2)/(N*denom)
	FIsMeans.append([row[0],row[1], round(FI,3)])
f = open('FIofthemeans.csv', 'w')
for fi in FIsMeans:
	print fi
	f.write(",".join(str(x) for x in fi))
	f.write('\n')
f.close()