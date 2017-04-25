
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
cp speeds.csv predict_speeds.csv
cd ..
sh train.sh
python predict.py
```
**注意这里predict的文件改变了,最后得到的预测结果在原数据文件speed.csv中，最后需要预测多久就在mypredict.py中进行修改**

此外还添加了pred_res文件，内容为speeds.csv

**为避免原数据丢失，可以先将speeds.csv备份**,如“cp speeds.csv speeds.bak”
//“cp speeds.bak speeds.csv”将数据还原


## 画图
run by:
```
python -m paddle.utils.plotcurve -i $log > plot.png
python plot_curve.py -i $log -o "ploterror.png" classification_error_evaluator
```
注意：需要python库　matplotlib
