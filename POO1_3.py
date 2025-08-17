from prettytable import PrettyTable
import mysql.connector

#*******************************************ABRIR BANCO**************************************************************

def abrebanco():
    try:
        global conexao
        conexao = mysql.connector.Connect(
            host='localhost',
            database='univap',
            user='root',
            password=''
        )
        if conexao.is_connected():
            informacaobanco = conexao.get_server_info()
            print('Conexão realizada')

            global comandosql
            comandosql = conexao.cursor()

            comandosql.execute('select database();')

            nomebanco = comandosql.fetchone()
            print(f'Banco de dados acessado = {nomebanco}')
            print('=' * 80)
            return 1
        else:
            print('Falha ao conectar')
            return 0
    except Exception as erro:
        print(f'Erro ao conectar: {erro}')
        return 0

#******************************************TABELA PROFESSORES********************************************************************

def tabelaProf():
    print('*' * 60)
    print('TABELA PROFESSORES')
    print('*' * 60)
    print('1 - Cadastrar')
    print('2 - Alterar')
    print('3 - Excluir')
    print('4 - Consultar')
    print('*' * 60)
    respProf = int(input('Escolha uma opção: '))
    print('*' * 60)
    if respProf == 1:
        cadastrarProf()
    elif respProf == 2:
        alterarProf()
    elif respProf == 3:
        excluirProf()
    elif respProf == 4:
        consultarProf()
    else:
        print('Selecione uma opção válida!!')

#*********************************************TABELA DISCIPLINAS***************************************************************

def tabelaDisc():
    print('*' * 60)
    print('TABELA DISCIPLINAS')
    print('*' * 60)
    print('1 - Cadastrar')
    print('2 - Alterar')
    print('3 - Excluir')
    print('4 - Consultar')
    print('*' * 60)
    respDisc = int(input('Escolha uma opção: '))
    print('*' * 60)
    if respDisc == 1:
        cadastrarDisc()
    elif respDisc == 2:
        alterarDisc()
    elif respDisc == 3:
        excluirDisc()
    elif respDisc == 4:
        consultarDisc()
    else:
        print('Selecione uma opção válida!!')

#*********************************************TABELA PxD*******************************************************

def tabelaDxP():
    print('*' * 60)
    print('TABELA PROFESSORESxDISCIPLINAS')
    print('*' * 60)
    print('1 - Cadastrar')
    print('2 - Alterar')
    print('3 - Excluir')
    print('4 - Consultar')
    print('*' * 60)
    respPxD = int(input('Escolha uma opção: '))
    print('*' * 60)
    if respPxD == 1:
        cadastrarDxP()
    elif respPxD == 2:
        alterarDxP()
    elif respPxD == 3:
        excluirDxP()
    elif respPxD == 4:
        consultarDxP()
    else:
        print('Selecione uma opção válida!!')

#****************************************CADASTRAR PROFESSOR************************************************************

def cadastrarProf():
    try:
        comandosql = conexao.cursor()
        
        while True:
            id = int(input('Insira o registro do professor: '))
            comandosql.execute(f'SELECT registro FROM professores WHERE registro = {id}')
            if comandosql.fetchone():
                print('Professor já existente!')
                continue
                
            if id >= 0:
                registroProf = id

                while True:
                    nome = input('Insira o nome do professor: ')
                    if not nome.isnumeric():
                        nomeProf = nome
                        break
                    print('Nome inválido!')

                while True:
                    telefone = input('Insira o telefone do professor: ')
                    if telefone.isdigit() and len(telefone) == 11:
                        telefoneProf = int(telefone)
                        break
                    print('Telefone inválido!')

                while True:
                    idade = input('Insira a idade do professor: ')
                    if idade.isdigit() and int(idade) >= 18:
                        idadeProf = int(idade)
                        break
                    print('Idade inválida!')

                while True:
                    salario = input('Insira o salário do professor: ')
                    if salario.isdigit() and int(salario) >= 0:
                        salarioProf = int(salario)
                        break
                    print('Salário inválido!')

                comandosql.execute(f"""
                    INSERT INTO professores(registro, nomeprof, telefoneprof, idadeprof, salarioprof) 
                    VALUES ({registroProf}, '{nomeProf}', {telefoneProf}, {idadeProf}, {salarioProf});
                """)
                conexao.commit()
                print('Professor cadastrado com sucesso!')
                break
            else:
                print('Registro inválido!')
                
    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        comandosql.close()
        conexao.close()   


