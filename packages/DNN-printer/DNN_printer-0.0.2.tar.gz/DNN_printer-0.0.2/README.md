:DNN Printer

This is a simple package to print the size of feature map and DNN weight.



:Usage

You can use this tool by three steps:

0. Install printer by running `pip3 install printer -U --user`

1. Find the file which defines the structure of a Network. Add the following code:

from DNN\_printer import DNN\_printer

def train(epoch):
    print('\nEpoch: %d' % epoch)
    net.train()
    train_loss = 0
    correct = 0
    total = 0
    DNN_printer(net, (3, 32, 32),batch_size)
    ...
    ...


**Notice:** The first parameter is the net, the second paramater is the size of input data and the third parameter is the batch size.



:result

![Sample](https://upload-images.jianshu.io/upload_images/7862980-b7d5eda25c7ef725.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



:Requirements

Make sure  `torch` has been installed.

:Authors

 CPing & Peiyi Hong


