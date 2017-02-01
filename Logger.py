import time
def log(info):
    try:
        info = str(info)
        time_str = time.strftime('%X', time.localtime(time.time()))
        print "[%s] %s" % (time_str, info)
        f = open('run_log.txt','a')
        f.write("[%s] %s \n" % (time_str, info) )
        f.close()
    except:
        pass
