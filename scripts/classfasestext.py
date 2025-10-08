import pygame

class Dialogos:
    def __init__(self):
        # Dicionário com os diálogos organizados por fase
        self.dialogos = {
            0: [  # 📝 Fase Tutorial
                ("Jogo", [
                    "Bem-vindo, jovem Samurai.",
                    "Ouça com atenção cada diálogo... eles revelarão pistas importantes.",
                    "Dentro de cada diálogo, existirá um problema criado pelo npc",
                    "Através dele você deve associar o problema ao conceito de estatistico"
                ]),
                ("Jogo", [
                    "Após analisar o diálogo, você tem a opção de comprar conceitos na loja",
                    "Para isso, é necessario eliminar a maioria dos inimigos",
                    "Para passar de fase é necessario responder corretamente a pergunta",
                    "Abrindo o portal e seguindo para a próxima fase!"
                ])
            ],

            1: [  # 🌾 Fase 1 — Cidade com falta de comida
                ("homem", [
                    "Samurai... você não pertence a este tempo, não é?",
                    "Nossa cidade enfrenta um grave problema: falta de comida.",
                    "Não conseguimos ajustar a quantidade que sirva para todos",
                    "para que ninguém passe fome."
                ]),
                ("Samurai", [
                    "Entendo. Isso é um problema sério. Diga-me, o que vocês já tentaram?"
                ]),
                ("homem", [
                    "Temos os dados de produção e consumo. ",
                    "Mas eles não fazem sentido isolados.",
                    "Precisamos de uma forma de resumir tudo em um único valor confiável.",
                    "Sem isso, não conseguimos planejar nem garantir alimento para todos."
                ]),
                ("Samurai", [
                    "Compreendo... mas não conheço métodos desse mundo.",
                    "Talvez haja alguém aqui que possa ajudá-lo."
                ]),
                ("homem", [
                    "Ouvi falar de um viajante mercador que guarda segredos antigos.",
                    "Ele sabe como equilibrar recursos",
                    "encontrando a quantidade certa para todos.",
                    "Mas ele só aparece para aqueles que provam coragem e determinação.",
                    "Para isso, ele necessita de se sentir seguro"
                ]),
                ("homem", [
                    "Samurai, você deve encontrá-lo e aprender com ele.",
                    "Só assim poderemos ajustar a comida e salvar nossa cidade."
                ]),
                ("Samurai", [
                    "Minha missão está clara.",
                    "Buscarei o mercador, aprenderei com ele e retornarei.",
                    "Nada ficará sem solução enquanto eu estiver aqui."
                ])
            ],

            2: [  # 🌡️ Fase 2 — Cidade atormentada por uma epidemia
    ("Dr", [
        
        "Uma nova doença começou a se espalhar rapidamente pela cidade.",
        "Tudo começou com alguns casos isolados nos bairros mais populosos.",
        "Mas em poucos dias, a contaminação se alastrou como fogo.",
        "Os sintomas aparecem de forma súbita "
        
    ]),
     ("Dr", ["enfraquencendo as pessoas."
        "Precisamos agir com rapidez,",
        "mas também com precisão ,",
        "para escolher o tratamento certo."
    ]),
    ("Samurai", [
        "Eu percebi a tensão nas ruas. Há filas enormes nas farmácias ",
        "e muita desinformação circulando.",
        "Erradon está por trás disso, não está? ",
        "Ele adora espalhar dados confusos para criar pânico "
       
    ]),
    ("Dr", [
        "Exatamente. Os registros sobre os tratamentos foram corrompidos.",
        "Alguns dados são verdadeiros, outros foram distorcidos, ",
        "muitos cidadãos estão se guiando apenas por boatos.",
        "Temos quatro tratamentos possíveis, mas cada um apresenta ",
        "diferentes chances de sucesso e riscos."
        
    ]),
    ("Samurai", [
        "Entendo... então não se trata apenas de agir rápido, ",
        "e sim de escolher com sabedoria.",
        "Afinal, um tratamento mal escolhido pode ",
        "gerar novos problemas e agravar a situação."
    ]),
    ("Dr", [
        "Correto. vi num pergaminho, que um tratamento pode ser rápido e barato, ",
        "mas se tiver pouca eficácia, a epidemia continuará se espalhando.",
        "Outro pode ter excelentes resultados, mas exigir mais tempo",
        "para ser aplicado em larga escala."
    ]),
     ("Dr", [
        "Também há opções experimentais que parecem promissoras, ",
        "mas cujos dados foram manipulados por Erradon."
    ]),
    ("Samurai", [
        "Então devemos considerar não só a eficácia,",
        "mas também o risco e a confiabilidade das informações.",
        "É um desafio estatístico… perfeito para um discípulo da Arte dos Dados."
    ]),
    ("Dr", [
        "Samurai, sua ajuda será crucial. ",
        "Avalie cada tratamento vendido pelo mercador com cuidado.",
        "Compare as probabilidades e os possíveis efeitos colaterais, ",
        "e escolha a estratégia mais segura e eficaz para conter a epidemia."
    ]),
    ("Samurai", [
        "Pode contar comigo, doutor. Erradon não vencerá desta vez.",
        "Usarei a razão e o conhecimento da arte dos dados para ",
        "revelar a melhor escolha!"
    ])
    ]


            # novas fases podem ser adicionadas aqui...
        }

    def dialogo_fase(self, fase: int):
        return self.dialogos.get(
            fase,
            [("NARRADOR", ["Nenhum diálogo encontrado para essa fase."])]
        )