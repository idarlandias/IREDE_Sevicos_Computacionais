from fpdf import FPDF
import os
from PIL import Image


class TechnicalReport(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 9)
        self.set_text_color(150, 150, 150)
        self.cell(
            0,
            10,
            "Relatório Técnico Estendido - Arquitetura Cloud & DevOps",
            align="R",
            ln=1,
        )
        self.line(10, 20, 200, 20)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(
            0,
            10,
            f"Página {self.page_no()}/{{nb}} - Projeto Integrador 2026",
            align="C",
        )

    def chapter_title(self, label):
        self.set_font("helvetica", "B", 14)
        self.set_text_color(15, 23, 42)  # Dark Slate
        self.cell(0, 8, label, align="L", ln=1)
        self.set_line_width(0.5)
        self.set_draw_color(15, 23, 42)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(5)

    def section_title(self, label):
        self.set_font("helvetica", "B", 12)
        self.set_text_color(51, 65, 85)
        self.cell(0, 8, label, align="L", ln=1)
        self.ln(2)

    def body_text(self, text):
        self.set_font("helvetica", "", 10)
        self.set_text_color(30, 41, 59)
        self.multi_cell(0, 5, text)
        self.ln(3)

    def list_item(self, text):
        self.set_font("helvetica", "", 10)
        self.set_text_color(30, 41, 59)
        self.cell(5)  # Indent
        self.cell(5, 5, chr(149), align="R")  # Bullet point
        self.multi_cell(0, 5, text)
        self.ln(2)

    def code_snippet(self, code):
        self.set_font("courier", "", 9)
        self.set_fill_color(248, 250, 252)
        self.set_text_color(30, 41, 59)
        self.set_x(15)
        self.multi_cell(180, 5, code, fill=True, border=1)
        self.ln(4)

    def draw_container_diagram(self):
        # Draw a visual representation of the Container Anatomy
        y = self.get_y()
        self.set_fill_color(224, 242, 254)  # Light Blue
        self.rect(20, y, 170, 50, "DF")

        self.set_font("helvetica", "B", 8)
        self.text(25, y + 5, "CONTAINER DOCKER (Debian Slim)")

        # Layers
        self.set_fill_color(255, 255, 255)

        # Process 1: Nginx
        self.rect(30, y + 15, 60, 25, "F")
        self.text(45, y + 25, "NGINX (Port 8080)")
        self.text(35, y + 30, "Static Files + Proxy")

        # Process 2: Python
        self.rect(100, y + 15, 60, 25, "F")
        self.text(115, y + 25, "FastAPI (Port 8000)")
        self.text(110, y + 30, "Logic + Data Access")

        # Connection
        self.line(90, y + 27, 100, y + 27)
        self.text(92, y + 25, "HTTP")

        # Volume
        self.set_fill_color(255, 237, 213)  # Orange
        self.rect(65, y + 42, 60, 6, "F")
        self.text(80, y + 46, "Volume Local (/data)")

        self.ln(55)

    def draw_pipeline_diagram(self):
        y = self.get_y()

        # Steps
        steps = ["GitHub Repo", "Actions Build", "Artifact Registry", "Cloud Run"]
        x = 20
        for step in steps:
            self.rect(x, y, 35, 15)
            self.set_font("helvetica", "B", 8)
            self.text(x + 2, y + 8, step)

            # Arrow
            if step != steps[-1]:
                self.line(x + 35, y + 7, x + 45, y + 7)
                self.line(x + 45, y + 7, x + 42, y + 5)  # arrow head top
                self.line(x + 45, y + 7, x + 42, y + 9)  # arrow head bot

            x += 45

        self.ln(25)

    def draw_files_table(self):
        """Draws a table showing the key containerization files"""
        y = self.get_y()

        # Header
        self.set_fill_color(30, 41, 59)  # Dark slate
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 10)
        self.rect(20, y, 50, 8, "F")
        self.rect(70, y, 120, 8, "F")
        self.text(25, y + 5.5, "Arquivo")
        self.text(75, y + 5.5, "Função")

        # Reset text color
        self.set_text_color(30, 41, 59)
        self.set_font("helvetica", "", 9)

        # Rows
        rows = [
            ("Dockerfile", "Define a imagem do container (Python + Nginx + FastAPI)"),
            ("compose.yml", "Orquestra o container localmente com redes e volumes"),
            ("entrypoint.sh", "Script que inicia os servicos dentro do container"),
        ]

        row_y = y + 8
        for file, desc in rows:
            self.set_fill_color(248, 250, 252)
            self.rect(20, row_y, 50, 10, "F")
            self.rect(70, row_y, 120, 10, "F")
            self.text(25, row_y + 6.5, file)
            self.text(75, row_y + 6.5, desc)
            row_y += 10

        self.ln(45)

    def draw_full_architecture(self):
        """Draws the complete container architecture diagram"""
        y = self.get_y()

        # Main container box (dashed border effect - solid for simplicity)
        self.set_draw_color(100, 100, 100)
        self.set_line_width(0.5)
        self.set_fill_color(15, 23, 42)  # Dark background
        self.rect(20, y, 170, 70, "D")

        # Container title
        self.set_font("helvetica", "B", 10)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(30, 41, 59)
        self.rect(25, y + 3, 160, 8, "F")
        self.text(70, y + 8, "CONTAINER DOCKER (Único)")

        # Base image
        self.set_font("helvetica", "", 9)
        self.set_fill_color(51, 65, 85)
        self.rect(30, y + 15, 155, 7, "F")
        self.text(35, y + 20, "Base: python:3.11-slim")

        # NGINX Box
        self.set_fill_color(56, 189, 248)  # Cyan
        self.rect(35, y + 28, 55, 20, "F")
        self.set_text_color(15, 23, 42)
        self.set_font("helvetica", "B", 9)
        self.text(45, y + 36, "NGINX")
        self.set_font("helvetica", "", 8)
        self.text(48, y + 42, ":8080")
        self.text(40, y + 46, "+ HTML")

        # Arrow
        self.set_draw_color(16, 185, 129)  # Green
        self.set_line_width(1)
        self.line(90, y + 38, 105, y + 38)
        self.line(102, y + 35, 105, y + 38)  # arrow head
        self.line(102, y + 41, 105, y + 38)
        self.set_line_width(0.5)

        # FastAPI Box
        self.set_fill_color(139, 92, 246)  # Purple
        self.rect(110, y + 28, 55, 20, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 9)
        self.text(115, y + 36, "FastAPI (Uvicorn)")
        self.set_font("helvetica", "", 8)
        self.text(128, y + 42, ":8000")
        self.text(125, y + 46, "/api/*")

        # Cron Job Box
        self.set_fill_color(245, 158, 11)  # Orange
        self.set_text_color(15, 23, 42)
        self.rect(35, y + 52, 130, 8, "F")
        self.set_font("helvetica", "", 8)
        self.text(60, y + 57, "+ Cron Job (backup automático)")

        # Arrow down to Cloud Run
        self.set_draw_color(16, 185, 129)
        self.set_line_width(1.5)
        self.line(105, y + 70, 105, y + 80)
        self.line(102, y + 77, 105, y + 80)
        self.line(108, y + 77, 105, y + 80)

        # Cloud Run box
        self.set_fill_color(66, 133, 244)  # Google Blue
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 9)
        self.rect(55, y + 82, 100, 10, "F")
        self.text(60, y + 88, "Google Cloud Run (Executa o container na nuvem)")

        self.set_text_color(30, 41, 59)  # Reset
        self.set_line_width(0.2)
        self.ln(100)


