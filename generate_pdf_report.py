from fpdf import FPDF
import os
from PIL import Image


class TechnicalReport(FPDF):
    def header(self):
        # Logo or Title on every page
        self.set_font("helvetica", "B", 10)
        self.set_text_color(150, 150, 150)
        self.cell(
            0,
            10,
            "Relatório Técnico: Projeto Integrador Docker e Nuvem",
            align="R",
            ln=1,
        )
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, num, label):
        self.set_font("helvetica", "B", 16)
        self.set_text_color(30, 41, 59)  # Dark Blue
        self.cell(0, 10, f"{num}. {label}", align="L", ln=1)
        self.ln(5)

    def chapter_subtitle(self, label):
        self.set_font("helvetica", "B", 12)
        self.set_text_color(71, 85, 105)  # Greyish Blue
        self.cell(0, 10, label, align="L", ln=1)
        self.ln(3)

    def body_text(self, text):
        self.set_font("helvetica", "", 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln(5)

    def list_item(self, text):
        self.set_font("helvetica", "", 11)
        self.set_text_color(0, 0, 0)
        self.cell(10)  # Indent
        self.cell(5, 6, chr(149), align="R")  # Bullet
        self.multi_cell(0, 6, text)
        self.ln(2)


# Create PDF
pdf = TechnicalReport()
pdf.alias_nb_pages()
pdf.add_page()

# Title Page
pdf.set_y(60)
pdf.set_font("helvetica", "B", 24)
pdf.set_text_color(15, 23, 42)
pdf.cell(0, 10, "Relatório Técnico", align="C", ln=1)
pdf.ln(5)
pdf.set_font("helvetica", "", 16)
pdf.set_text_color(100, 116, 139)
pdf.cell(0, 10, "Projeto Integrador: Docker e Nuvem", align="C", ln=1)
pdf.ln(40)
pdf.set_font("helvetica", "B", 12)
pdf.cell(0, 10, "Residência em TIC 20 - Janeiro 2026", align="C", ln=1)
pdf.add_page()

# Content
pdf.chapter_title(1, "Descrição da Aplicação")
pdf.body_text(
    "A aplicação consiste em um portfólio institucional web integrado a uma API de monitoramento, desenvolvido para demonstrar conceitos de arquitetura em nuvem e DevOps."
)
pdf.list_item(
    "Frontend: Aplicação SPA estática, desenvolvida com HTML5, CSS3 (efeitos de glassmorphism) e JavaScript Vanilla."
)
pdf.list_item(
    "Backend: API REST desenvolvida em Python com FastAPI, fornecendo dados de saúde do sistema e métricas."
)
pdf.list_item(
    "Servidor Web: Nginx, atuando como proxy reverso e servidor estático em um único container."
)

pdf.chapter_title(2, "Modelo de Serviço: PaaS")
pdf.body_text(
    'Optamos por utilizar o Google Cloud Run, um serviço de PaaS gerenciado "Serverless".'
)
pdf.chapter_subtitle("Justificativa")
pdf.body_text(
    "O modelo PaaS abstrai a complexidade do Sistema Operacional, permitindo focar exclusivamente no código."
)
pdf.chapter_subtitle("Benefícios")
pdf.list_item("Automação: Gerenciamento total da infraestrutura pelo Google.")
pdf.list_item('Economia: Modelo "Pay-as-you-go" (Custo zero se inativo).')
pdf.chapter_subtitle("Statelessness e Desafios")
pdf.body_text(
    "Containers no Cloud Run são efêmeros. Demonstramos isso implementando um registro de visitas local que é reiniciado com o container, provando a necessidade de serviços de banco de dados externos para persistência real em nuvem."
)

pdf.chapter_title(3, "Arquitetura")
if os.path.exists("docs/diagrama.png"):
    try:
        # Convert to RGB JPG to avoid PNG compatibility issues in FPDF
        img = Image.open("docs/diagrama.png")
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save("docs/diagrama_temp.jpg")

        pdf.image("docs/diagrama_temp.jpg", x=10, w=190)
        pdf.ln(5)
        pdf.set_font("helvetica", "I", 9)
        pdf.cell(0, 5, "Figura 1: Arquitetura Simplificada da Solução", ln=1, align="C")
        pdf.ln(10)

        # Cleanup
        try:
            os.remove("docs/diagrama_temp.jpg")
        except:
            pass
    except Exception as e:
        pdf.body_text(f"[Imagem não pode ser carregada: {str(e)}]")
else:
    pdf.body_text("[Imagem do diagrama não encontrada]")

pdf.chapter_title(4, "Estratégia de Deploy (CI/CD)")
pdf.body_text("Implementamos uma pipeline completa de CI/CD usando GitHub Actions:")
pdf.list_item("1. Trigger: Commit na branch main.")
pdf.list_item("2. Build: Construção da imagem Docker.")
pdf.list_item("3. Push: Upload para o Google Artifact Registry.")
pdf.list_item("4. Deploy: Atualização automática do serviço no Cloud Run.")

pdf.chapter_title(5, "Melhorias Avançadas")
pdf.body_text("Implementamos recursos nível sênior para demonstrar domínio técnico:")
pdf.list_item("Dashboards: Gráficos em tempo real com Chart.js.")
pdf.list_item("Segurança: Autenticação via Token e Logs em tempo real.")
pdf.list_item("Backup: Cron Job simulando backup automático de dados.")
pdf.list_item("UX: Modo Escuro/Claro e micro-interações.")

pdf.chapter_title(6, "Conclusão")
pdf.body_text(
    "O projeto cumpre todos os requisitos, demonstrando uma aplicação Full-Stack containerizada, escalável e com deploy automatizado, pronta para ambientes de produção modernos."
)

# Output
pdf.output("docs/Documentacao_Tecnica_Final.pdf")
print("PDF Gerado com sucesso!")
