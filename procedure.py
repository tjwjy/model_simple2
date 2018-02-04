import pandas as pd

# import test_agentS
# import test_dualcentric
# import test_agentExp
# import test_agentL
import test_agentR
#  import test_agent2
# import model_statics.txt2csv as txt2csv
path='E:\\data\\taxidata\\shanghai\\20140301grid.csv'
pathod='E:\\data\\taxidata\\shanghai.csv'
model_num=1
for i in range(1):
    print ('the model number is '+str(i))
    path=test_agentR.run(path=path,pathod=pathod)
    # txt2csv.read_txt_tocsv24(path,csv_path=pathod)
    print ('OK')
