1. start_server/ start_edge中使用的logging？
    garage_name从哪里传入edge？start时输入？

2. message.py中 为什么要继承Enum？
    type=MessageType(xxx)为什么需要传参数？
    from_bytes()方法声明不需要self ？

    _id= id or ULID()?

    message为什么需要转为json重新赋值一遍然后在转为python输出？  from_bytes是这个意思（通过调用下面的construct等）麽？

    （注释中 用json 没有用protobuf好？ 是什么）

3. sever中 logging最好放在执行完send之后
    （zzmq.noblock作用？）
    已经发过的msg 生成 payload为none 但还是会生成msg发送？
    handle_msg 收到无法辨认的消息加一条if record disgard。

4. (edge中 zmq.again作用？)
        try:
        raw = socket.recv()
    except zmq.Again:
        return  --》运行不到？

    注释“# this would likely happen asynchronously”什么意思？   -  server中也有

    event_callback 怎么调用， 和最下面的if分支择一？

    garage name增加由garage id 组成

    simulate_parking_garage 的while true循环 和  我的sensor里面while 冲突？？！！

5. garage 里面注释的问题。。

总系统python 文件名无法运行？