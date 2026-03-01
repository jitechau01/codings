schema_list= ('landing','crdh_dea_iport_reporting', 'dp_rdportfolio360', 'semantic', 
             'srv_mdm_rndmasterdata', 'srv_rnd_df', 'stg_manual_inputs')
landing,iport,p360,semantic,mdm,srv,stg=schema_list

for schema in schema_list:
    print(schema)
    
print(landing)
print(iport)
print(p360)
print(semantic)
print(mdm)
print(srv)
print(stg)