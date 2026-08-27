import pgrlib
import os
import json
import sys

if len(sys.argv) > 1:
    pgrFile = pgrlib.PGR(sys.argv[1])

    print(pgrFile.getResources())
    if not os.path.exists("decrypted/"):
        os.mkdir("decrypted")
    for resource in pgrFile.getResources():
        resource.save("decrypted/"+resource.getFileName())
        if len(resource.getTags()) != 0:
            f = open("decrypted/"+resource.getFileName()+".json", "w")
            jsonStr = json.dump(resource.getTags(), f)
            f.close()