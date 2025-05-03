import cv2
import json
import os
import urllib.request
import numpy as np
from pyzbar.pyzbar import decode
import time

class BarcodeScanner:
    def __init__(self, database_path="products_database.json"):
        """
        Inicializa o scanner de código de barras
        
        Args:
            database_path (str): Caminho para o arquivo JSON do banco de dados
        """
        self.database_path = database_path
        self.products_db = self._load_database()
        
    def _load_database(self):
        """Carrega o banco de dados JSON ou cria um novo se não existir"""
        if os.path.exists(self.database_path):
            try:
                with open(self.database_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print(f"Erro ao ler o banco de dados. Criando um novo.")
                return {}
        else:
            # Criar banco de dados com exemplos
            example_db = {
                "7894650940174": {
                    "nome": "Odorizador de ambiente aerossol brisa cítrica de verão Glade",
                    "marca": "Glade",
                    "volume": "360ml",
                    "tipo": "Spray",
                    "categoria": "Limpeza e Perfumaria"
                },
                "7896051020158": {
                    "nome": "Palito Roliço Gina",
                    "marca": "Gina",
                    "quantidade": "200 unidades",
                    "categoria": "Utilidades Domésticas"
                }
            }
            
            with open(self.database_path, 'w', encoding='utf-8') as file:
                json.dump(example_db, file, indent=4, ensure_ascii=False)
            
            return example_db
    
    def save_database(self):
        """Salva o banco de dados atualizado"""
        with open(self.database_path, 'w', encoding='utf-8') as file:
            json.dump(self.products_db, file, indent=4, ensure_ascii=False)
    
    def add_product(self, barcode, product_info):
        """
        Adiciona um novo produto ao banco de dados
        
        Args:
            barcode (str): Código de barras do produto
            product_info (dict): Informações do produto
        """
        self.products_db[barcode] = product_info
        self.save_database()
        print(f"Produto {product_info.get('nome', 'Desconhecido')} adicionado com sucesso!")
    
    def get_product(self, barcode):
        """
        Busca um produto pelo código de barras
        
        Args:
            barcode (str): Código de barras a ser buscado
            
        Returns:
            dict or None: Informações do produto ou None se não encontrado
        """
        return self.products_db.get(barcode)
    
    def scan_with_phone_camera(self, url="http://192.168.1.100:8080/video", quality=70):
        """
        Usa a câmera do celular via IP Webcam para escanear códigos de barras
        
        Args:
            url (str): URL do stream da câmera do celular
        """
        print("\n=== SCANNER DE CÓDIGO DE BARRAS COM CÂMERA DO CELULAR ===")
        print(f"Tentando conectar à câmera do celular em: {url}")
        print("Se estiver usando o IP Webcam, certifique-se de que o aplicativo esteja rodando")
        print("e que o URL esteja correto (verifique o IP mostrado no aplicativo).")
        print("\nPressione 'q' para sair")
        print("Pressione 'a' para adicionar um novo produto")
        print("==============================\n")
        
        try:
            # Modifica a URL para usar uma resolução menor (para melhor desempenho)
            if "ip-webcam" in url.lower() or ":8080" in url:
                # Ajusta URL para IP Webcam com qualidade reduzida
                base_url = url.split("/video")[0]
                url = f"{base_url}/videofeed?quality={quality}"
                print(f"URL otimizada: {url}")
            
            # Tenta conectar à câmera do celular
            cap = cv2.VideoCapture(url)
            
            # Configura buffer menor para reduzir latência
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if not cap.isOpened():
                print("Não foi possível conectar à câmera do celular.")
                print("Verifique se o URL está correto e se o aplicativo IP Webcam está rodando.")
                return
        except Exception as e:
            print(f"Erro ao conectar à câmera do celular: {e}")
            print("Tentando usar a câmera do notebook como fallback...")
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Não foi possível acessar nenhuma câmera. Encerrando programa.")
                return
        
        last_scan = None
        cooldown = 0
        
        while True:
            try:
                # Captura frame por frame (com atraso mínimo)
                # Descarta frames em buffer para reduzir latência
                for _ in range(2):  # Limpa frames antigos
                    cap.grab()
                
                ret, frame = cap.read()
                
                if not ret:
                    print("Falha ao capturar o frame. Tentando reconectar...")
                    cap = cv2.VideoCapture(url)
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    if not cap.isOpened():
                        print("Falha na reconexão. Encerrando programa.")
                        break
                    continue
                
                # Adiciona linhas guia para ajudar no posicionamento do código de barras
                height, width = frame.shape[:2]
                
                # Linha horizontal central
                cv2.line(frame, (0, height//2), (width, height//2), (255, 0, 0), 2)
                
                # Linha vertical central
                cv2.line(frame, (width//2, 0), (width//2, height), (255, 0, 0), 2)
                
                # Retângulo guia no centro
                rect_width, rect_height = width//3, height//4
                rect_x = (width - rect_width)//2
                rect_y = (height - rect_height)//2
                cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (255, 0, 0), 2)
                
                # Texto de instrução
                cv2.putText(frame, "Alinhe o código de barras no retângulo azul", 
                           (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                # Redimensiona o frame para processamento mais rápido
                process_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                
                # Converte para escala de cinza para processamento mais rápido
                gray_frame = cv2.cvtColor(process_frame, cv2.COLOR_BGR2GRAY)
                
                # Decodifica os códigos de barras no frame em escala de cinza
                barcodes = decode(gray_frame)
                
                # Desenha um retângulo ao redor dos códigos de barras detectados
                for barcode in barcodes:
                    # Ajusta as coordenadas ao tamanho original do frame
                    (x, y, w, h) = barcode.rect
                    x *= 2
                    y *= 2
                    w *= 2
                    h *= 2
                    # Extrai as coordenadas do código de barras
                    (x, y, w, h) = barcode.rect
                    
                    # Desenha um retângulo ao redor do código de barras
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # Decodifica os dados do código de barras
                    barcode_data = barcode.data.decode('utf-8')
                    barcode_type = barcode.type
                    
                    # Mostra o tipo e os dados do código de barras na tela
                    text = f"{barcode_type}: {barcode_data}"
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Verifica se é um novo scan (com cooldown para evitar múltiplas leituras)
                    if cooldown <= 0 and barcode_data != last_scan:
                        last_scan = barcode_data
                        cooldown = 30  # frames de cooldown
                        
                        # Busca o produto no banco de dados
                        product = self.get_product(barcode_data)
                        
                        if product:
                            print("\n=== PRODUTO ENCONTRADO ===")
                            for key, value in product.items():
                                print(f"{key}: {value}")
                            print("========================\n")
                            
                            # Mensagem na tela para produto encontrado
                            cv2.putText(frame, "PRODUTO ENCONTRADO!", (x, y + h + 30), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            cv2.putText(frame, product.get("nome", "")[:30], (x, y + h + 60), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        else:
                            print(f"\nERRO: Produto com código {barcode_data} não encontrado no banco de dados.")
                            print("Pressione 'a' para adicionar este produto.\n")
                            
                            # Mensagem de erro na tela
                            cv2.putText(frame, f"ERRO: Produto não encontrado!", (x, y + h + 30), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            cv2.putText(frame, f"Código: {barcode_data}", (x, y + h + 60), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                            cv2.putText(frame, "Pressione 'a' para cadastrar", (x, y + h + 90), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                
                # Reduz o cooldown
                if cooldown > 0:
                    cooldown -= 1
                
                # Redimensiona o frame para caber na tela (se necessário)
                if width > 1200 or height > 800:
                    scale_factor = min(1200 / width, 800 / height)
                    new_width = int(width * scale_factor)
                    new_height = int(height * scale_factor)
                    display_frame = cv2.resize(frame, (new_width, new_height))
                else:
                    display_frame = frame.copy()
                
                # Mostra o resultado
                cv2.imshow('Barcode Scanner (Celular)', display_frame)
                
                # Verifica teclas pressionadas
                key = cv2.waitKey(1) & 0xFF
                
                # Se 'q' for pressionado, sai do loop
                if key == ord('q'):
                    break
                    
                # Se 'a' for pressionado e houver um código de barras lido, adiciona um novo produto
                elif key == ord('a') and last_scan:
                    cap.release()
                    cv2.destroyAllWindows()
                    
                    print(f"\nAdicionando produto com código {last_scan}:")
                    nome = input("Nome do produto: ")
                    marca = input("Marca: ")
                    
                    # Menu para tipo de produto
                    print("\nEscolha a categoria:")
                    print("1. Alimentos")
                    print("2. Bebidas")
                    print("3. Limpeza")
                    print("4. Higiene")
                    print("5. Outros")
                    
                    categoria_opcao = input("Opção: ")
                    categorias = {
                        "1": "Alimentos",
                        "2": "Bebidas",
                        "3": "Limpeza",
                        "4": "Higiene",
                        "5": "Outros"
                    }
                    categoria = categorias.get(categoria_opcao, "Outros")
                    
                    # Informações adicionais
                    info_adicional = {}
                    while True:
                        campo = input("\nAdicionar campo adicional (deixe em branco para encerrar): ")
                        if not campo:
                            break
                        valor = input(f"Valor para '{campo}': ")
                        info_adicional[campo] = valor
                    
                    # Cria o dicionário do produto
                    product_info = {
                        "nome": nome,
                        "marca": marca,
                        "categoria": categoria,
                        **info_adicional
                    }
                    
                    # Adiciona ao banco de dados
                    self.add_product(last_scan, product_info)
                    
                    # Reinicia a câmera
                    cap = cv2.VideoCapture(url)
                    if not cap.isOpened():
                        print("Erro ao reabrir a câmera. Encerrando programa.")
                        break
                    
                    print("\nPressione 'q' para sair")
                    print("Pressione 'a' para adicionar um novo produto")
                    print("==============================\n")
                    
            except Exception as e:
                print(f"Erro durante a execução: {e}")
                continue
        
        # Quando tudo estiver feito, libera a captura
        cap.release()
        cv2.destroyAllWindows()


def main():
    """Função principal"""
    scanner = BarcodeScanner()
    
    # Solicita o IP do celular
    print("=== SCANNER DE CÓDIGO DE BARRAS COM CÂMERA DO CELULAR ===")
    print("Para usar a câmera do celular, instale o aplicativo 'IP Webcam' na Play Store")
    print("Abra o aplicativo, vá até o final e toque em 'Iniciar servidor'")
    print("O aplicativo mostrará um endereço IP (exemplo: http://192.168.1.100:8080)")
    
    ip = input("\nDigite o endereço IP mostrado no aplicativo IP Webcam: ")
    if not ip:
        ip = "http://192.168.1.100:8080/video"  # IP padrão
    elif not ip.startswith("http://"):
        ip = f"http://{ip}"
    if not ip.endswith("/video"):
        ip = f"{ip}/video"
    
    # Configuração de qualidade/performance
    print("\nEscolha o modo de performance:")
    print("1. Alta Qualidade (mais lento)")
    print("2. Balanceado (recomendado)")
    print("3. Alta Performance (mais rápido)")
    
    modo = input("Opção (1-3) [2]: ") or "2"
    
    quality_map = {
        "1": 90,  # Alta qualidade
        "2": 60,  # Balanceado
        "3": 30   # Alta performance
    }
    
    quality = quality_map.get(modo, 60)
    
    print(f"\nConectando a {ip} com qualidade {quality}%...")
    scanner.scan_with_phone_camera(ip, quality)


if __name__ == "__main__":
    main()