#*****************************************ALTERAR PROFESSOR***********************************************************

def alterarProf():
    try:
        comandosql = conexao.cursor()

        while True:
            registroProf = int(input('Insira o registro do professor que deseja alterar: '))
            comandosql.execute(f'SELECT * FROM professores WHERE registro = {registroProf}')
            tabela = comandosql.fetchall()
            if not tabela:
                print('Professor não registrado!')
                continue
            
            print('*' * 60)
            print('ALTERAÇÕES DISPONÍVEIS:')
            print('*' * 60)
            print('1 - Nome')
            print('2 - Telefone')
            print('3 - Idade')
            print('4 - Salário')
            print('*' * 60)
            respALteracao = int(input('Escolha uma opção: '))
            print('*' * 60)
        
            if respALteracao == 1:
                if comandosql.rowcount > 0:
                    for registro in tabela:
                        print(f'Atual professor: {registro[1]}')
                    while True:
                        nomeProf = input('Insira o novo nome do professor: ')
                        if not nomeProf.isnumeric():
                            break
                        print('Nome inválido!')
                    comandosql.execute(f"UPDATE professores SET nomeprof = '{nomeProf}' WHERE registro = {registroProf};")

            elif respALteracao == 2:
                if comandosql.rowcount > 0:
                    for registro in tabela:
                        print(f'Atual telefone: {registro[2]}')
                    while True:
                        telefoneProf = input('Insira o telefone do professor: ')
                        if telefoneProf.isdigit() and len(telefoneProf) == 11:
                            break
                        print('Telefone inválido! Deve ter 11 dígitos.')
                    comandosql.execute(f"UPDATE professores SET telefoneprof = '{telefoneProf}' WHERE registro = {registroProf};")

            elif respALteracao == 3:
                if comandosql.rowcount > 0:
                    for registro in tabela:
                        print(f'Atual idade: {registro[3]}')
                    while True:
                        idadeProf = input('Insira a idade do professor: ')
                        if idadeProf.isdigit() and int(idadeProf) >= 18:
                            break
                        print('Idade inválida! Mínimo 18 anos.')
                    comandosql.execute(f"UPDATE professores SET idadeprof = {idadeProf} WHERE registro = {registroProf};")

            elif respALteracao == 4:
                if comandosql.rowcount > 0:
                    for registro in tabela:
                        print(f'Atual salário: {registro[4]}')
                    while True:
                        salarioProf = input('Insira o salário do professor: ')
                        if salarioProf.isdigit() and int(salarioProf) >= 0:
                            break
                        print('Salário inválido! Não pode ser negativo.')
                    comandosql.execute(f"UPDATE professores SET salarioprof = {salarioProf} WHERE registro = {registroProf};")
        
            else:
                print('Selecione uma opção válida!!')

            conexao.commit()
            print('Professor alterado com sucesso!')
            break

    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        comandosql.close()
        conexao.close()
#*****************************************EXCLUIR PROFESSOR************************************************************

def excluirProf():
    try:
        comandosql = conexao.cursor()
        while True:
            registroProf = int(input('Insira o registro do professor que deseja excluir: '))
            comandosql.execute(f'SELECT * FROM professores WHERE registro = {registroProf};')
            tabela = comandosql.fetchall()
            if not tabela:
                print('Professor não registrado!')
                continue
        
            if comandosql.rowcount > 0:
                for registro in tabela:
                    print (f'Atual professor: {registro[1]}')
                if input('Deseja excluir o professor? Digite S para sim: ') == 'S':
                    comandosql.execute(f'DELETE FROM professores WHERE registro = {registroProf};')
                    conexao.commit()
                    print('Professor excluído com sucesso!')
                    break
    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        comandosql.close()
        conexao.close()

#****************************************CONSULTAR PROFESSOR*************************************************************

