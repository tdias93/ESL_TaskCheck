import pyodbc

def connection():
    try:
        print('\n################################################## Connecting to Database')

        driver = '{SQL Server}'                         # '{ODBC Driver 17 for SQL Server}' ; '{SQL Server}'
        server = 'tcp:192.168.1.158,49172'              # 'DESKTOP-TDO2019\SQLSERVER' ; 'BRLNB35.BRLOG.LOCAL' ; 'BRLNB35\SQLEXPRESS' ; 'tcp:BRLNB35,49172'; 'tcp:192.168.1.158,49172'
        database = 'dtbBR_Samor'                        # 'TaskCheck'
        username = 'BR_Admin'
        password = 'Admin#2020'

        string_conection = 'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID='+username+';PWD='+ password

        return pyodbc.connect(string_conection)

    except pyodbc.Error as error:
        print(f'################################################## Connecting to Database Unsuccessful: \n'
              f'    Error: {error}')


def insert(pid_number, task_name, svmem_used, svmem_free, svmem_perc, sswap_used, sswap_free, sswap_perc, boot_time, user_name, cpu_used, task_status, log_time, email_status, email_error, process_log):
    try:
        sql = f"INSERT INTO tbd_GerenciadorTarefasRefistro (pid_number, task_name, svmem_used, svmem_free, svmem_perc, sswap_used, sswap_free, sswap_perc, boot_time, user_name, cpu_used, " \
              f"task_status, log_time, email_status, email_error, process_log) VALUES ({pid_number}, '{task_name}', '{svmem_used}', {svmem_free}, {svmem_perc}, {sswap_used}, {sswap_free}, {sswap_perc}, " \
              f"'{boot_time}', '{user_name}', {cpu_used}, '{task_status}', '{log_time}', '{email_status}', '{email_error}', '{process_log}')"

        con = connection()                  # Abre Conexão com BD
        cursor = con.cursor()               # Obtem uma transação
        cursor.execute(sql)                 # Passa comando de dados em SQL
        con.commit()                        # Executa comandos no banco de dados
        con.close                           # Fecha conexão

    except pyodbc.Error as error:
        print(f'################################################## Error INSERT: {error}')


def select(pid_number):
    try:
        sql = f'SELECT TOP 5 task_status, id FROM tbd_GerenciadorTarefasRefistro WHERE pid_number = 1 ORDER BY id DESC'     # {pid_number} ORDER BY id DESC

        con = connection()                  # Abre Conexão com BD
        cursor = con.cursor()               # Obtem uma transação
        cursor.execute(sql)                 # Passa comando de dados em SQL
        result = cursor.fetchall()          # Pega valore do SELECT

        return result

    except pyodbc.Error as error:
        print(f'################################################## Error SELECT: {error}')
