import os
import sys
import time
 
#cmd = './test.sh'
cmd_dict = {'cmd1': {'shell': './run1.sh', 'flag': False},
            'cmd2': {'shell': './run2.sh', 'flag': False},
}

# cmd_dict = {'cmd1': {'shell': './run1.sh', 'flag': False}}

def gpu_info():
    gpu_status = os.popen('nvidia-smi | grep %').read().split('|')
    gpu_memory = int(gpu_status[14].split('/')[0].split('M')[0].strip())   # device 0/1/2/3 -> gpu_status[2/6/10/14]
    print(gpu_memory)
    gpu_power = int(gpu_status[1].split('   ')[-1].split('/')[0].split('W')[0].strip())
    return gpu_power, gpu_memory, gpu_status
 
 
def narrow_setup(interval=60):
    # gpu_power, gpu_memory, gpu_status = gpu_info()
    i = 0

    for key in cmd_dict:
        single_dict = cmd_dict[key]
        gpu_power, gpu_memory, gpu_status = gpu_info()

        while gpu_memory > 10000:  # set waiting condition
            gpu_power, gpu_memory, _ = gpu_info()
            i = i % 5
            symbol = 'monitoring: ' + '>' * i + ' ' * (10 - i - 1) + '|'
            gpu_power_str = 'gpu power:%d W |' % gpu_power
            gpu_memory_str = 'gpu memory:%d MiB |' % gpu_memory
            sys.stdout.write('\r' + gpu_memory_str + ' ' + gpu_power_str + ' ' + symbol)
            sys.stdout.flush()
            time.sleep(interval)
            i += 1

        if single_dict['flag'] is False:
            single_dict['flag'] = True
            shell_cmd = single_dict['shell']
            print('\n' + shell_cmd)
            os.system(shell_cmd)
            time.sleep(200)


   
    


if __name__ == '__main__':
    narrow_setup()
