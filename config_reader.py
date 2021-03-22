import sys, getopt, json
from libs import api_config

#config_reader.py is used to retrieved config parameters from either json file or environment variables (i.e. api_config)

def getConfig(argv):
   jsonFilePath = None

   try:
      opts, args = getopt.getopt(argv,"j:",["json="])
   except getopt.GetoptError:
      print('json_test.py -j <JSON config file>')
      sys.exit(2)


   for opt, arg in opts:
      if opt in ("-j", "--json"):
         jsonFilePath = arg

   print("[config_reader.py] Input JSON file is ", jsonFilePath)

   jsonData = None

   if jsonFilePath is not None:
        with open(jsonFilePath) as f:
          jsonData = json.load(f)
   
   config = api_config.get_config_from_env() if jsonData is None else jsonData
   
   print("[config_reader.py] config dictionary: ", config)
   return config

# if __name__ == "__main__":
#    argv = sys.argv[1:]
#    config = getConfig(argv)
#    print("[config_reader.py] config dictionary: ", config)