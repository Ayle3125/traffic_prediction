
## 运行docker容器
```
sudo docker -v /home/asc17/paddle:/home -it mypaddleimage
```
注意文件路径和镜像名。

## 运行
run by:
```
cd ./data
sh get_data.sh
python preprocess.py # notice the filename
cd ..
sh train.sh 
sh predict.sh
```


## 画图
run by:
```
python -m paddle.utils.plotcurve -i $log > plot.png
python plot_curve.py -i $log -o "ploterror.png" classification_error_evaluator
```
注意：需要python库　matplotlib
