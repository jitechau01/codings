import sys
sys.path.insert(1,'/home/cloud/codings/snowflake_pythons')
from __connections.__con_policy_admin import _conn

cur=_conn()
tag_schema="rndcontrolling.data_governance"

def create_required_tags():
    cur.execute("use schema rndcontrolling.data_governance")
    cur.execute(f""" select distinct ADGROUP from rndcontrolling.data_governance.consumer_ADGROUP """)
    result=cur.fetchall()
    print(f"""\n---------->Creating tags for consumers based on ADGROUP values""")
    for row in result:
        consumer_name=row[0]
        tag=f" {tag_schema}.tag_{consumer_name}_masked"
        try:
            cur.execute(f"""CREATE TAG if not exists {tag}""")
            status = cur.fetchone()
            message = status[0] 
            if status:
                if "successfully created" in message.lower():
                    print(f"{tag} created successfully")
                elif "already exists" in message.lower():
                    print(f"{tag} already exists, skipping creation")
                else:   
                    print(f"Tag {tag} creation status: {message}")    
            else:
                print(f"No status returned for tag {tag}")
        except Exception as e:
            print(f"Error creating tag {tag}: {e}")
def add_tag_values():
    cur.execute(f""" select distinct consumer_name,sensitivity_level from rndcontrolling.data_governance.data_sensitivity where upper(mark_sensitive)='TRUE' """)
    result=cur.fetchall()
    print(f"""\n---------->Adding tag values for consumer tags""")
    for row in result:
        consumer_name=row[0]
        allowed_value=row[1]
        tag=f" {tag_schema}.tag_{consumer_name}_masked"
        print(f"""ALTER TAG {tag} ADD allowed_values '{allowed_value}' """)
        # try:
        #     cur.execute(f"""ALTER TAG {tag} ADD allowed_values '{allowed_value}' """)
        #     status = cur.fetchone()
        #     message = status[0] 
        #     if status:
        #         if "executed successfully" in message.lower():
        #             print(f"Value added successfully")
        # except Exception as e:
        #     print(f"Error adding value to tag {tag}: {e}")     
def Apply_tags_to_attributes():
    cur.execute("use schema rndcontrolling.DP_RDPORTFOLIO360")
    cur.execute(f""" select db_name,schema_name,object_name,object_type,attribute_name,consumer_name,sensitivity_level from rndcontrolling.data_governance.data_sensitivity where upper(mark_sensitive)='TRUE' """)
    result=cur.fetchall()
    for row in result:
        db_name,schema_name,object_name,object_type,attribute_name,consumer_name,sensitivity_level=row
        tag=f" {tag_schema}.tag_{consumer_name}_masked"
        try:
            print(f""" Applying tag {tag} with value '{sensitivity_level}' to attribute {attribute_name} in table {db_name}.{schema_name}.{object_name} """)
            cur.execute(f"""ALTER {object_type} {db_name}.{schema_name}.{object_name} MODIFY {attribute_name} SET TAG {tag} = '{sensitivity_level}' """)
            status = cur.fetchone()
            message = status[0] 
            if status:
                if "executed successfully" in message.lower():
                    print(f"    Tag applied successfully")
                else:   
                    print(f"    Tag {tag} application status: {message}")    
            else:
                print(f"    No status returned for applying tag {tag}")
        except Exception as e:
            print(f"Error applying tag {tag}: {e}")
    
            
create_required_tags()
add_tag_values()
# Apply_tags_to_attributes()



