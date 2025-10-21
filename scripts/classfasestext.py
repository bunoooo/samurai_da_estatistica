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
                    "Samurai... bem-vindo ao lugar onde até a morte perdeu o controle.",
                    "Desde que a maldição começou, as almas que eu deveria colher não me escutam mais.",
                    "Elas se perdem... e retornam como esqueletos.",
                    "Tentei todos os rituais que conheço, mas nenhum funcionou."
                ]),
                ("Samurai", [
                    "Então a maldição está além da sua compreensão.",
                    "Diga-me, há algum padrão no modo como as almas se perdem?"
                ]),
                ("Ceifador", [
                    "Talvez sim... um sábio me deixou este gráfico.",
                    "Ele mostra quantas almas se perderam por tipo de causa da maldição.",
                    "Mas esses números me confundem. Eu apenas sinto a dor delas...",
                    "Não sei interpretar o que o gráfico revela."
                ]),
                ("Samurai", [
                    "Deixe-me ver...",
                    "Entendo. Cada barra representa uma causa possível da maldição.",
                    "Se observarmos qual causa tem mais almas perdidas, saberemos onde agir primeiro."
                ]),
                ("Ceifador", [
                    "Então devo escolher o ritual que enfraquece a causa mais devastadora?",
                    "Isso exigirá sabedoria... e talvez algumas moedas."
                ]),
                ("Samurai", [
                    "Exato. Visitaremos a loja de rituais.",
                    "Cada ritual foi feito para combater uma das causas possíveis da maldição.",
                    "Mas apenas um reduzirá o maior número de almas perdidas."
                ]),
                ("Ceifador", [
                    "Então olhe bem o gráfico, Samurai.",
                    "Descubra o coração desta maldição...",
                    "E compre o ritual certo antes que o silêncio da morte se torne eterno."
                ]),
                ("Samurai", [
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
            ]
        }

    def dialogo_fase(self, fase: int):
        """Retorna a lista de diálogos de uma fase."""
        return self.dialogos.get(
            fase,
            [("NARRADOR", ["Nenhum diálogo encontrado para essa fase."])]
        )
