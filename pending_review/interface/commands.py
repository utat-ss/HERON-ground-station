# 15, 22, 23, 24, , 31 - 42
commands = {

    "00" : {
        "pass"       : False,
        "name"       : "Ping OBC",
        "args"       : 0,
        "arg1_type"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },

    "01" : {
        "pass"       : False,
        "name"       : "Get RTC Date/Time",
        "args"       : 0,
        "arg1_type"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 6
    },
    
    "02" : {
        "pass"       : True,
        "name"       : "Set RTC Date/Time",
        "args"       : 2,
        "RTC Date"  : None,
        "RTC Time"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "03" : {
        "pass"       : True,
        "name"       : "Read OBC EEPROM",
        "args"       : 1,
        "EEPROM Address"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 4
    },
    
    
    "04" : {
        "pass"       : True,
        "name"       : "Erase OBC EEPROM",
        "args"       : 1,
        "EEPROM Address"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "05" : {
        "pass"       : True,
        "name"       : "Read OBC RAM Byte",
        "args"       : 1,
        "RAM Address"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 1
    },
    
    #unneeded I believe
    "06" : {
        "pass"       : False,
        "name"       : "Set Indefinite Beacon Enable",
        "args"       : 2,
        "arg1_type"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "10" : {
        "pass"       : False,
        "name"       : "Read Data Block",
        "args"       : 2,
        "Block Type"  : None,
        "Block number"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 4
    },
    
    
    "11" : {
        "pass"       : False,
        "name"       : "Read Primary Command Blocks",
        "args"       : 2,
        "Block number (start)"  : None,
        "Number of blocks"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 4
    },
    
    
    "12" : {
        "pass"       : False,
        "name"       : "Read Secondary Command Blocks",
        "args"       : 2,
        "Block number (start)"  : None,
        "Number of blocks"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 4
    },
    
    
    "13" : {
        "pass"       : False,
        "name"       : "Read Most Recent Status Info",
        "args"       : 0,
        "arg1_type"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 33
    },
    
    
    "14" : {
        "pass"       : False,
        "name"       : "Read Recent Local Data Block",
        "args"       : 1,
        "Block Type"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 4
    },
    
    
    "15" : {
        "pass"       : True,
        "name"       : "Read Raw Memory Bytes",
        "args"       : 2,
        "Flash Memory Address (start)"  : None,
        "Number of bytes"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 4
    },
    
    
    "20" : {
        "pass"       : False,
        "name"       : "Collect Data Block",
        "args"       : 2,
        "Block Type"  : None,
        "Field number to start at"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 4
    },
    
    
    "21" : {
        "pass"       : False,
        "name"       : "Get Automatic Data Collection Settings",
        "args"       : 2,
        "arg1_type"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 40
    },
    
    
    "22" : {
        "pass"       : True,
        "name"       : "Set Automatic Data Collection Enable",
        "args"       : 2,
        "Block Type"  : None,
        "0 (disable) or 1 (enable)"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "23" : {
        "pass"       : True,
        "name"       : "Set Automatic Data Collection Period",
        "args"       : 2,
        "Block Type"  : None,
        "Period (in seconds)"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "24" : {
        "pass"       : True,
        "name"       : "Resync Automatic Data Collection Timers",
        "args"       : 0,
        "arg1_type"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "30" : {
        "pass"       : False,
        "name"       : "Get Current Block Numbers",
        "args"       : 0,
        "arg1_type"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 24
    },
    
    
    "31" : {
        "pass"       : True,
        "name"       : "Set Current Block Number",
        "args"       : 2,
        "Block Type"  : None,
        "Block number"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "32" : {
        "pass"       : True,
        "name"       : "Get Memory Selection Adresses",
        "args"       : 0,
        "arg1_type"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 48
    },
    
    
    "33" : {
        "pass"       : True,
        "name"       : "Set Memory Section Start Address",
        "args"       : 2,
        "Block Type"  : None,
        "Flash Memory Address (start)"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "34" : {
        "pass"       : True,
        "name"       : "Set Memory Section End Address",
        "args"       : 2,
        "Block Type"  : None,
        "Flash Memory Address (end)"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "35" : {
        "pass"       : True,
        "name"       : "Erase Memory Physical Sector",
        "args"       : 1,
        "Flash Memory Address"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "36" : {
        "pass"       : True,
        "name"       : "Erase Memory Physical Block",
        "args"       : 1,
        "Flash Memory Address"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "37" : {
        "pass"       : True,
        "name"       : "Erase All Memory",
        "args"       : 0,
        "arg1_type"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
    
    "40" : {
        "pass"       : True,
        "name"       : "Send EPS CAN Message",
        "args"       : 2,
        "First 4 bytes of request"  : None,
        "Last 4 bytes of request"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 8
    },
    
    
    "41" : {
        "pass"       : True,
        "name"       : "Send PAY CAN Message",
        "args"       : 2,
        "First 4 bytes of request"  : None,
        "Last 4 bytes of request"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : 8
    },
    
    
    "42" : {
        "pass"       : True,
        "name"       : "Reset Subsystem",
        "args"       : 1,
        "Subsystem"  : None,
        "arg2_type"  : None,
        "arg1_valid" : None,        
        "arg2_valid" : None,
        "resp_size"  : None
    },
    
}

