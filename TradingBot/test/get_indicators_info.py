from talib import abstract

print(abstract.__TA_FUNCTION_NAMES__)

func_info = abstract.Function('EMA').info
print(f"=====Info======")
print(func_info)

defaults, documentation = abstract._get_defaults_and_docs(func_info)
print(f"=====Defaults======")
print(defaults)
print(f"=====Documentation======")
print(documentation)