pdf = TechnicalReport()
pdf.alias_nb_pages()
pdf.add_page()

# --- CAPA ---
pdf.set_y(80)
pdf.set_font("helvetica", "B", 26)
pdf.cell(0, 15, "Relatório Técnico de Engenharia", align="C", ln=1)
pdf.set_font("helvetica", "", 16)
pdf.cell(
    0, 10, "Arquitetura de Microsserviços, DevOps e Cloud Computing", align="C", ln=1
)
pdf.ln(20)
pdf.set_font("helvetica", "B", 12)
pdf.cell(0, 10, "Projeto Integrador - Residência em TIC 20", align="C", ln=1)
pdf.cell(0, 10, "Janeiro, 2026", align="C", ln=1)
pdf.add_page()

# --- PÁGINA 1: VISÃO GERAL ---
pdf.chapter_title("1. Visão Geral da Solução")
pdf.body_text(
    "Este documento detalha a arquitetura técnica de uma aplicação web moderna, projetada para alta disponibilidade, escalabilidade e observabilidade no ecossistema Google Cloud Platform (GCP). A solução integra frontend, backend e rotinas de automação em uma unidade de deploy coesa."
)

pdf.section_title("1.1. O Desafio")
pdf.body_text(
    "Desenvolver uma aplicação capaz de suportar tráfego elástico (Scale-to-Zero), com persistência de dados demonstrativa e esteira de CI/CD automatizada, eliminando intervenção manual em produção."
)

