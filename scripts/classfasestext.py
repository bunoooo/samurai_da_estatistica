import pygame

class Dialogos:
    def __init__(self):
        # Dicionário com os diálogos organizados por fase
        self.dialogos = {
    1: [
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
            "Temos os dados de produção e consumo. "
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
            2: [
                ("NARRADOR", [
                    "Você encontrou a Santa da Morte.",
                    "Ela guarda segredos que podem salvar a princesa.",
                    "Mas primeiro, você deve provar sua sabedoria."
                ]),
                ("SANTA DA MORTE", [
                    "Resolva o desafio estatístico que irei propor.",
                    "Somente assim o portal será ativado."
                ])
            ]
            # pode ir adicionando novas fases aqui...
        }

    def dialogo_fase(self, fase: int):
        return self.dialogos.get(fase, [("NARRADOR", ["Nenhum diálogo encontrado para essa fase."])])
