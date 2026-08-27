import pgrlib
import os
import json
import sys

if len(sys.argv) > 1:
    pgrFile = pgrlib.PGR(sys.argv[1])

    print("Version: "+pgrFile.getVersion())
    print("Author: "+pgrFile.getAuthor())
    print("Title: "+pgrFile.getTitle())

    print("Resources:")
    for resource in pgrFile.getResources():
        print(" "+resource.fileName)
        if len(resource.getTags()) != 0:
            print(" Tags:")
            for tag, value in resource.getTags().items():
                print("  "+str(tag)+": "+str(value))
        