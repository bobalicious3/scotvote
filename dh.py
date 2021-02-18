#!/usr/bin/env python
import argparse
import sys
import pprint
import logging
import yaml
import re
import math
import copy

def max(list):
    curr = 0
    maxparty = "eek"
    for party in list:
       if curr < list[party]:
    	   curr = list[party]
    	   maxparty = party
    return maxparty

def vote_win(party,votes):
    votes['seats'][party] = votes['seats'][party] + 1
    return votes

def dhondt(votes):
    for party in votes['list']:
    	votes['dhondt'][party] = math.ceil(votes['list'][party] / (votes['seats'][party] + 1))
    return votes

def do_rounds(votes):
    votes = dhondt(votes)
    for n in range(1, votes['listseats']):
       winner = max(votes['dhondt'])
       votes = vote_win(winner,votes)
       votes = dhondt(votes)
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(votes)
    #print (winner)
    return votes

def clear_dhondt(votes):
    votes['dhondt'] = {}
    for party in votes['seats']:
    	votes['dhondt'][party] = 0
    return votes

def print_votes(votes):
    for party in votes['seats']:
    	print (party,":",votes['seats'][party])

def read_vote_data(configfile):
    try:
    	votes = yaml.load(open(configfile),Loader=yaml.FullLoader)
    except (IOError, err):
    	print ("bad config file?: %s" % (err))
    return votes

def main():

    parser = argparse.ArgumentParser(description='dhondt calc.')
    parser.add_argument('-p', default='Green',action='store', help='The party for the list vote (Green/ Alliance/ ISP)')
    parser.add_argument('-n', default='0',action='store', help='the number of list seats - taken from the SNP')
    parser.add_argument('-d', default='HI.yaml',action='store', help='The Yaml data')
    args = parser.parse_args()

    configfile = args.d
    list_party = args.p
    list_votes = args.n

    # get data and calc seats
    votes = read_vote_data(configfile)
    votes = clear_dhondt(votes)
    votes = do_rounds(votes)
    print_votes(votes)

    # two vars for printed output
    snplist = votes['list']['SNP']
    startseats = votes['seats'][list_party]
    print ('-----')


    # again, get data and calc seats (with param modifys)
    votes = read_vote_data(configfile)
    votes = clear_dhondt(votes)
    if list_party in votes['list']:
    	votes['list'][list_party] = votes['list'][list_party] + int(list_votes)
    else:
    	votes['list'][list_party] = int(list_votes)
    if list_party != 'SNP':
    	votes['list']['SNP'] = votes['list']['SNP'] - int(list_votes)
    else:
        # move 80% Labour and 20% Tory to SNP ... if were upping SNP
        list20 = round(int(list_votes) * 0.2)
        list80 = round(int(list_votes) * 0.8)
        votes['list']['Tory'] = votes['list']['Tory'] - list20
        votes['list']['Labour'] = votes['list']['Labour'] - list80
        #print(votes['list']['Labour'])
        #print(votes['list']['Tory'])
    votes = do_rounds(votes)
    print_votes(votes)

    # List is what this is looking at mostly - if it changes
    endseats = votes['seats'][list_party]
    print ('With ', list_party,':',votes['list'][list_party])
    if endseats > startseats:
        diff = endseats - startseats
        print ('    SNP got list:',snplist)
        print ('   ',list_party,' UP by:',diff)
        print ('    Using votes:',args.n)
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(votes)
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(votes)

  
if __name__ == "__main__":
    main()



 # seats:
 #   SNP: 9
 #   Labour: 0
 #   Tory: 1
 #   Green: 0
 #   Libdem: 0
 #   ISP: 0
 #     
 # list:
 #   SNP: 137086
 #   Labour: 85848
 #   Tory: 38791
 #   Green: 15123
 #   Libdem: 18444
 #   ISP: 0
 # 
 # 
 # listseats: 6

