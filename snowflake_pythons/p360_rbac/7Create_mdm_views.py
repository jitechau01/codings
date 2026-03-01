import os
import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_data_engineer import _conn

cur=_conn()
database='rndcontrolling'
srv_layer_schema='srsrv_mdm_rndmasterdata'