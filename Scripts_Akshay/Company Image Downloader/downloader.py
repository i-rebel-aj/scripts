import urllib.request
from csv import reader
with open('out.csv', 'r') as fp:
    csv_reader = reader(fp)
    count=0
    for row in csv_reader:
        #print(row[0])
        name=row[0].replace(' ', '')
        name=name.lower()
        #print(name)
        link="http://logo.clearbit.com/"+name+".com"
        try:
            urllib.request.urlretrieve(link, "./imageDump/{}.jpg".format(name))
        except:
            count+=1
            print(link+" Not Found")
    print(count)    
    print("Done")