import pgrlib
import os
pgrFile = pgrlib.PGR()

pgrFile.setAuthor("MorganPG")
pgrFile.setTitle("SaveToPGR-EncodedOutput")
for file in os.listdir("src"):
    res = pgrlib.Resource.fromFile(os.path.join("src", file))
    pgrFile.addResource(res)

pgrFile.save("src/comp.pgr")