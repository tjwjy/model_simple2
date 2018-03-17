import pandas as pd

# import test_agentS
# import test_dualcentric
# import test_agentExp
# import test_agentL
import test_agentS
#  import test_agent2
# import model_statics.txt2csv as txt2csv
# path='E:\\data\\taxidata\\shanghai\\20140301grid.csv'
# pathod='E:\\data\\taxidata\\shanghai.csv'

path=r'D:\data_test\mapdata\shanghai\\Shanghai_Pop_Lambert_filter.shp'
pathod='E:\\data\\taxidata\\shanghai.csv'
model_num=1
for i in range(1):
    print ('the model number is '+str(i))
    path=test_agentS.run(path=path,pathod=pathod)
    # txt2csv.read_txt_tocsv24(path,csv_path=pathod)
    print ('OK')