def consultarProf():
    grid = PrettyTable(['Registro', 'Nome', 'Telefone', 'Idade', 'Salário'])

    try:
        comandosql = conexao.cursor()
        comandosql.execute('select * from professores;')
        tabela = comandosql.fetchall()

        if comandosql.rowcount > 0:
            for registro in tabela:
                grid.add_row([registro[0], registro[1], registro[2], registro[3], registro[4]])
            print(grid)
        else:
            print('Não existem professores cadastrados!!!')
    except Exception as erro:
        print(f'Erro: {erro}')

#********************************************CADASTRAR DISCIPLINA*********************************************************

def cadastrarDisc():
    try:
        comandosql = conexao.cursor()
        codigoDisc = int(input('Insira o código da disciplina: '))

        while True:
            nome = input('Insira o nome da disciplina: ')
            if not nome.isdigit():
                nomeDisc = nome
                break
            print('Nome inválido!')

        comandosql.execute(f"INSERT INTO disciplinas(codigodisc, nomedisc) VALUES ({codigoDisc}, '{nomeDisc}');")
        conexao.commit()
        print('Disciplina cadastrada com sucesso!')

    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        comandosql.close()
        conexao.close()

#*******************************************ALTERAR DISCIPLINA********************************************************

def alterarDisc():
    try:
        comandosql = conexao.cursor()
        while True:
            codigoDisc = int(input('Insira o código da disciplina que deseja alterar: '))
            comandosql.execute(f'SELECT * FROM disciplinas WHERE codigodisc = {codigoDisc};')
            tabela = comandosql.fetchall()
            if not tabela:
                print('Disciplina não registrada!')
                continue

            if comandosql.rowcount > 0:
                for registro in tabela:
                    print (f'Atual disciplina: {registro[1]}')
                    while True:
                        novaDisc = input('Insira o novo nome da disciplina: ')
                        if not novaDisc.isnumeric():
                            break
                        print('Nome inválido!')
                    comandosql.execute(f"UPDATE disciplinas SET nomedisc = '{novaDisc}' WHERE codigodisc = {codigoDisc};")
                
                conexao.commit()
                print('Disciplina alterada com sucesso!')
                break

    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        comandosql.close()
        conexao.close()

#********************************************EXCLUIR DISCIPLINA**********************************************************

def excluirDisc():
    try:
        comandosql = conexao.cursor()

        while True:
            codigoDisc = int(input('Insira o código da disciplina que deseja excluir: '))
            comandosql.execute(f'SELECT * FROM disciplinas WHERE codigodisc = {codigoDisc};')
            tabela = comandosql.fetchall()
            if not tabela:
                print('Disciplina não registrada!')
                continue

            if comandosql.rowcount > 0:
                for registro in tabela:
                    print (f'Atual disciplina: {registro[1]}')
                if input('Deseja excluir a disciplina? Digite S para sim: ') == 'S':
                    comandosql.execute(f'DELETE FROM disciplinas WHERE codigodisc = {codigoDisc};')
                    conexao.commit()
                    print('Disciplina excluída com sucesso!')
                    break

    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        comandosql.close()
        conexao.close()

#**********************************************CONSULTAR DISCIPLINA**********************************************************

def consultarDisc():
    grid = PrettyTable(['Código', 'Nome'])

    try:
        comandosql = conexao.cursor()
        comandosql.execute('select * from disciplinas;')
        tabela = comandosql.fetchall()

        if comandosql.rowcount > 0:
            for registro in tabela:
                grid.add_row([registro[0], registro[1]])
            print(grid)
        else:
            print('Não existem disciplinas cadastradas!!!')
    except Exception as erro:
        print(f'Erro: {erro}')

#*******************************************CADASTRAR DxP***********************************************************

