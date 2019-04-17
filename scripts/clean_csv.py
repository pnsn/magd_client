import csv
import argparse


parser = argparse.ArgumentParser(description="Takes a csv file of form \n \
        sta,chan, net, location, lat, lon, rate and cleans duplicate stas. Outputs: \
        sta, chan, net, location, lat, lon, rate")
parser.add_argument('-i','--infile',help='input file name', required=True)
parser.add_argument('-o','--outfile', help='output file name',required=True)
args = parser.parse_args()## show values ##

outfile  = open(args.outfile, "w")
infile= open(args.infile)
# print(infile)
writer=csv.writer(outfile)
header=True
#create dict to find unique sta:net combo
uniq_stas = {}
with  infile as csvfile:
    reader=csv.reader(csvfile)
    for row in reader:
        if header:
            writer.writerows([[ "sta","chan","net","location","lat","lon","rate"]])
            header=False
        else:
            key = row[0] + row[2]
            if key not in uniq_stas:
                #stub out a key, but no need for val. Just a O(1) lookup
                uniq_stas[key] = None
                #stupid -- thing
                if len(row[3])<2:
                    loc="--"
                else:
                    loc=row[3]
                writer.writerows([row])


infile.close()
outfile.close()
