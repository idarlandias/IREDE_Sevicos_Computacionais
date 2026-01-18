# Relatório Técnico: Projeto Integrador Docker e Nuvem

## 1. Descrição da Aplicação

A aplicação consiste em um portfólio institucional web integrado a uma API de monitoramento.

- **Frontend**: Aplicação SPA (Single Page Application) estática, desenvolvida com HTML5, CSS3 (efeitos de glassmorphism) e JavaScript Vanilla.
- **Backend**: API REST desenvolvida em Python com **FastAPI**, responsável por fornecer dados de saúde do sistema (health check) e métricas de uso (uptime, contador de visitas persistente).
- **Servidor Web**: **Nginx**, atuando como servidor de arquivos estáticos e Proxy Reverso para a API, tudo encapsulado em um único container.

## 2. Modelo de Serviço Escolhido: PaaS (Platform as a Service)

Optamos por utilizar o **Google Cloud Run**, um serviço de PaaS gerenciado "Serverless" para containers.

### Justificativa

O modelo PaaS foi escolhido pois abstrai a complexidade de gerenciamento do Sistema Operacional e do Hardware subjacente, permitindo focar exclusivamente no código e no container da aplicação.

### Benefícios

- **Automação**: O Google gerencia a infraestrutura, atualizações de segurança do host e provisionamento de recursos.
- **Custo-Benefício**: Modelo "Pay-as-you-go" (pague pelo uso). Se ninguém acessa o site, o custo tende a zero (dependendo da configuração de instâncias mínimas).
- **Simplicidade Operacional**: Deploy simplificado através de uma única imagem Docker, sem necessidade de configurar clusters Kubernetes complexos manualmente (embora o Cloud Run use Knative por baixo).

### Desafios

- **Cold Starts**: Como o serviço pode escalar a zero, a primeira requisição após um período de inatividade pode levar alguns segundos a mais para carregar enquanto o container é iniciado.
- **Estado (Statelessness)**: Aplicações no Cloud Run devem ser preferencialmente _stateless_. A persistência de dados (como o nosso contador) em arquivos locais do container é efêmera e perdida se o container reiniciar. Solução ideal seria usar um banco de dados externo ou Google Cloud Storage, mas para este projeto acadêmico, demonstramos a persistência via volumes locais no ambiente Docker de desenvolvimento.

## 3. Arquitetura e Conceitos Aplicados

### 3.1 Docker e Containerização

Utilizamos um **Dockerfile** que prepara uma imagem híbrida baseada em `python:3.11-slim`, instalando o `nginx` sobre ela. Isso permite que um único artefato de deploy contenha tanto a lógica de apresentação quanto a de negócio, simplificando a esteira de deploy.

### 3.2 Escalabilidade e Elasticidade

O Cloud Run oferece **Elasticidade Automática**.

- Se o tráfego aumentar repentinamente (ex: campanha de marketing), a plataforma provisiona automaticamente novas instâncias do container para lidar com a carga (Scale Out).
- Quando o tráfego diminui, as instâncias são desligadas (Scale In), otimizando custos.

### 3.3 Responsabilidade Compartilhada

No modelo PaaS/Cloud Run:

- **Provedor (Google)**: Responsável pela segurança física dos datacenters, rede, hardware e do sistema operacional host onde os containers rodam.
- **Cliente (Nós)**: Responsável pela segurança da aplicação (código), das dependências dentro do container (atualizar bibliotecas Python/Nginx) e pelo gerenciamento de acesso (IAM).

## 4. Estratégia de Deploy (CI/CD)

Implementamos uma esteira de Integração e Entrega Contínuas (CI/CD) utilizando **GitHub Actions**.

### Fluxo Automatizado

1.  **Trigger**: Commit na branch `main`.
2.  **Build**: O GitHub Actions constrói a imagem Docker.
3.  **Push**: A imagem é enviada para o **Google Artifact Registry** (repositório privado e seguro de imagens).
4.  **Deploy**: O comando `gcloud run deploy` atualiza o serviço em produção com a nova imagem.

Essa abordagem elimina erros manuais de deploy e garante que a versão em produção esteja sempre sincronizada com o código aprovado no repositório.
