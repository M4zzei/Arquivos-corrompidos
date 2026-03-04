import os
import zipfile
import rarfile
sssas
#--- configuacoes ---
rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRAR.exe"
PASTA_ALVO = r"C:/Dev/Teste"

#--- LISTAS ---
arquivos_excluidos = []
arquivos_vistos = {}
pastas_sem_compactados = []
arquivos_duplos = {}


# ----- FUNCOES .ZIP E .RAR -----
def Test_zip(caminho):  #AQ TESTAMOS SE O ARQUIVO .ZIP TA CORROMPIDO OU N
    try:
        with zipfile.ZipFile(caminho, 'r') as z:
            erro = z.testzip()

        if erro is not None:    #NO .ZIP, SE N RETORNAR NADA, EH PQ O ARQUIVO TA SAFE
            os.remove(caminho)
            arquivos_excluidos.append(caminho)
            return True

        return False

    except Exception as e:
        try:
            os.remove(caminho)
            arquivos_excluidos.append(caminho)
            return True
        except: pass
        return False


def Test_rar(caminho):  #AQ TESTAMOS SE O ARQUIVO .RAR TA CORROMPIDO OU N
    try:
        with rarfile.RarFile(caminho) as r:
            r.testrar()     #NO .RAR SE TESTAR E DAR NONE, DEU RUIM
            return False
        
    except Exception as e: 
        try:
            os.remove(caminho)
            arquivos_excluidos.append(caminho)
            return True
        except:
            return False
        
def Test_duplicate():
    pass
        

# ----- CODIGO FONTE ------

for raiz, pastas, arquivos in os.walk(PASTA_ALVO):
    arquivo_valido = False

    for nome in arquivos:
        caminho_completo = os.path.join(raiz, nome)
        nome_puro, extensao = os.path.splitext(nome.lower())
        


        if extensao in [".rar", ".zip"]:
            arquivo_valido = True

            if extensao == ".rar":
                deletado = Test_rar(caminho_completo)
            else:
                deletado = Test_zip(caminho_completo)

            if not deletado:

                tamanho_atual = os.path.getsize(caminho_completo)

                if nome_puro in arquivos_vistos:
        
                    if nome_puro not in arquivos_duplos:
                        arquivos_duplos[nome_puro] = [arquivos_vistos[nome_puro]]

                    arquivos_duplos[nome_puro].append((tamanho_atual, caminho_completo))
                else:
                    arquivos_vistos[nome_puro] = (tamanho_atual, caminho_completo)


    if not arquivo_valido:
        pastas_sem_compactados.append(raiz)


# --- RELATORIO ---

print("\n" + "="*60)
print("RELATÓRIO FINAL DA VARREDURA")
print("="*60)

# EXCLUIDOS
print(f"\nSANEAMENTO: {len(arquivos_excluidos)} arquivo(s) removido(s)")
if arquivos_excluidos:
    for item in arquivos_excluidos:
        print(f" - {item}")
else:
    print(" Nenhum arquivo corrompido foi encontrado.")

# DUPLICADOS
print(f"\nDUPLICADOS: {len(arquivos_duplos)} grupo(s) identificado(s)")
if arquivos_duplos:
    for nome, ocorrencias in arquivos_duplos.items():
        print(f"\nArquivo: {nome}")
        for tam, cam in ocorrencias:
            # CONVERTER 
            if tam < 1024:
                tamanho_formatado = f"{tam} Bytes"
            elif tam < 1024**2:
                tamanho_formatado = f"{tam/1024:.2f} KB"
            else:
                tamanho_formatado = f"{tam/(1024**2):.2f} MB"

            print(f"   {tamanho_formatado} | {cam}")
else:
    print(" Nenhum arquivo duplicado foi encontrado.")

# PASTAS SEM COMPACTADOS
print(f"\nPASTAS SEM ARQUIVOS COMPACTADOS: {len(pastas_sem_compactados)}")
if pastas_sem_compactados:
    for pasta in pastas_sem_compactados:
        print(f" - {pasta}")
else:
    print(" Todas as pastas analisadas contêm arquivos compactados.")

print("\n" + "="*60)
print("FIM DA EXECUÇÃO")

print("="*60)