def cadastrarDxP():
    try:
        comandosql = conexao.cursor()
        while True:
            id = int(input('Insira o código da disciplina no curso: '))
            comandosql.execute(f'SELECT codigodisciplinanocurso FROM disciplinaxprofessores WHERE codigodisciplinanocurso = {id}')
            if comandosql.fetchone():
                print('Registro já existente!')
                continue
                
            if id >= 0:
                cDc = id

            codigoDisc = int(input('Insira o código da disciplina: '))
            comandosql.execute(f'SELECT codigodisc FROM disciplinas WHERE codigodisc = {codigoDisc}')
            tabela = comandosql.fetchall()
            if not tabela:
                print('Disciplina não cadastrada!')
                continue    
            
            codigoProf = int(input('Insira o código do professor: '))
            comandosql.execute(f'SELECT codigoprof FROM professores WHERE codigoprof = {codigoProf}')
            comandosql.execute(f'''
                    SELECT COUNT(*) FROM disciplinaxprofessores
                    WHERE codigoprof = {codigoProf};
                ''')
            (qtdProf,) = comandosql.fetchone()
            if qtdProf > 0:
                print('Este professor já está atrelado a uma disciplina. Não é permitido vincular a mais de uma.')
                continue

            tabela = comandosql.fetchall()
            if not tabela:
                print('Professor não cadastrado!')
                continue


            while True:
                codigo = input('Insira o código do curso: ')
                if codigo.isdigit():
                    curso = codigo
                    break
                print('Código inválido!')

            while True:
                    ch = input('Insira a carga horária: ')
                    if ch.isdigit() and int(ch) >= 0:
                        cargaHoraria = int(ch)
                        break
                    print('Salário inválido!')

            while True:
                    al = input('Insira o ano letivo: ')
                    if al.isdigit() and int(al) >= 2025:
                        anoLetivo = int(al)
                        break
                    print('Ano letivo inválido!')

            comandosql.execute(f"INSERT INTO disciplinaxprofessores (codigodisciplinanocurso, coddisciplina, codprofessor, curso, cargahoraria, anoletivo) VALUES ({cDc}, {codigoDisc}, {codigoProf}, '{curso}', {cargaHoraria}, {anoLetivo});")
            conexao.commit()
            print('Cadastro realizado com sucesso!')
            break

    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        comandosql.close()
        conexao.close()

#******************************************ALTERAR DxP**************************************************************

def alterarDxP():
    try:
        comandosql = conexao.cursor()

        while True:
            cDc = int(input('Insira o código do registro que deseja alterar: '))
            comandosql.execute(f'SELECT * FROM disciplinaxprofessores WHERE codigodisciplinanocurso = {cDc}')
            tabela = comandosql.fetchall()
            if not tabela:
                print('Registro não encontrado!')
                continue
            
            print('*' * 60)
            print('ALTERAÇÕES DISPONÍVEIS:')
            print('*' * 60)
            print('1 - Código Disciplina')
            print('2 - Código Professor')
            print('3 - Código Curso')
            print('4 - Carga Horária')
            print('5 - Ano Letivo')
            print('*' * 60)
            respALteracao = int(input('Escolha uma opção: '))
            print('*' * 60)
        
            if respALteracao == 1:
                if comandosql.rowcount > 0:
                    for registro in tabela:
                        print(f'Atual código da disciplina: {registro[1]}')
                    while True:
                        if not tabela:
                            print('Disciplina não registrada!')
                            continue

                        codigoDisc = input('Insira o novo código da disciplina: ')
                        if not codigoDisc.isnumeric():
                            break
                        print('Nome inválido!')
                    comandosql.execute(f"UPDATE disciplinaxprofessores SET codigodisc = '{codigoDisc}' WHERE codigodisciplinanocurso = {cDc};")

            elif respALteracao == 2:
                if comandosql.rowcount > 0:
                    for registro in tabela:
                        print(f'Atual código do professor: {registro[2]}')
                        codigoProf = input('Insira o novo código da disciplina: ')
                        while True:
                            if not tabela:
                                print('Professor não registrado!')
                                continue
                            if not codigoProf.isnumeric():
                                break
                            print('Código inválido!')
                    comandosql.execute(f"UPDATE disciplinaxprofessores SET codigoprof = '{codigoProf}' WHERE codigodisciplinanocurso = {cDc};")

            elif respALteracao == 3:
                if comandosql.rowcount > 0:
                    for registro in tabela:
                        print(f'Atual código do curso: {registro[3]}')
                    while True:
                        codigoCurso = input('Insira o novo código do curso: ')
                        if codigoCurso.isdigit():
                            break
                        print('Código inválido!')
                    comandosql.execute(f"UPDATE disciplinaxprofessores SET curso = {codigoCurso} WHERE codigodisciplinanocurso = {cDc};")

            elif respALteracao == 4:
                if comandosql.rowcount > 0:
                    for registro in tabela:
                        print(f'Atual carga horária: {registro[4]}')
                    while True:
                        cargaHoraria = input('Insira a nova carga horária: ')
                        if cargaHoraria.isdigit() and int(cargaHoraria) >= 0:
                            break
                        print('Carga horária inválida!')
                    comandosql.execute(f"UPDATE disciplinaxprofessores SET cargahoraria = {cargaHoraria} WHERE codigodisciplinanocurso = {cDc};")

            elif respALteracao == 5:
                if comandosql.rowcount > 0:
                    for registro in tabela:
                        print(f'Atual ano letivo: {registro[5]}')
                    while True:
                        anoLetivo = input('Insira o novo ano letivo: ')
                        if anoLetivo.isdigit() and int(anoLetivo) >= 2025:
                            break
                        print('Ano letivo inválido!!')
                    comandosql.execute(f"UPDATE disciplinaxprofessores SET anoletivo = {anoLetivo} WHERE codigodisciplinanocurso = {cDc};")
        
            else:
                print('Selecione uma opção válida!!')

            conexao.commit()
            print('Alteração realizada com com sucesso!')
            break

    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        comandosql.close()
        conexao.close()

