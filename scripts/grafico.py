import matplotlib.pyplot as plt
import numpy as np
import os

def gerar_grafico_fase5(caminho_saida="assets/graficos/grafico_dispersao_feedback_fase5.png"):
    """
    Gráfico de dispersão honesto, sem manipulação de eixos.
    Rosa criou este gráfico para estudar a relação entre o vento e o crescimento das flores.
    Agora o gráfico aparece de forma proporcional e verdadeira.
    """

    # Gera dados fictícios
    np.random.seed(42)
    vento = np.random.uniform(0, 20, 30)
    crescimento = 2 * np.random.normal(5, 2, 30)  # sem correlação real

    # Estilo antigo
    plt.style.use("seaborn-v0_8-muted")
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

    # Fundo envelhecido (bege claro)
    fig.patch.set_facecolor("#f3e9d2")
    ax.set_facecolor("#f3e9d2")

    # Pontos no estilo clássico
    ax.scatter(vento, crescimento, color="#5b3a29", edgecolors="#2b1d13", s=70)

    # ❌ Sem manipulação de eixos
    # ❌ Sem set_aspect artificial
    # ✔️ Eixos automáticos
    ax.set_xlim(min(vento) - 1, max(vento) + 1)
    ax.set_ylim(min(crescimento) - 1, max(crescimento) + 1)

    # Título e rótulos com estilo antigo
    ax.set_title("Crescimento das Flores x Velocidade do Vento",
                 fontsize=13, color="#3b2f2f", pad=10)
    ax.set_xlabel("Velocidade do Vento (km/h)", color="#4b3e2b", fontsize=11)
    ax.set_ylabel("Altura das Flores (cm)", color="#4b3e2b", fontsize=11)

    # Grade sutil e envelhecida
    ax.grid(True, linestyle="--", alpha=0.4, color="#8c7b6b")

    # Moldura discreta
    for spine in ax.spines.values():
        spine.set_color("#6b594a")
        spine.set_linewidth(1.2)

    plt.tight_layout()

    pasta_saida = os.path.dirname(caminho_saida)
    if pasta_saida and not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    plt.savefig(caminho_saida, dpi=100)
    plt.close(fig)

    print(f"✅ Gráfico da Fase 5 salvo em: {os.path.abspath(caminho_saida)} (600x400 px)")


if __name__ == "__main__":
    gerar_grafico_fase5()
