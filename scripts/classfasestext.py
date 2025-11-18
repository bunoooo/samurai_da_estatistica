import pygame

class Dialogos:
    def __init__(self):
        # Dicionário com os diálogos organizados por fase
        self.dialogos = {
            0: [  # Fase Tutorial
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

            1: [  # Fase 1 — Cidade com falta de comida
                ("Chefe", [
                    "Samurai... você não pertence a este tempo, não é?",
                    "Nossa cidade enfrenta um grave problema: falta de comida.",
                    " Não conseguimos ajustar a quantidade que sirva para todos",
                    "para que ninguém passe fome."
                ]),
                ("Samurai", [
                    "Entendo. Isso é um problema sério. Diga-me, o que vocês já tentaram?"
                ]),
                ("Chefe", [
                    "Temos os dados de produção e consumo. ",
                    "Mas eles não fazem sentido isolados.",
                    "Precisamos de uma forma de resumir tudo em um único valor confiável.",
                    "Sem isso, não conseguimos planejar"
                ]),
                ("Chefe", [
                    "é preciso que haja quantidade suficiente ",
                    "para a próxima colheita",
                    "sabemos que algumas familias comem muito mais que outras"
                ]),
                ("Samurai", [
                    "Compreendo... mas não conheço métodos desse mundo.",
                    "Talvez haja alguém aqui que possa ajudá-lo."
                ]),
                ("Chefe", [
                    "Ouvi falar de um viajante mercador que guarda segredos antigos.",
                    "Ele sabe como equilibrar recursos",
                    "encontrando a quantidade certa para todos."
                ]),
                ("Chefe", [
                    "Samurai, você deve encontrá-lo e aprender com ele.",
                    "Só assim poderemos ajustar a comida e salvar nossa cidade."
                ]),
                ("Samurai", [
                    "Minha missão está clara.",
                    "Buscarei o mercador, aprenderei com ele e retornarei.",
                    "Nada ficará sem solução enquanto eu estiver aqui."
                ])
            ],

            2: [  # Fase 2 — Cidade atormentada por uma epidemia
                ("Chefe", [
                    "Uma nova doença começou a se espalhar rapidamente pela cidade.",
                    "Tudo começou com alguns casos isolados nos bairros mais populosos.",
                    "Mas em poucos dias, a contaminação se alastrou como fogo.",
                    "Os sintomas aparecem de forma súbita "
                ]),
                ("Chefe", [
                    "enfraquecendo as pessoas.",
                    "Precisamos agir com rapidez,",
                    "mas também com precisão,",
                    "para escolher o tratamento certo."
                ]),
                ("Jack", [
                    "Eu percebi a tensão nas ruas. Há filas enormes nas farmácias ",
                    "e muita desinformação circulando.",
                    "Erradon está por trás disso, não está?",
                    "Ele adora espalhar dados confusos para criar pânico."
                ]),
                ("Chefe", [
                    "Exatamente. Os registros sobre os tratamentos foram corrompidos.",
                    "Alguns dados são verdadeiros, outros foram distorcidos,",
                    "muitos cidadãos estão se guiando apenas por boatos.",
                    "Temos quatro tratamentos possíveis, mas cada um apresenta ",
                    "diferentes chances de sucesso e riscos."
                ]),
                ("Jack", [
                    "Entendo... então não se trata apenas de agir rápido,",
                    "e sim de escolher com sabedoria.",
                    "Afinal, um tratamento mal escolhido pode ",
                    "gerar novos problemas e agravar a situação."
                ]),
                ("Chefe", [
                    "Correto. Vi num pergaminho que um tratamento pode ser rápido e barato,",
                    "mas se tiver pouca eficácia, a epidemia continuará se espalhando.",
                    "Outro pode ter excelentes resultados, mas exigir mais tempo",
                    "para ser aplicado em larga escala."
                ]),
                ("Chefe", [
                    "Também há opções experimentais que parecem promissoras,",
                    "mas cujos dados foram manipulados por Erradon."
                ]),
                ("Jack", [
                    "Então devemos considerar não só a eficácia,",
                    "mas também o risco e a confiabilidade das informações.",
                    "É um desafio estatístico… perfeito para um discípulo da Arte dos Dados."
                ]),
                ("Chefe", [
                    "Samurai, sua ajuda será crucial.",
                    "Avalie cada tratamento vendido pelo mercador com cuidado.",
                    "Compare as probabilidades e os possíveis efeitos colaterais,",
                    "e escolha a estratégia mais segura e eficaz para conter a doença."
                ]),
                ("Jack", [
                    "Pode contar comigo, doutor. Erradon não vencerá desta vez.",
                    "Usarei a razão e o conhecimento da arte dos dados para",
                    "revelar a melhor escolha!"
                ])
            ],

            3: [  #  Fase 3 — A Maldição das Almas Perdidas
                ("Ceifador", [
                    "Samurai... bem-vindo ao lugar onde até a morte perdeu força.",
                    "Desde a maldição, as almas que eu colhia fugiram do meu chamado.",
                    "Agora vagam perdidas, voltando como esqueletos amaldiçoados.",
                    "Tentei todos os rituais, mas nenhum trouxe a ordem de volta."
                ]),
                ("Jack", [
                    "Então a maldição está além da sua compreensão.",
                    "Diga-me, há algum padrão no modo como as almas se perdem?"
                ]),
                ("Ceifador", [
                    "Talvez sim... um sábio me deixou este antigo gráfico.",
                    "Ele mostra quantas almas se perderam por tipo de maldição.",
                    "Mas esses números me confundem, só sinto a dor delas.",
                    "Não consigo entender o que o gráfico realmente revela."
                ]),
                ("Jack", [
                    "Deixe-me ver...",
                    "Entendo. Cada barra representa uma causa possível da maldição.",
                    "Se observarmos qual causa tem mais almas perdidas, ",
                    "saberemos onde agir primeiro."
                ]),
                ("Ceifador", [
                    "Então devo escolher o ritual que enfraquece a", 
                    "causa mais devastadora?",
                    "Isso exigirá sabedoria... e talvez algumas moedas."
                ]),
                ("Jack", [
                    "Exato. Visitarei a loja de rituais.",
                    "Cada ritual foi feito para combater uma das causas ",
                    "possíveis da maldição.",
                    "Mas apenas um reduzirá o maior número de almas perdidas."
                ]),
                ("Ceifador", [
                    "Então olhe bem o gráfico, Samurai.",
                    "Descubra o coração desta maldição...",
                    "E compre o ritual certo antes que o silêncio da morte ",
                    "se torne eterno."
                ]),
                ("Jack", [
                    "Entendido. Onde há dados, há esperança.",
                    "Vou interpretar o gráfico e libertar as almas aprisionadas."
                ])
                    ] ,      
                    4: [  # Fase 4 — Epidemia de Zumbis e Distritos Futuristas
                ("Doutor", [
                    "Jack, você chegou à cidade infestada de zumbis.",
                    "A população está em pânico e as ruas, desertas.",
                    "Há 10 dias a epidemia começou a se espalhar.",
                    "O primeiro zumbi foi contaminado pelo Virus CognoZombi."
                ]),
                ("Doutor", [
                    "Precisamos descobrir em qual distrito tudo começou.",
                    "O gráfico mostra a evolução de cada distrito.",
                    "Alguns picos podem ter sido manipulados por Erradon.",
                    "Nem todas as tendências são confiáveis."
                ]),
                ("Doutor", [
                    "Analise cada dado com cuidado, Jack.",
                    "Cada distrito apresenta uma curva diferente.",
                    "A interpretação correta é essencial.",
                    "Somente assim podemos conter a epidemia desde a raiz."
                ]),
                ("Jack", [
                    "Entendido, Doutor. A cidade está em caos total.",
                    "Precisamos localizar o primeiro zumbi infectado.",
                    "Cada detalhe do gráfico será crucial.",
                    "Vamos descobrir a origem do Virus CognoZombi."
                ])
            ],

          
             5:  [
    ("Rosa", [
        "Jack! Você voltou! Há boatos de que viajou pelo tempo...",
        "Mas algo terrível aconteceu enquanto esteve longe.",
        "Erradon espalhou desinformação entre os estudiosos da vila.",
        "Agora todos andam confusos com gráficos e números sem sentido."
    ]),
    ("Jack", [
        "Erradon... então ele começou seus planos.",
        "Sempre soube que ele tentaria distorcer o conhecimento,",
        "não só os fatos. Mas o que exatamente ele fez desta vez, Rosa?"
    ]),
    ("Rosa", [
        "Eu criei um gráfico sobre o vento e o crescimento das flores da colina.",
        "Mas desde que Erradon interferiu, algo parece errado.",
        "O gráfico parece sugerir uma relação forte, mas a escala está estranha.",
        "Talvez eu tenha caído em uma das ilusões dele."
    ]),
    ("Jack", [
        "Deixe-me ver esse gráfico, Rosa. Hmm...",
        "Repare como o eixo Y está bem comprimido enquanto o eixo X é muito maior.",
        "Essa diferença de escala cria a falsa impressão de uma tendência.",
        "Mas se olharmos só os pontos, não existe padrão real."
    ]),
    ("Rosa", [
        "Então o problema não é nos dados em si, e sim na forma como o gráfico foi mostrado!",
        "Erradon deve ter manipulado a escala para enganar as pessoas!",
        "Como posso aprender a identificar quando um gráfico está distorcido?"
    ]),
    ("Jack", [
        "Um gráfico honesto mostra a verdade dos dados.",
        "Devemos sempre verificar as escalas, a dispersão, a amostra e o contexto.",
        "Só assim descobrimos se há de fato um padrão ou se é apenas uma ilusão visual."
    ]),
    ("Jack", [
        "Venha, Rosa. Vamos reconstruir este gráfico e revelar a verdade",
        "escondida entre esses pontos dispersos."
    ])
],
          
            6: [
                ("Erradon", [
                    "Finalmente nos encontramos, pequeno Jack.",
                    "Sou Erradon, o senhor da distorção e da incerteza.",
                    "Seus cálculos vacilam, seus golpes erram o alvo.",
                    "Você luta contra o erro, mas o erro é parte de você!"
                ]),
                ("Jack", [
                    "Você é quem espalha confusão entre as medidas.",
                    "Faz o certo parecer duvidoso e o errado confiável.",
                    "Suas ilusões distorcem o julgamento dos sábios.",
                    "Mas eu aprendi a enxergar por trás dos desvios."
                ]),
                ("Erradon", [
                    "Hahaha! E o que aprendeu, pequeno samurai?",
                    "Cada tentativa sua gera novos erros e incertezas.",
                    "Quanto mais ajusta, mais se afasta da verdade.",
                    "Sua própria busca é o alimento da variância!"
                ]),
                ("Jack", [
                    "Então é isso... você vive do excesso e do desequilíbrio.",
                    "Não basta atacar com força, é preciso medir com clareza.",
                    "Se eu for constante demais, caio no viés.",
                    "Se variar demais, me perco no caos."
                ]),
                ("Erradon", [
                    "Exato! Nenhum golpe pode escapar desse paradoxo.",
                    "A precisão e o erro dançam lado a lado para sempre.",
                    "Você jamais atingirá meu núcleo, Jack.",
                    "Sou a incerteza viva!"
                ]),
                ("Jack", [
                    "Talvez não precise escapar, apenas entender o ritmo.",
                    "Seus extremos se anulam quando estão em harmonia.",
                    "Então, existe um ponto onde a verdade se equilibra.",
                    "É lá que meu golpe deve atingir..."
                ]),
                ("Erradon", [
                    "O que está dizendo?! Ninguém jamais dominou isso!",
                    "O equilíbrio destrói tanto o viés quanto a variância!",
                    "Você não pode sustentar esse poder!",
                    "Ele consumirá sua própria razão!"
                ]),
                ("Jack", [
                    "Chamarei esse poder de *Golpe do Equilíbrio*.",
                    "Nem força cega, nem instabilidade — apenas precisão justa.",
                    "Com ele, atacarei no ponto onde o erro se dissolve.",
                    "Prepare-se, Erradon... a batalha começa agora!"
                ])
                ]

        }

    def dialogo_fase(self, fase: int):
        """Retorna a lista de diálogos de uma fase."""
        return self.dialogos.get(
            fase,
            [("NARRADOR", ["Nenhum diálogo encontrado para essa fase."])]
        )