pdf.section_title("1.2. Decisão Arquitetural: PaaS (Platform as a Service)")
pdf.body_text(
    "A escolha do Google Cloud Run fundamenta-se na abstração da infraestrutura. Diferente de IaaS (EC2), onde gerenciamos o SO, o Cloud Run permite focar puramente no artefato Docker."
)
pdf.body_text(
    "Benefícios Chave: (1) Cobrança por segundo de uso; (2) HTTPS automático e gerenciado; (3) Integração nativa com Cloud Build e Artifact Registry."
)

if os.path.exists("docs/diagrama.png"):
    pdf.ln(5)
    try:
        from PIL import Image

        img = Image.open("docs/diagrama.png").convert("RGB")
        img.save("docs/diagrama_temp.jpg")
        pdf.image("docs/diagrama_temp.jpg", x=40, w=130)
        os.remove("docs/diagrama_temp.jpg")
    except:
        pass
    pdf.ln(5)

# --- PÁGINA 2: ENGENHARIA DO CONTAINER ---
pdf.add_page()
pdf.chapter_title("2. Engenharia de Containerização")
pdf.body_text(
    'A aplicação não utiliza múltiplos containers orquestrados (como seria com Kubernetes), mas sim um padrão de "Container Híbrido" onde Nginx e Python coexistem. Isso reduz custos e latência de rede interna.'
)

pdf.section_title("2.1. Anatomia do Dockerfile")
pdf.draw_container_diagram()

pdf.body_text(
    "O Dockerfile foi construído em camadas estratégicas para otimizar o cache e garantir segurança:"
)
pdf.list_item("- Camada Base: python:3.11-slim (Debian leve, ~150MB).")
pdf.list_item(
    "- Instalação de Pacotes: Nginx, Cron e dependências de sistema consolidados em um único RUN para reduzir layers."
)
pdf.list_item(
    "- Sanitização (Robustez): Comando sed aplicado aos scripts (.sh) para converter quebras de linha Windows (CRLF) para Unix (LF), eliminando falhas de execução."
)

pdf.section_title("2.2. Orquestração de Processos (Entrypoint)")
pdf.body_text(
    "Como o Docker nativamente roda apenas um processo PID 1, desenvolvemos um entrypoint script que gerencia o ciclo de vida de múltiplos serviços concorrentes:"
)
pdf.code_snippet(
    "#!/bin/bash\ncron &        # Inicia agendador de tarefas\nnginx &       # Inicia Proxy Reverso\nuvicorn app.main:app & # Inicia Backend"
)
pdf.body_text(
    "Isso garante que, se o Backend falhar, o container todo falha e é reiniciado pelo Cloud Run, mantendo a integridade do serviço."
)

# --- PÁGINA 3: BACKEND E API ---
pdf.add_page()
pdf.chapter_title("3. Desenvolvimento Backend e API")
pdf.section_title("3.1. Framework FastAPI")
pdf.body_text(
    "Utilizamos FastAPI por sua performance (ASGI) e validação automática de dados via Pydantic. A API expõe endpoints de gerenciamento e negócio."
)

pdf.section_title("3.2. Estratégia de Persistência Híbrida")
pdf.body_text("Para fins acadêmicos, demonstramos a persistência de dois modos:")
pdf.list_item(
    '1. Efêmera (Stateless): Logs e dados em /data dentro do Cloud Run são perdidos ao reiniciar. Isso valida o conceito de "Twelve-Factor App".'
)
pdf.list_item(
    "2. Simulada (Volume Local): Em ambiente Docker local, o volume é persistente. No Cloud, implementamos um script de Backup Automático via Cron."
)

pdf.section_title("3.3. Observabilidade e Monitoramento")
pdf.body_text('Implementamos endpoints de "White-box Monitoring":')
pdf.list_item("- /api/healthcheck: Verifica latência e escrita em disco.")
pdf.list_item("- /api/metrics: Exporta contadores de visita e uptime.")
pdf.list_item("- /api/logs: Permite leitura remota de logs do sistema.")

# --- PÁGINA 4: CI/CD E AUTOMAÇÃO ---
pdf.add_page()
pdf.chapter_title("4. Pipeline de Entrega Contínua (CI/CD)")
pdf.body_text(
    "A automação é garantida via GitHub Actions, eliminando o erro humano no processo de deploy."
)

pdf.section_title("4.1. Fluxo de Execução")
pdf.draw_pipeline_diagram()

