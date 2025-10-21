import matplotlib.pyplot as plt
import os

def gerar_grafico_zumbis(caminho_saida="assets/graficos/grafico_zumbis.png"):
    """
    Gráfico da epidemia de zumbis com estilo futurista (600x400 px).
    O Doutor analisa a tendência dos casos em cada distrito para descobrir a origem da infecção.
    """

    # Dias da epidemia
    dias = list(range(1, 11))

    # Distritos futuristas da cidade
    distrito_helios = [3, 5, 9, 14, 22, 32, 45, 60, 78, 90]  # tendência mais precoce → provável origem
    distrito_nebula = [0, 0, 2, 3, 4, 6, 9, 13, 18, 25]      # normal
    distrito_void = [0, 0, 1, 1, 2, 4, 5, 6, 8, 10]          # baixo crescimento

    # Manipulação de Erradon: dado falso inserido para confundir o Doutor
    distrito_nebula[7] = 35  # pico súbito (falso)

    # Cria figura com tema escuro (tamanho exato 600x400 px)
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

    # Fundo e grade neon
    fig.patch.set_facecolor("#0a0f16")
    ax.set_facecolor("#0a0f16")

    # Linhas de tendência com cores de neon
    ax.plot(dias, distrito_helios, marker='o', color="#ff005c", linewidth=2, label="Distrito Hélios")
    ax.plot(dias, distrito_nebula, marker='o', color="#00b3ff", linewidth=2, label="Distrito Nébula (dados alterados)")
    ax.plot(dias, distrito_void, marker='o', color="#00ff99", linewidth=2, label="Distrito Void")

    # Efeitos visuais
    ax.grid(True, linestyle="--", alpha=0.3, color="#00ffaa")

    # Títulos e eixos
    ax.set_title("📊 Propagação da Epidemia de Zumbis — Cidade de Elysium", fontsize=13, color="#00eaff", pad=12)
    ax.set_xlabel("Dia da Epidemia", color="#cccccc", fontsize=10)
    ax.set_ylabel("Número de Infectados", color="#cccccc", fontsize=10)

    # Legenda
    legenda = ax.legend(facecolor="#0f1620", edgecolor="#00ffaa", fontsize=9)
    for text in legenda.get_texts():
        text.set_color("#d9f9ff")

    # Ajuste de margens e salvamento
    plt.tight_layout()

    pasta_saida = os.path.dirname(caminho_saida)
    if pasta_saida and not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    plt.savefig(caminho_saida, dpi=100)
    plt.close(fig)

    print(f"✅ Gráfico futurista salvo em: {os.path.abspath(caminho_saida)} (600x400 px)")


if __name__ == "__main__":
    gerar_grafico_zumbis()
