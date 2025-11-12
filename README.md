# Barcode Scanner Pro - Leitor de Código de Barras com Câmera

> Solução em Python para leitura de códigos de barras em tempo real utilizando a câmera de um smartphone como um scanner sem fio. Ideal para prototipagem de sistemas de inventário e gestão de produtos.

[![Status](https://img.shields.io/badge/Status-Funcional-success)](https://github.com/seu-usuario/barcode-scanner-pro)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB)](https://python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Processamento_de_Imagem-5C3EE8)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

## Sobre o Projeto

O **Barcode Scanner Pro** é uma ferramenta desenvolvida para demonstrar uma abordagem prática e de baixo custo para a leitura de códigos de barras. O projeto transforma um smartphone em um scanner de produtos, comunicando-se em tempo real com um script Python via streaming de vídeo.

Criado como um protótipo funcional, ele resolve a necessidade de um hardware dedicado para leitura de códigos, sendo perfeito para testes, validação de ideias de sistemas de Ponto de Venda (PDV), controle de estoque ou qualquer aplicação que necessite de entrada de dados via código de barras.

## ✨ Funcionalidades

### 🎥 Leitura em Tempo Real com Câmera
- **Conexão sem Fio:** Utiliza a câmera do celular através de aplicativos como o IP Webcam, eliminando a necessidade de cabos.
- **Feedback Visual:** Desenha um retângulo ao redor do código de barras detectado e exibe as informações diretamente na tela.
- **Guias Visuais:** Inclui linhas e um retângulo guia para facilitar o alinhamento do código de barras, melhorando a experiência do usuário.

### 🗃️ Banco de Dados de Produtos
- **Base de Dados Local:** Gerencia um banco de dados de produtos em formato JSON, fácil de ler e manipular.
- **Consulta Instantânea:** Ao ler um código, o sistema busca o produto no banco de dados e exibe suas informações no console.
- **Cadastro Dinâmico:** Permite adicionar novos produtos ao banco de dados diretamente pelo terminal caso um código não seja encontrado.

### ⚙️ Otimização e Usabilidade
- **Ajuste de Performance:** Opções para configurar a qualidade do vídeo, permitindo um balanço entre velocidade de processamento e qualidade da imagem.
- **Interface de Console Interativa:** Guia o usuário para configurar o IP da câmera e adicionar novos produtos de forma intuitiva.
- **Cooldown de Leitura:** Previne múltiplas leituras do mesmo código em sequência, garantindo que cada escaneamento seja único.

## Tecnologias

### Core
- **Python 3.8+** - Linguagem principal do projeto.
- **OpenCV** - Biblioteca para processamento de imagem e captura de vídeo em tempo real.
- **Pyzbar** - Biblioteca para decodificação de códigos de barras.
- **JSON** - Formato utilizado para o banco de dados de produtos.

### Ferramentas
- **IP Webcam** (ou similar) - Aplicativo Android para streaming de vídeo da câmera do celular.

## Pré-requisitos

- [Python 3.8+](https://python.org/downloads/)
- Um smartphone com o aplicativo **IP Webcam** instalado.
- Computador e smartphone conectados à mesma rede Wi-Fi.

## Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/barcode-scanner-pro.git
   cd barcode-scanner-pro
   ```

2. **Instale as dependências**
   
   Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

   Instale os pacotes necessários:
   ```bash
   pip install opencv-python pyzbar numpy
   ```

3. **Execute o sistema**
   ```bash
   python main.py
   ```

## Uso

### Primeira Utilização

1. **Instale e inicie o IP Webcam** no seu smartphone.
2. Na tela inicial do aplicativo, role para baixo e selecione **"Iniciar servidor"**.
3. O aplicativo exibirá um endereço IP na tela (ex: `http://192.168.1.100:8080`).
4. **Execute o script** `main.py` no seu computador.
5. **Insira o endereço IP** exibido no celular quando solicitado pelo script.
6. Aponte a câmera do celular para um código de barras.

### Operação Diária

1. **Escanear um Produto**: Alinhe o código de barras com as guias visuais na tela.
2. **Consultar Informações**: Os detalhes do produto, se encontrado, serão exibidos no terminal.
3. **Cadastrar Novo Produto**: Se o código não for encontrado, pressione a tecla 'a' na janela de vídeo para iniciar o processo de cadastro via terminal.
4. **Sair do Programa**: Pressione a tecla 'q' na janela de vídeo para encerrar a execução.

### Banco de Dados

O sistema cria e utiliza um arquivo `products_database.json` na mesma pasta. A estrutura é um dicionário onde a chave é o código de barras e o valor é um objeto com os detalhes do produto.

**Exemplo (`products_database.json`):**
```json
{
    "7894650940174": {
        "nome": "Odorizador de ambiente aerossol brisa cítrica de verão Glade",
        "marca": "Glade",
        "volume": "360ml",
        "tipo": "Spray",
        "categoria": "Limpeza e Perfumaria"
    }
}
```

## Contribuição

Contribuições são bem-vindas! Se você tem ideias para melhorar o projeto:

1. Fork o projeto.
2. Crie uma nova branch (`git checkout -b feature/minha-feature`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona minha feature'`).
4. Faça push para a branch (`git push origin feature/minha-feature`).
5. Abra um Pull Request.

## FAQ

**P: O sistema funciona com a câmera do notebook?**
R: Sim. Se a conexão com o celular falhar, o script tentará usar a câmera padrão do computador como alternativa.

**P: Posso usar outro aplicativo de streaming de vídeo?**
R: Sim, desde que ele forneça uma URL de streaming de vídeo acessível. Você precisará ajustar a URL no código, se necessário.

**P: O sistema é lento ou está travando.**
R: Tente escolher uma opção de "Alta Performance" ao iniciar o script. Isso reduz a qualidade do vídeo, mas melhora significativamente a velocidade de processamento.

## Suporte

Para suporte técnico ou dúvidas, entre em contato:

- **Email**: [g.moreno.souza05@gmail.com](mailto:g.moreno.souza05@gmail.com)

## Licença

Este projeto está licenciado sob uma Licença Proprietária. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

**Uso Restrito**: Este software é de propriedade exclusiva do autor. O uso comercial, redistribuição ou modificação sem autorização expressa é proibido.

---

<div align="center">
  Desenvolvido por Gustavo Moreno  
  <br><br>
  <a href="https://www.linkedin.com/in/gustavomoreno05" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24" alt="LinkedIn"/>
  </a>
</div>