#******************************************EXCLUIR DxP*****************************************************************

def excluirDxP():
    try:
        comandosql = conexao.cursor() 

        while True:
            cDc = int(input('Insira o código do registro que deseja excluir: '))
            comandosql.execute(f'SELECT * FROM disciplinaxprofessores WHERE codigodisciplinanocurso = {cDc};')
            tabela = comandosql.fetchall()
            if not tabela:
                print('Registro não encontrado!')
                continue
        
            if comandosql.rowcount > 0:
                for registro in tabela:
                    print (f'Atual registro: {registro[1]}')
                if input('Deseja excluir? Digite S para sim: ') == 'S':
                    comandosql.execute(f'DELETE FROM disciplinaxprofessores WHERE codigodisciplinanocurso = {cDc};')
                    conexao.commit()
                    print('Exclusão realizada com sucesso!')
                    break
    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        comandosql.close()
        conexao.close()

#*********************************************CONSULTAR DxP********************************************************

def consultarDxP():
    grid = PrettyTable(['Código Disciplina no Curso', 'Código Disciplina', 'Código Professor', 'Curso', 'Carga Horária', 'Ano Letivo'])

    try:
        comandosql = conexao.cursor()
        comandosql.execute('select * from disciplinaxprofessores;')
        tabela = comandosql.fetchall()

        if comandosql.rowcount > 0:
            for registro in tabela:
                grid.add_row([registro[0], registro[1], registro[2], registro[3], registro[4], registro[5]])
            print(grid)
        else:
            print('Não existem cadastros!!!')
    except Exception as erro:
        print(f'Erro: {erro}')

#*******************************************CODIGO PRINCIPAL************************************************************

if __name__ == "__main__":
    if abrebanco() == 1:
        while True:
            try:
                print ('*'*60)
                print (' ')
                print('1 - Tabela Professores')
                print('2 - Tabela Disciplinas')
                print('3 - Tabela Disciplinaxprofessores')
                print('4 - Sair')
                print('  ')
                print('*' * 60)
                resp = int(input('Qual tabela deseja acessar: '))
                print('*' * 60)

                if resp == 1:
                    tabelaProf()

                elif resp == 2:
                    tabelaDisc()
                    
                elif resp == 3:
                    tabelaDxP()

                elif resp == 4:
                    conexao.close()
                    comandosql.close()
                    print('Fim do programa')
                    break
                else:
                    print('Selecione uma opção válida!!')

            except Exception as error:
                print(f'Erro: {error}')