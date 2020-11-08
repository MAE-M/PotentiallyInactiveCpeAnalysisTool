# Potentially inactive CPE analysis tool

Potentially inactive CPE analysis tool is an offline analysis tool by using pandas to process data and using xgboost to idetify potentially inactice CPE users.

## License

Licensed under an Apache-2 license.

## Copyright

Copyright (c) Huawei Technologies Co., Ltd.

## Requirements

* Windows  
* Python 3.7+  
* Pandas 1.0.3  
* xgboost 0.9

## Build

Make sure you have installed [pandas 1.0.3+](https://pandas.pydata.org/) and [xgboost-0.9](https://github.com/dmlc/xgboost/tree/release_0.90) .And to build exe file from source you need Cython and Pyinstaller.Cython and Pyinstaller can be installed from pypi:  

* Install Cython and Pyinstaller  
```pip install cython```  
```pip install pyinstaller```  
* Build py file to pyd file by using cython  
```python build\build_pyd.py build_ext --inplace```
* Packaged into exe file  
```pyinstaller -F src\ui\potentially_inactive_cpe_analysis_tool.py -p venv\Lib\site-packages --add-data=venv\Scripts\xgboost;xgboost  --noconsole```

## Run Potentially inactive CPE analysis tool

 1. Either download or build Potentially inactive CPE analysis tool
 2. Get the parameter.json file from source code, the directory is src\setting\parameter.json.  
 Make sure the execution directory like bellow:  
 |----setting  
 |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|----parameter.json  
 |----PotentiallyInactiveCpeAnalysisTool.exe
 3. Double click Potentially_inactive_CPE_analysis_tool.exe to run

## Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.Your help is very valuable to make the package better for everyone.