pdf.body_text(
    "O workflow definido em .github/workflows/deploy-cloudrun.yml executa as seguintes etapas críticas:"
)
pdf.list_item("1. Checkout & Auth: Autenticação segura via Service Account JSON Key.")
pdf.list_item("2. Build: Construção da imagem Docker utilizando cache para velocidade.")
pdf.list_item("3. Push: Envio seguro para o Google Artifact Registry (us-central1).")
pdf.list_item(
    "4. Deploy: Atualização atômica do serviço Cloud Run, com migração de tráfego imediata."
)

pdf.section_title("4.2. Segurança no Deploy")
pdf.body_text(
    "Utilizamos Secrets do GitHub para não expor credenciais no código-fonte. O Service Account utilizado (portfolio-deployer) possui permissões mínimas necessárias (Princípio do Menor Privilégio)."
)

# --- PÁGINA 5: ROBUSTEZ E CONCLUSÃO ---
pdf.add_page()
pdf.chapter_title("5. Robustez e Confiabilidade")

pdf.section_title("5.1. Tratamento de Erros e EOL")
pdf.body_text(
    "Um dos maiores desafios em ambientes heterogêneos (Windows Dev -> Linux Prod) é a formatação de arquivos. Implementamos uma higienização automática:"
)
pdf.code_snippet("RUN sed -i 's/\\r$//' /entrypoint.sh")
pdf.body_text(
    "Isso garante que, independentemente do sistema do desenvolvedor, o container final seja 100% compatível com o Kernel Linux."
)

pdf.section_title("5.2. Backup e Disaster Recovery (Simulado)")
pdf.body_text(
    "Um Cron Job executa min-a-min verificando a existência de dados críticos e criando cópias de segurança datadas. Embora o disco seja efêmero, essa lógica prepara a aplicação para cenários reais onde esses backups seriam enviados para um Bucket S3/GCS."
)

# --- PÁGINA 6: UX 2.0 E SCREENSHOTS ---
pdf.add_page()
pdf.chapter_title("6. Experiência do Usuário Avançada (UX 2.0)")

pdf.section_title("6.1. Micro-interações e Feedback Visual")
pdf.body_text(
    "Para elevar a experiência do usuário a um nível profissional, foram implementadas funcionalidades visuais modernas que demonstram domínio de CSS3 e JavaScript:"
)
pdf.list_item(
    "- Toast Notifications: Notificações elegantes no topo da tela substituindo os alerts nativos do navegador."
)
pdf.list_item(
    "- Confetti Animation: Explosão de 50 partículas coloridas ao registrar visitas, criando uma micro-interação celebratória."
)
pdf.list_item(
    "- Skeleton Loaders: Retângulos animados com efeito shimmer durante o carregamento de dados."
)
pdf.list_item(
    "- Staggered Card Animations: Cards entram em sequência com delay escalonado."
)

pdf.section_title("6.2. Dashboards de Monitoramento")
pdf.body_text(
    "Gráficos circulares em SVG animados (gauges) simulam o uso de CPU e Memória RAM, atualizando dinamicamente a cada 5 segundos. Essa feature demonstra a capacidade de criar dashboards de monitoramento em tempo real."
)

pdf.chapter_title("7. Evidências de Containerização")

pdf.section_title("7.1. Arquivos de Configuração")
pdf.body_text(
    "A tabela abaixo apresenta os arquivos essenciais para a containerização do projeto:"
)

# Draw the files table
pdf.draw_files_table()

pdf.section_title("7.2. Arquitetura do Container")
pdf.body_text(
    "O diagrama abaixo ilustra como funciona a arquitetura do container único, demonstrando a comunicação entre Nginx e FastAPI, além do Cron Job para backups automáticos:"
)

# Draw the architecture diagram
pdf.draw_full_architecture()

pdf.body_text(
    "O percentual de Dockerfile (2.4%) no repositório é típico para projetos containerizados, pois Dockerfiles são naturalmente concisos (~50 linhas), enquanto o código de aplicação (Python, CSS, JavaScript) é mais extenso."
)

pdf.chapter_title("8. Conclusão")
pdf.body_text(
    "O projeto entrega uma arquitetura de referência para modernização de aplicações. Combinando a leveza do Nginx, a velocidade do FastAPI e a automação do Cloud Run, atingimos um nível de maturidade de software (SRE/DevOps) compatível com padrões de mercado."
)
pdf.body_text(
    "A aplicação é resiliente, observável e segura, pronta para escalar horizontalmente de acordo com a demanda."
)
pdf.body_text(
    "Acesse o projeto online: https://portfolio-docker-cloudrun-728889819893.us-central1.run.app"
)

pdf.output("docs/Documentacao_Tecnica_Estendida.pdf")
print("Novo PDF Gerado (6 Páginas): docs/Documentacao_Tecnica_Estendida.pdf")
