from fpdf import FPDF
import os
from PIL import Image


class TechnicalReport(FPDF):
    def header(self):
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
        self.set_text_color(30, 41, 59)
        self.cell(0, 10, f"{num}. {label}", align="L", ln=1)
        self.ln(5)

    def chapter_subtitle(self, label):
        self.set_font("helvetica", "B", 12)
        self.set_text_color(71, 85, 105)
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
        self.cell(10)
        self.cell(5, 6, chr(149), align="R")
        self.multi_cell(0, 6, text)
        self.ln(2)


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
pdf.list_item("Frontend: Aplicação SPA estática (HTML5/CSS3/JS).")
pdf.list_item("Backend: API REST com FastAPI (Python).")
pdf.list_item("Servidor Web: Nginx (Proxy Reverso).")

pdf.chapter_title(2, "Modelo de Serviço: PaaS")
pdf.body_text("Optamos pelo Google Cloud Run (Serverless Container).")
pdf.chapter_subtitle("Benefícios")
pdf.list_item("Automação de Infraestrutura e Patching.")
pdf.list_item("Custo Zero quando inativo (Scale to Zero).")
pdf.chapter_subtitle("Statelessness")
pdf.body_text(
    "Containers são efêmeros. Implementamos um registro de visitas local que demonstra que dados em disco são perdidos ao reiniciar o container, validando o conceito de Statelessness."
)

pdf.chapter_title(3, "Arquitetura")
if os.path.exists("docs/diagrama.png"):
    try:
        from PIL import Image

        img = Image.open("docs/diagrama.png")
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save("docs/diagrama_temp.jpg")
        pdf.image("docs/diagrama_temp.jpg", x=10, w=190)
        pdf.ln(5)
        pdf.set_font("helvetica", "I", 9)
        pdf.cell(0, 5, "Figura 1: Arquitetura Simplificada", align="C", ln=1)
        pdf.ln(10)
        os.remove("docs/diagrama_temp.jpg")
    except Exception as e:
        pdf.body_text(f"[Erro imagem: {str(e)}]")
else:
    pdf.body_text("[Imagem não encontrada]")

pdf.chapter_title(4, "Estratégia de Deploy (CI/CD)")
pdf.body_text("Pipeline GitHub Actions automatizada:")
pdf.list_item("1. Commit na master -> Trigger.")
pdf.list_item("2. Build da Imagem Docker.")
pdf.list_item("3. Push para Artifact Registry.")
pdf.list_item("4. Deploy no Cloud Run.")

pdf.chapter_title(5, "Melhorias Avançadas")
pdf.body_text("Recursos implementados para nível sênior:")
pdf.chapter_subtitle("5.1 Observabilidade")
pdf.list_item("Dashboards com Chart.js e Logs em tempo real.")
pdf.chapter_subtitle("5.2 Segurança")
pdf.list_item("Autenticação via Token e Health Check avançado.")
pdf.chapter_subtitle("5.3 UX Premium")
pdf.list_item("Modo Dark/Light e Animações.")
pdf.chapter_subtitle("5.4 Robustez e Confiabilidade")
pdf.list_item("Correção auto. de EOL (Windows/Linux) no Docker build.")
pdf.list_item("Orquestração de serviços no Entrypoint.")
pdf.list_item("Backup Scripts com Fail-safe.")

pdf.chapter_title(6, "Comparativo de Nuvem")
pdf.body_text("IaaS (EC2): Alto controle, Alto gerenciamento.")
pdf.body_text("PaaS (Cloud Run): Médio controle, Escalabilidade auto.")
pdf.body_text("SaaS (Firebase): Baixo controle, Alta velocidade.")

pdf.chapter_title(7, "Conclusão")
pdf.body_text(
    "O projeto atende aos requisitos de arquitetura moderna, com containerização eficiente, CI/CD automatizado e alta disponibilidade via Cloud Run."
)

pdf.output("docs/Documentacao_Tecnica_Final.pdf")
print("PDF Gerado: docs/Documentacao_Tecnica_Final.pdf")
