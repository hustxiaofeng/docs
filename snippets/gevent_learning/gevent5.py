import gevent
import random

def task(pid):
    """
    Some non-deterministic task
    """
    gevent.sleep(2)
    print('Task %s done' % pid)

def synchronous():
    for i in range(1,10):
        task(i)

def asynchronous():
    threads = [gevent.spawn(task, i) for i in xrange(10)]
    gevent.joinall(threads)

print('Synchronous:')
synchronous()

print('Asynchronous:')
asynchronous()

"""
上例中，在同步的部分，所有的task都同步的执行， 结果当每个task在执行时主流程被阻塞(主流程的执行暂时停住)。

程序的重要部分是将task函数封装到Greenlet内部线程的gevent.spawn。 初始化的greenlet列表存放在数组threads中，
此数组被传给gevent.joinall 函数，后者阻塞当前流程，并执行所有给定的greenlet。执行流程只会在 所有greenlet执行完后才会继续向下走。

要重点留意的是，异步的部分本质上是随机的，而且异步部分的整体运行时间比同步 要大大减少。事实上，同步部分的最大运行时间，
即是每个task停0.002秒，结果整个 队列要停0.02秒。而异步部分的最大运行时间大致为0.002秒，
因为没有任何一个task会 阻塞其它task的执行。
"""