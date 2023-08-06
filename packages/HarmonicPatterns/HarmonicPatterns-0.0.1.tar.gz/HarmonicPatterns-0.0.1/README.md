### Harmonic Pattern Detector


##### patterns found

![plot_0](res/plot_0.png)

##### patterns predict

![predict_0](res/predict_0.png)


#### Reqirements

+ TA-Lib

<details>

  <summary> <b>安装Setup</b>   </summary>
  <p>
  
  
  ```bash
  cd <project_dir>
  pip install -r requirements.txt
  pip install -e . # or python setup.py install
  ```
  
  </p>
</details>


###  Features

####  Visualize

+ Draw Harmonic Patterns in the graph using ipympl
+ 使用ipympl绘图

####  Notify

+ Send alerts to Wechat when Harmonic are newly found
+ 如果最新行情形成了谐波模式，发送消息到微信

####  Predict

+ Predict harmonic patterns according to current kline
+ 根据当前的K线行情，预测会形成谐波模式的价格点位


#### Else:

+ go to examples/*.ipynb
+ [example](examples/HarmoCurrent.ipynb)
