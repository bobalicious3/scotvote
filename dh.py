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
       #print (winner)
    #pp.pprint(votes)
    return votes

def clear_dhondt(votes):
    votes['dhondt'] = {}
    for party in votes['seats']:
    	votes['dhondt'][party] = 0
    return votes

def print_votes(votes):
    for party in votes['seats']:
    	print (party,":",votes['seats'][party])

def main():

    parser = argparse.ArgumentParser(description='dhondt calc.')
    parser.add_argument('-p', default='Green',action='store', help='The party for the list vote (Green/ Alliance/ ISP)')
    parser.add_argument('-n', default='0',action='store', help='the number of list seats - taken from the SNP')
    parser.add_argument('-d', default='HI.yaml',action='store', help='The Yaml data')
    args = parser.parse_args()

    configfile = args.d

    try:
    	votes = yaml.load(open(configfile),Loader=yaml.FullLoader)
    except (IOError, err):
    	print ("bad config file?: %s" % (err))
    original_data = copy.deepcopy(votes)

    votes = clear_dhondt(votes)
    votes = do_rounds(votes)
    print_votes(votes)
    print ('-----')

    list_party = args.p
    list_votes = args.n

    votes = clear_dhondt(original_data)
    if list_party in votes['list']:
    	votes['list'][list_party] = votes['list'][list_party] + int(list_votes)
    else:
    	votes['list'][list_party] = int(list_votes)
    if list_party != 'SNP':
    	votes['list']['SNP'] = votes['list']['SNP'] - votes['list'][list_party]
    votes = do_rounds(votes)
    print_votes(votes)
    print ('With ', list_party,':',votes['list'][list_party])
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

