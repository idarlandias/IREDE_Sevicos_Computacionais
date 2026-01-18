# Portfolio Docker & Nuvem

[![Cloud Run Deploy](https://img.shields.io/badge/Deploy-Google_Cloud_Run-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://portfolio-docker-cloudrun-728889819893.us-central1.run.app)
[![Status](https://img.shields.io/website?url=https%3A%2F%2Fportfolio-docker-cloudrun-728889819893.us-central1.run.app%2Fapi%2Fhealth&style=for-the-badge&label=Service%20Status)](https://portfolio-docker-cloudrun-728889819893.us-central1.run.app)

> **Link Oficial:** [https://portfolio-docker-cloudrun-728889819893.us-central1.run.app](https://portfolio-docker-cloudrun-728889819893.us-central1.run.app)

Aplicação demonstrativa de arquitetura containerizada implantada no Google Cloud Run, atendendo aos requisitos do Projeto Integrador.

## 📋 Visão Geral

Este projeto implementa uma página institucional (Portfólio) servida junto a uma API REST em um único container Docker.

- **Frontend**: HTML5/CSS3 moderno (Glassmorphism), servido pelo Nginx.
- **Backend**: FastAPI (Python) expondo status e contador de visitas.
- **Infraestrutura**: Google Cloud Run (PaaS), Deployment Contínuo (CI/CD) via GitHub Actions.

![Arquitetura do Projeto](docs/diagrama.png)
_Diagrama simplificado da arquitetura na nuvem._

## 🔗 Link do Projeto (Online)

**[Acesse o Portfólio no Google Cloud Run](https://portfolio-docker-cloudrun-728889819893.us-central1.run.app)**

## 🚀 Como Rodar Localmente (Docker)

Certifique-se de ter o Docker instalado.

1. Clone o repositório e acesse a pasta:

   ```bash
   git clone <URL_DO_REPO>
   cd portfolio-docker-cloudrun
   ```

2. Suba o ambiente com Docker Compose:

   ```bash
   docker compose up --build
   ```

3. Acesse:
   - **Frontend**: [http://localhost:8080](http://localhost:8080)
   - **API Status**: [http://localhost:8080/api/status](http://localhost:8080/api/status)

O volume persistente `./data` será criado na raiz do projeto, mantendo a contagem de visitas mesmo após reiniciar o container.

## ☁️ Deploy na Nuvem (Google Cloud Run)

O projeto está configurado com CI/CD. Ao fazer push na branch `main`, o GitHub Actions executa:

1. **Build** da imagem Docker.
2. **Push** para o Google Artifact Registry.
3. **Deploy** automático no Cloud Run.

URL de Produção: [INSERIR URL APÓS DEPLOY]

## 🛠️ Estrutura do Projeto

```
/
├── app/                  # FastAPI Application
├── web/                  # Frontend Estático (HTML/CSS/JS)
├── nginx/                # Configuração do Proxy Reverso
├── docs/                 # Documentação e Relatório
├── .github/workflows/    # Pipeline CI/CD
├── Dockerfile            # Definição do Container (Multi-service)
└── compose.yml           # Orquestração Local
```

---

**Entregáveis:**

- [x] Dockerfile funcional
- [x] Simulação local com Rede, Porta e Volume (`compose.yml`)
- [x] Estratégia de Deploy Automatizada
- [x] Documentação Técnica (`docs/relatorio.md`)
