from Include import TC_ConnectionDB, TC_Email
from datetime import datetime
import psutil, os, subprocess
from subprocess import run

def insert():
    TC_ConnectionDB.insert(
        pid_number,             # ENVIA P/ BD -> Numero PID da tarefa analisada
        task_name,              # ENVIA P/ BD -> Nome da tarefa analisada
        svmem_used,             # ENVIA P/ BD -> Memória virtual utilizada
        svmem_free,             # ENVIA P/ BD -> Memória virtual livre
        svmem_perc,             # ENVIA P/ BD -> Porcentagem da memória virtual utilizada
        sswap_used,             # ENVIA P/ BD -> Memória SWAP utilizada
        sswap_free,             # ENVIA P/ BD -> Memória SWAP livre
        sswap_perc,             # ENVIA P/ BD -> Porcentagem da memória SWAP utilizada
        boot_time,              # ENVIA P/ BD -> Data Bootcomputador
        user_name,              # ENVIA P/ BD -> Usuário
        cpu_used,               # ENVIA P/ BD -> Utilização da CPU
        task_status,            # ENVIA P/ BD -> Status do PID
        log_time,               # ENVIA P/ BD -> Data do Log
        email_status,           # ENVIA P/ BD -> Status evio do e-mail
        email_error,            # ENVIA P/ BD -> Erro envio e-mail
        process_log)            # ENVIA P/ BD -> Erro no reset da tarefa


# Pega nome da tarefa a ser analisada
process_file = open(f'{os.getcwd()}\File\processlog.txt', 'r')   # Abre .TXT
process_name = process_file.readlines()                          # Le Dados
process_name = process_name[0].replace('\n', '')                 # Pega Primeira Linha
process_file.close()                                             # Fecha TXT

psutil_flag = 0                                                  # flag 0 -> Busca não correspondida
for proc in psutil.process_iter(attrs=['name', 'pid']):          # Percorre todas as tarefas em execução

    if proc.info['name'] == process_name:                        # Valida se o nome atual da tarefa corresponde ao analisado
        print(proc.info['name'])
        psutil_flag = 1                                          # flag 1 -> Busca Correspondida
        p = psutil.Process(pid= proc.info['pid'])

        pid_number = proc.info['pid']                                                         # Numero PID da tarefa analisada
        task_name = proc.info['name']                                                         # Nome da tarefa analisada
        svmem_used = round(psutil.virtual_memory().used / 1000000000, 2)                      # Memória virtual utilizada
        svmem_free = round(psutil.virtual_memory().free / 1000000000, 2)                      # Memória virtual livre
        svmem_perc = psutil.virtual_memory().percent                                          # Porcentagem da memória virtual utilizada
        sswap_used = round(psutil.swap_memory().used / 1000000000, 2)                         # Memória SWAP utilizada
        sswap_free = round(psutil.swap_memory().free / 1000000000, 2)                         # Memória SWAP livre
        sswap_perc = psutil.swap_memory().percent                                             # Porcentagem da memória SWAP utilizada
        user_name = psutil.users()[0].name                                                    # Usuário
        cpu_used = round(psutil.Process().cpu_times().user * 100, 2)                          # Utilização da CPU
        log_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')                               # Data do Log
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%dT%H:%M:%S')  # Data Bootcomputador
        task_status = os.popen(f'tasklist /V /FI "PID eq {pid_number}"').read().split('\n')   # Status do PID

        # Valida Status da processo PID
        for status in task_status[3].split():
            if status == '#############Running':
                task_status = 'Running'
                break
            else:
                task_status = 'Not Responding'

        # Tratativa do PID
        if task_status == 'Running':

            email_status = ''   # Define valor -> Status envio e-mail
            email_error = ''    # Define valor -> Erro envio e-mail
            insert()            # Chama função para salvar dados no BD

        else:
            result = TC_ConnectionDB.select(pid_number)    # Consulta status anteriores no BD
            flag = 0                                       # flag 0 -> Envia e-mail

            for value in result:

                if value[0] != 'Not Responding':
                    flag = 1
                print(value)

                if value[1] != '':
                    flag = 2

            if flag == 1:                   # flag 1 -> Não envia e-mail
                email_status = 'Not Sent'   # Define valor -> Status envio e-mail
                email_error = ''            # Define valor -> Erro envio e-mail
                insert()                    # Chama função para salvar dados no BD

            elif flag == 2:
                try:
                    proc.kill()
                    email_status = 'Not Sent'       # Define valor -> Status envio e-mail
                    email_error = ''                # Define valor -> Erro envio e-mail
                    process_log = 'System Reset'    # Define valor -> Reset Log
                    insert()

                except Exception as error:
                    email_status = 'Not Sent'       # Define valor -> Status envio e-mail
                    email_error = ''                # Define valor -> Erro envio e-mail
                    process_log = str(error)        # Define valor -> Reset Log
                    insert()

            else:
                subject = 'Attention - Gerenciador de Tarefas'
                msg = 'Hello! ' \
                      '\n\n\n' \
                      'The ESL - Gerenciador de Tarefas isn`t running, please check it. ' \
                      '\n\n\n' \
                      'More information about it:' \
                      '\n' \
                      '\n- PID: ' + str(pid_number) + \
                      '\n- Task Name: ' + str(task_name).upper() + \
                      '\n- Task Status: ' + str(task_status).upper() + \
                      '\n- Memory Usage: ' + str(svmem_used) + '%'\
                      '\n- Total Memory Usage: ' + str(svmem_perc) + '%'\
                      '\n- CPU Usage: ' + str(cpu_used) + '%'\
                      '\n- Computer Start: ' + str(boot_time)

                email = TC_Email.send_email(subject, msg)       # Envia E-mail

                email_status = email[0]                         # Capta valor -> Status envio e-mail
                email_error = email[1]                          # Capta valor -> Erro envio e-mail
                insert()                                        # Chama função para salvar dados no BD

if psutil_flag == 0:                                            # flag 0 -> Busca não correspondida do PID
    subject = 'Attention - Gerenciador de Tarefas is Closed'
    msg = 'Hello! ' \
          '\n\n\n' \
          'The ESL - Gerenciador de Tarefas isn`t open, please check it. ' \

    TC_Email.send_email(subject, msg)    # Envia E-mail

    # python -m auto_py_to_exe