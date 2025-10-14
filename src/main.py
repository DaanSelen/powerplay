#!/usr/bin/env python3

from modules.confread import confread

def main():
    cnf = confread()       # Create an instance that reads our config file.
    cnf.verify_integrity() # Make sure its at least filled in.

    

main()